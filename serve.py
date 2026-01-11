from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
import numpy as np
import torch
from typing import List, Optional, Dict
import os
import json
from datetime import datetime
import glob
from model import AdvancedTimeSeriesTransformer
from data_loader import load_and_preprocess_data, add_technical_indicators, download_data
import uvicorn

app = FastAPI(
    title="Advanced Market Predictor API",
    version="2.0.0",
    description="Advanced transformer-based market prediction with technical indicators and attention visualization"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model and config
model = None
model_config = None
scaler = None
model_info = {}

class PredictionRequest(BaseModel):
    sequence: List[List[float]] = Field(..., description="Input sequence of shape (seq_len, n_features)")
    return_attention: bool = Field(default=False, description="Whether to return attention weights")

class PredictionResponse(BaseModel):
    prediction: float
    confidence: Optional[float] = None
    attention_weights: Optional[List] = None
    timestamp: str

class ModelInfo(BaseModel):
    model_loaded: bool
    model_path: str
    config: Optional[Dict]
    metrics: Optional[Dict]
    features: Optional[int]

class LivePredictionRequest(BaseModel):
    symbol: str = Field(..., description="Stock symbol (e.g., AAPL)")
    days_ahead: int = Field(default=1, description="Days to predict ahead")

def load_latest_model():
    """Load the most recent trained model"""
    global model, model_config, scaler, model_info
    
    # Find latest model file
    model_files = glob.glob('outputs/model_*.pt')
    if not model_files:
        model_files = glob.glob('model_*.pt')
    
    if not model_files:
        print("⚠️ No trained model found. Run train.py first!")
        model_info = {'model_loaded': False, 'error': 'No model found'}
        return False
    
    latest_model = max(model_files, key=os.path.getctime)
    
    try:
        checkpoint = torch.load(latest_model, map_location=torch.device('cpu'))
        model_config = checkpoint.get('config', {})
        scaler = checkpoint.get('scaler')
        metrics = checkpoint.get('metrics', {})
        
        # Initialize model
        input_dim = 33  # Default with technical indicators
        model = AdvancedTimeSeriesTransformer(
            input_dim=input_dim,
            model_dim=model_config.get('MODEL_DIM', 64),
            num_heads=model_config.get('NUM_HEADS', 4),
            num_layers=model_config.get('NUM_LAYERS', 2),
            dropout=model_config.get('dropout', 0.1),
            use_positional_encoding=model_config.get('use_positional_encoding', True)
        )
        
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        
        model_info = {
            'model_loaded': True,
            'model_path': latest_model,
            'config': model_config,
            'metrics': metrics,
            'features': input_dim
        }
        
        print(f"✅ Loaded model from {latest_model}")
        print(f"📊 Metrics: {metrics}")
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model_info = {'model_loaded': False, 'error': str(e)}
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize model on startup"""
    load_latest_model()

@app.get("/", response_model=Dict)
async def root():
    """API root endpoint"""
    return {
        "message": "Advanced Market Predictor API",
        "version": "2.0.0",
        "status": "running",
        "model_loaded": model is not None,
        "endpoints": {
            "health": "/health",
            "model_info": "/model/info",
            "predict": "/predict",
            "predict_live": "/predict/live",
            "attention": "/attention",
            "reload_model": "/model/reload"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    """Get information about the loaded model"""
    return model_info

@app.post("/model/reload")
async def reload_model():
    """Reload the latest model"""
    success = load_latest_model()
    if success:
        return {"status": "success", "message": "Model reloaded successfully", "info": model_info}
    else:
        raise HTTPException(status_code=500, detail="Failed to reload model")

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make a prediction from input sequence"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Run train.py first.")
    
    try:
        # Convert to tensor
        sequence = torch.FloatTensor(request.sequence).unsqueeze(0)  # Add batch dimension
        
        # Make prediction
        with torch.no_grad():
            if request.return_attention:
                prediction, attention_weights = model(sequence, return_attention=True)
                attention_data = [attn.cpu().numpy().tolist() for attn in attention_weights]
            else:
                prediction = model(sequence)
                attention_data = None
        
        pred_value = prediction.item()
        
        # Calculate confidence (inverse of prediction variance if we have ensemble)
        confidence = 0.95  # Placeholder
        
        return PredictionResponse(
            prediction=pred_value,
            confidence=confidence,
            attention_weights=attention_data,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict/live")
async def predict_live(request: LivePredictionRequest):
    """Make live prediction for a stock symbol"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Download recent data
        from datetime import datetime, timedelta
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        
        df = download_data(request.symbol, start_date, end_date)
        df = add_technical_indicators(df)
        
        # Get last sequence
        from sklearn.preprocessing import MinMaxScaler
        seq_len = model_config.get('SEQ_LEN', 30)
        
        temp_scaler = MinMaxScaler()
        scaled_data = temp_scaler.fit_transform(df.values)
        
        if len(scaled_data) < seq_len:
            raise HTTPException(status_code=400, detail=f"Not enough data. Need at least {seq_len} days")
        
        last_sequence = scaled_data[-seq_len:]
        sequence_tensor = torch.FloatTensor(last_sequence).unsqueeze(0)
        
        # Predict
        with torch.no_grad():
            prediction = model(sequence_tensor)
        
        # Inverse transform
        close_idx = df.columns.get_loc('Close')
        dummy = np.zeros((1, len(df.columns)))
        dummy[0, close_idx] = prediction.item()
        predicted_price = temp_scaler.inverse_transform(dummy)[0, close_idx]
        
        current_price = df['Close'].iloc[-1]
        change_percent = ((predicted_price - current_price) / current_price) * 100
        
        return {
            "symbol": request.symbol,
            "current_price": float(current_price),
            "predicted_price": float(predicted_price),
            "change_percent": float(change_percent),
            "direction": "UP" if change_percent > 0 else "DOWN",
            "days_ahead": request.days_ahead,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Live prediction error: {str(e)}")

@app.get("/attention/{sample_idx}")
async def get_attention_weights(sample_idx: int):
    """Get attention weights for a specific sample (for debugging/visualization)"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "message": "Attention visualization endpoint",
        "note": "Use /predict with return_attention=true to get attention weights"
    }

@app.get("/experiments")
async def get_experiments():
    """Get all logged experiments"""
    try:
        with open('experiment_log.json', 'r') as f:
            experiments = json.load(f)
        return {"experiments": experiments, "count": len(experiments)}
    except FileNotFoundError:
        return {"experiments": [], "count": 0}

@app.get("/outputs/{filename}")
async def get_output_file(filename: str):
    """Serve generated output files (plots, etc.)"""
    file_path = os.path.join('outputs', filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

def start_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the FastAPI server"""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    print("🚀 Starting Advanced Market Predictor API...")
    print("📖 API documentation available at: http://localhost:8000/docs")
    start_server()
