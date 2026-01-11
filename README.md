# Advanced Transformer-Based Market Movement Prediction (AIML)

A state-of-the-art deep learning project using advanced transformer architectures for financial market prediction with comprehensive technical indicators, attention visualization, and model interpretability.

## 🚀 Advanced Features

### Model Architecture
- **Advanced Transformer** with positional encoding and multi-head attention
- **Attention Visualization** to understand model decision-making
- **Residual Connections** and Layer Normalization
- **GELU Activation** for improved non-linearity
- **Custom Attention Mechanisms** with visualization support

### Training Enhancements
- **Learning Rate Scheduling** with ReduceLROnPlateau
- **Early Stopping** to prevent overfitting
- **Gradient Clipping** for training stability
- **AdamW Optimizer** with weight decay
- **Advanced Loss Tracking** and visualization

### Data Processing
- **30+ Technical Indicators**:
  - Moving Averages (SMA, EMA)
  - MACD and RSI
  - Bollinger Bands
  - ATR (Average True Range)
  - Volume indicators
  - Momentum and ROC
  - Volatility measures
- **Automated Feature Engineering**
- **MinMax Scaling** for normalized inputs

### Hyperparameter Optimization
- **Bayesian Optimization** using Optuna
- **Traditional Grid Search** for comparison
- **Parameter Importance Analysis**
- **Optimization History Tracking**

### Model Evaluation & Interpretability
- **Comprehensive Metrics**: MSE, RMSE, MAE, MAPE, R²
- **Advanced Visualizations**:
  - Prediction vs Actual with error bands
  - Learning curves
  - Residual analysis
  - Error distribution
  - Attention heatmaps
  - Learning rate schedules
- **Feature Importance** using permutation method
- **Saliency Maps** for input importance
- **Ensemble Predictions** with uncertainty estimates

### Production-Ready API
- **FastAPI REST API** with OpenAPI documentation
- **Live Stock Predictions** with real-time data
- **Attention Weight Visualization** endpoints
- **Model Hot-Reloading**
- **Health Checks** and monitoring
- **CORS Support** for web integration

## 📋 Requirements
- Python 3.8+
- See [requirements.txt](requirements.txt) for all dependencies

## 🔧 Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd <project-folder>

# Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Deployment

### Quick Deploy (Choose One):

**🐳 Docker (Recommended):**
```bash
docker build -t market-predictor .
docker run -p 8000:8000 market-predictor
```

**🔥 Docker Compose (Full Stack):**
```bash
docker-compose up -d
```

**☁️ Cloud Platforms:**
- **Heroku:** `git push heroku main`
- **Railway:** One-click deploy from GitHub
- **Render:** Auto-deploy from repo
- **AWS/GCP/Azure:** See [DEPLOYMENT.md](DEPLOYMENT.md)

**📖 Full Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)  
**⚡ Quick Start:** [QUICKSTART_DEPLOY.md](QUICKSTART_DEPLOY.md)

### Test Deployment:
```bash
python test_deployment.py --url http://localhost:8000
```

## 📊 Usage

### 1. Basic Training
```bash
python main.py
```

### 2. Advanced Hyperparameter Search
```bash
python hyperparameter_search.py
```
Choose between:
- Bayesian Optimization (recommended - more efficient)
- Grid Search (traditional - exhaustive)

### 3. Start API Server
```bash
python serve.py
```
Access API documentation at: `http://localhost:8000/docs`

### 4. Model Interpretability
```python
from ensemble import ModelInterpreter, EnsemblePredictor

# Feature importance analysis
interpreter = ModelInterpreter()
importance = interpreter.feature_importance_permutation(model, X_test, y_test, feature_names)
interpreter.visualize_feature_importance(importance)

# Attention analysis
interpreter.analyze_attention_patterns(model, X_test)

# Saliency maps
interpreter.generate_saliency_map(model, X_test[0])
```

## 📁 Project Structure

```
├── main.py                          # Entry point
├── train.py                         # Advanced training with early stopping & LR scheduling
├── model.py                         # Advanced Transformer architecture
├── data_loader.py                   # Data processing with technical indicators
├── hyperparameter_search.py         # Bayesian & grid search optimization
├── ensemble.py                      # Ensemble models & interpretability
├── serve.py                         # FastAPI production server
├── utils.py                         # Helper utilities
├── config.json                      # Model configuration
├── requirements.txt                 # Dependencies
├── Dockerfile                       # Docker containerization
├── outputs/                         # Generated outputs
│   ├── model_*.pt                   # Trained models with metadata
│   ├── analysis_*.png               # Comprehensive analysis plots
│   ├── attention_*.png              # Attention visualizations
│   ├── feature_importance.png       # Feature importance plots
│   └── optimization_history.png     # Hyperparameter search results
├── experiment_log.json              # Experiment tracking
└── README.md                        # Documentation
```

## 🎯 Configuration

Edit [config.json](config.json) to customize:

```json
{
  "symbol": "AAPL",              // Stock symbol
  "start": "2015-01-01",         // Start date
  "end": "2024-01-01",           // End date
  "SEQ_LEN": 30,                 // Sequence length
  "EPOCHS": 100,                 // Training epochs
  "MODEL_DIM": 128,              // Model dimension
  "NUM_HEADS": 8,                // Attention heads
  "NUM_LAYERS": 3,               // Transformer layers
  "LR": 0.001,                   // Learning rate
  "dropout": 0.2,                // Dropout rate
  "patience": 20,                // Early stopping patience
  "use_technical_indicators": true
}
```

## 📈 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /model/info` - Model details
- `POST /predict` - Make predictions
- `POST /predict/live` - Live stock predictions
- `POST /model/reload` - Reload latest model
- `GET /experiments` - View all experiments
- `GET /outputs/{filename}` - Access generated files

## 🔬 Advanced Metrics

The model tracks:
- **MSE** (Mean Squared Error)
- **RMSE** (Root Mean Squared Error)
- **MAE** (Mean Absolute Error)
- **MAPE** (Mean Absolute Percentage Error)
- **R²** (Coefficient of Determination)

## 🎓 Model Interpretability

- **Attention Visualization**: See what the model focuses on
- **Feature Importance**: Understand which features matter most
- **Saliency Maps**: Visualize input importance over time
- **Ensemble Uncertainty**: Get confidence intervals

## 🐳 Docker Support

```bash
docker build -t market-predictor .
docker run -p 8000:8000 market-predictor
```

## 📝 Notes

- All outputs saved to `outputs/` directory with timestamps
- Experiment results logged to `experiment_log.json`
- Models saved with configuration and metrics
- Automatic attention weight extraction
- Support for multiple stock symbols
- Extensible to crypto, forex, and other markets

## 🔮 Future Enhancements

- [ ] Multi-asset portfolio prediction
- [ ] LSTM comparison models
- [ ] Real-time streaming predictions
- [ ] Backtesting framework
- [ ] Risk management metrics
- [ ] Sentiment analysis integration

## 📄 License

MIT License - feel free to use for research and educational purposes.

---

**Built with ❤️ using PyTorch, FastAPI, and Optuna**
