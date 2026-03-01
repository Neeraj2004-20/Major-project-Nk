"""
FastAPI Endpoints for LLM/AI Market Intelligence
Integrates LLM analysis with existing stock prediction API
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
from datetime import datetime

# Import new modules for enhanced predictions
from prediction_db import prediction_db
from graph_generator import GraphGenerator, format_chart_data
from ai_trainer import ai_trainer

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/ai", tags=["AI Analysis"])

# Global AI intelligence instance
ai_intelligence = None

# Fallback engines
from simple_prediction import simple_predictor
from simple_sentiment import simple_analyzer


def init_ai_system():
    """Initialize AI system (lazy - models load on demand)"""
    global ai_intelligence
    if ai_intelligence is None:
        try:
            from ai_llm_integration import create_ai_intelligence
            ai_intelligence = create_ai_intelligence()
            logger.info("✓ AI Intelligence system ready (lazy loading)")
        except ImportError as e:
            logger.warning(f"AI Intelligence unavailable: {e}")
            ai_intelligence = None
    return ai_intelligence


def get_ai_system():
    """Get AI system, initializing if needed"""
    global ai_intelligence
    if ai_intelligence is None:
        init_ai_system()
    return ai_intelligence


# Request/Response models
class AnalyzeStockRequest(BaseModel):
    symbol: str
    current_price: float
    predicted_price: Optional[float] = None
    sentiment_score: float = 0
    technical_indicators: Dict = {}
    news_headlines: List[str] = []
    sentiment_text: Optional[str] = None
    confidence: float = 0.7


class ChatRequest(BaseModel):
    message: str


class MarketSummaryRequest(BaseModel):
    symbols: List[str]


# Endpoints
@router.post("/analyze")
async def analyze_stock(request: AnalyzeStockRequest):
    """
    Get comprehensive AI analysis for a stock
    Uses LLM if available, falls back to simple prediction engine
    """
    try:
        # Try to use full LLM system
        try:
            ai = get_ai_system()
            if ai:
                # Use provided predicted_price or let analyzer predict
                analysis = ai.analyze_stock(
                    symbol=request.symbol,
                    current_price=request.current_price,
                    predicted_price=request.predicted_price or request.current_price,
                    technical_indicators=request.technical_indicators,
                    news_headlines=request.news_headlines,
                    confidence=request.confidence
                )
                return {
                    "status": "success",
                    "data": analysis,
                    "engine": "full_llm"
                }
        except Exception as llm_error:
            logger.warning(f"LLM unavailable: {type(llm_error).__name__}, using fallback")
        
        # Fallback to simple prediction
        # Combine sentiment from multiple sources
        sentiment_text = request.sentiment_text or " ".join(request.news_headlines or [])
        sentiment_data = simple_analyzer.analyze_sentiment(sentiment_text)
        
        prediction = simple_predictor.analyze_with_sentiment(
            symbol=request.symbol,
            current_price=request.current_price,
            sentiment=sentiment_data
        )
        
        return {
            "status": "success",
            "data": prediction,
            "engine": "fallback_simple",
            "note": "Using simplified prediction engine - full LLM not available"
        }
    
    except Exception as e:
        logger.error(f"Analysis error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analyze/{symbol}")
async def get_cached_analysis(symbol: str):
    """
    Get previously cached analysis for a symbol
    Or get quick prediction
    """
    try:
        # Try cached analysis first
        try:
            if ai_intelligence and symbol in ai_intelligence.analysis_cache:
                return {
                    "status": "success",
                    "data": ai_intelligence.analysis_cache[symbol],
                    "source": "cache"
                }
        except:
            pass
        
        # Fallback: return quick prediction
        return {
            "status": "info",
            "message": f"No cached analysis for {symbol}",
            "available_endpoints": [
                f"POST /api/ai/analyze - Full analysis",
                f"POST /api/ai/sentiment - Sentiment analysis",
                f"GET /api/ai/predict/{{symbol}} - Get prediction"
            ]
        }
    
    except Exception as e:
        logger.error(f"Cache retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sentiment")
async def analyze_sentiment(text: str = Query(..., min_length=1)):
    """
    Analyze sentiment from text
    
    Args:
        text: Text to analyze for sentiment
        
    Returns:
        Sentiment score and classification
    """
    try:
        sentiment = simple_analyzer.analyze_sentiment(text)
        return {
            "status": "success",
            "data": sentiment,
            "engine": "simple_keyword_based"
        }
    except Exception as e:
        logger.error(f"Sentiment analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict")
@router.get("/predict")
async def quick_predict(symbol: str = Query(...), current_price: float = Query(..., gt=0)):
    """
    Get quick price prediction for a symbol
    
    Args:
        symbol: Stock symbol
        current_price: Current stock price
        
    Returns:
        Quick prediction with signal
    """
    try:
        prediction = simple_predictor.predict(
            symbol=symbol,
            current_price=current_price
        )
        
        # Store prediction in database for history and AI training
        prediction_db.store_prediction(symbol, prediction)
        
        return {
            "status": "success",
            "data": prediction,
            "engine": "simple_heuristic"
        }
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predict/{symbol}")
async def get_cached_prediction(symbol: str):
    """Get cached prediction for a symbol"""
    try:
        prediction = simple_predictor.get_cached_prediction(symbol)
        if prediction:
            return {
                "status": "success",
                "data": prediction
            }
        else:
            return {
                "status": "not_found",
                "message": f"No cached prediction for {symbol}"
            }
    except Exception as e:
        logger.error(f"Error retrieving prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
async def chat_with_analyst(request: ChatRequest):
    """
    Chat with AI market analyst
    Falls back to simple prediction if LLM unavailable
    """
    try:
        # Try LLM
        try:
            if not ai_intelligence:
                init_ai_system()
            
            response = ai_intelligence.chat(request.message)
            
            return {
                "status": "success",
                "response": response,
                "engine": "full_llm",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as llm_error:
            logger.warning(f"LLM chat unavailable: {type(llm_error).__name__}")
        
        # Fallback response
        return {
            "status": "success",
            "response": f"I can help with stock analysis. Available commands: /predict SYMBOL, /sentiment 'text', /analyze SYMBOL PRICE",
            "engine": "fallback_simple",
            "note": "Running in fallback mode",
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversation-history")
async def get_conversation_history(limit: int = Query(10, ge=1, le=100)):
    """
    Get conversation history with AI analyst
    
    Args:
        limit: Number of recent conversations to return
        
    Returns:
        List of conversation turns
    """
    try:
        if not ai_intelligence:
            init_ai_system()
        
        history = ai_intelligence.conversation_agent.get_conversation_history(limit)
        
        return {
            "status": "success",
            "total": len(history),
            "data": history
        }
    
    except Exception as e:
        logger.error(f"History retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/market-summary")
async def get_market_summary(request: MarketSummaryRequest):
    """
    Get market summary across multiple stocks
    
    Args:
        request: MarketSummaryRequest with list of symbols
        
    Returns:
        Market-wide summary and insights
    """
    try:
        if not ai_intelligence:
            init_ai_system()
        
        summary = ai_intelligence.get_market_summary(request.symbols)
        
        return {
            "status": "success",
            "data": summary
        }
    
    except Exception as e:
        logger.error(f"Market summary error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts")
async def get_trading_alerts(symbols: List[str] = Query(...)):
    """
    Get trading alerts for symbols
    
    Args:
        symbols: List of stock symbols
        
    Returns:
        Trading alerts sorted by signal strength
    """
    try:
        if not ai_intelligence:
            init_ai_system()
        
        alerts = ai_intelligence.get_trading_alerts(symbols)
        
        return {
            "status": "success",
            "total_alerts": len(alerts),
            "data": alerts
        }
    
    except Exception as e:
        logger.error(f"Alerts error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance")
async def get_performance_metrics():
    """
    Get AI system performance metrics
    
    Returns:
        Analysis statistics and performance data
    """
    try:
        if not ai_intelligence:
            init_ai_system()
        
        metrics = ai_intelligence.get_performance_metrics()
        
        return {
            "status": "success",
            "data": metrics
        }
    
    except Exception as e:
        logger.error(f"Metrics error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export")
async def export_analysis(filepath: str = Query(...), format: str = Query("json")):
    """
    Export analysis data
    
    Args:
        filepath: Where to save the file
        format: Export format (json or csv)
        
    Returns:
        Export status
    """
    try:
        if not ai_intelligence:
            init_ai_system()
        
        ai_intelligence.export_analysis(filepath, format)
        
        return {
            "status": "success",
            "message": f"Analysis exported to {filepath}",
            "format": format
        }
    
    except Exception as e:
        logger.error(f"Export error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Check AI system health"""
    
    try:
        # Check what's available
        status = "degraded"
        services = {
            "fallback_prediction": "available",
            "fallback_sentiment": "available"
        }
        
        try:
            if not ai_intelligence:
                init_ai_system()
            services["llm_analytics"] = "available"
            status = "healthy"
        except Exception as e:
            services["llm_analytics"] = f"unavailable: {type(e).__name__}"
        
        return {
            "status": status,
            "services": services,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "services": {
                "fallback_prediction": "available",
                "fallback_sentiment": "available"
            }
        }


# ============================================================
# DATABASE & HISTORY ENDPOINTS
# ============================================================

@router.get("/history/{symbol}")
async def get_prediction_history(symbol: str, days: int = Query(30, ge=1, le=365)):
    """Get prediction history for a symbol"""
    try:
        history = prediction_db.get_predictions_history(symbol, days)
        return {
            "status": "success",
            "symbol": symbol,
            "days": days,
            "total_predictions": len(history),
            "predictions": history,
            "accuracy": prediction_db.get_accuracy(symbol)
        }
    except Exception as e:
        logger.error(f"History error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# GRAPH & VISUALIZATION ENDPOINTS
# ============================================================

@router.get("/chart/{symbol}")
async def get_ascii_chart(symbol: str, days: int = Query(30, ge=1, le=365)):
    """Get ASCII chart for symbol - shows price trends (UP/DOWN)"""
    try:
        history = prediction_db.get_predictions_history(symbol, days)
        if not history:
            return {"status": "no_data", "message": "No predictions found"}
        
        # Extract prices
        prices = [p.get('predicted_price', 0) for p in history]
        
        # Generate chart
        chart = GraphGenerator.create_ascii_chart(
            prices,
            title=f"{symbol} Price Trend (Last {days} days)"
        )
        
        # Analyze trend
        trend = GraphGenerator.create_trend_analysis(prices)
        
        return {
            "status": "success",
            "symbol": symbol,
            "chart": chart,
            "trend_analysis": trend,
            "total_data_points": len(prices)
        }
    except Exception as e:
        logger.error(f"Chart error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/graph/{symbol}")
async def get_graph_data(symbol: str, days: int = Query(30, ge=1, le=365)):
    """Get graph data for web visualization (JSON format)"""
    try:
        history = prediction_db.get_predictions_history(symbol, days)
        if not history:
            return {"status": "no_data"}
        
        chart_data = format_chart_data(history)
        trend = GraphGenerator.create_trend_analysis(
            chart_data['predicted']
        )
        
        return {
            "status": "success",
            "symbol": symbol,
            "chart_data": chart_data,
            "trend": trend,
            "prediction_count": len(history),
            "accuracy": prediction_db.get_accuracy(symbol)
        }
    except Exception as e:
        logger.error(f"Graph error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# AI TRAINING & FEEDBACK ENDPOINTS
# ============================================================

class FeedbackRequest(BaseModel):
    symbol: str
    prediction_idx: int
    correct: bool
    signal: str = "HOLD"
    notes: Optional[str] = None


@router.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit feedback on prediction accuracy for AI training"""
    try:
        prediction_db.add_feedback(
            feedback.symbol,
            feedback.prediction_idx,
            feedback.correct,
            feedback.notes or ""
        )
        
        return {
            "status": "success",
            "message": "Feedback recorded for AI training",
            "symbol": feedback.symbol,
            "feedback_correct": feedback.correct
        }
    except Exception as e:
        logger.error(f"Feedback error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train")
async def train_model(symbol: Optional[str] = None):
    """Train AI model on accumulated feedback"""
    try:
        # Get feedback
        if symbol:
            feedback = prediction_db.get_feedback(symbol)
        else:
            feedback = prediction_db.get_feedback()
        
        if not feedback:
            return {
                "status": "no_feedback",
                "message": "No feedback available for training"
            }
        
        # Process feedback
        result = ai_trainer.process_feedback(feedback)
        
        # Get suggestions
        suggestions = ai_trainer.suggest_improvement(
            symbol or "all",
            feedback
        )
        
        return {
            "status": result.get('status'),
            "updated": result.get('updated'),
            "training_summary": {
                "feedback_processed": result.get('total_feedback'),
                "accuracy_rate": result.get('accuracy_rate'),
                "signal_accuracy": result.get('signal_accuracy')
            },
            "suggestions": suggestions.get('suggestions'),
            "symbol": symbol or "all"
        }
    except Exception as e:
        logger.error(f"Training error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model-stats")
async def get_model_statistics():
    """Get AI model training statistics"""
    try:
        stats = ai_trainer.get_model_stats()
        db_stats = prediction_db.get_statistics()
        
        return {
            "status": "success",
            "ai_model": stats,
            "database": db_stats,
            "system_status": "Ready for predictions with AI training"
        }
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/accuracy/{symbol}")
async def get_accuracy_metrics(symbol: str):
    """Get accuracy metrics for specific symbol"""
    try:
        accuracy = prediction_db.get_accuracy(symbol)
        history = prediction_db.get_predictions_history(symbol)
        
        return {
            "status": "success",
            "symbol": symbol,
            "accuracy_metrics": accuracy,
            "total_predictions": len(history),
            "last_prediction": history[-1] if history else None
        }
    except Exception as e:
        logger.error(f"Accuracy error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/store-prediction")
async def store_prediction(symbol: str, prediction_data: Dict):
    """Store prediction in database (called internally)"""
    try:
        record = prediction_db.store_prediction(symbol, prediction_data)
        return {
            "status": "success",
            "stored": record
        }
    except Exception as e:
        logger.error(f"Store error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_system_info():
    """Get AI system information"""
    
    try:
        if ai_intelligence:
            return {
                "system": "AI Market Intelligence",
                "version": "2.0.0",
                "mode": "full_llm",
                "components": {
                    "llm_analyst": "active",
                    "conversational_agent": "active",
                    "sentiment_analysis": "full",
                    "prediction_engine": "full"
                }
            }
    except:
        pass
    
    return {
        "system": "AI Market Intelligence",
        "version": "2.0.0",
        "mode": "fallback",
        "components": {
            "llm_analyst": "unavailable",
            "conversational_agent": "unavailable",
            "sentiment_analysis": "simple_keyword_based",
            "prediction_engine": "simple_heuristic"
        },
        "note": "Running in fallback mode - full ML dependencies not loaded",
        "features": [
            "Conversational AI assistant",
            "Market summary and alerts",
            "Performance metrics"
        ],
        "endpoints": [
            "POST /api/ai/analyze - Analyze stock",
            "GET /api/ai/analyze/{symbol} - Get cached analysis",
            "POST /api/ai/chat - Chat with analyst",
            "GET /api/ai/conversation-history - Get chat history",
            "POST /api/ai/market-summary - Market overview",
            "GET /api/ai/alerts - Trading alerts",
            "GET /api/ai/performance - Performance metrics",
            "POST /api/ai/export - Export analysis",
            "GET /api/ai/health - Health check",
            "GET /api/ai/info - System information"
        ]
    }


# Export router for main app
__all__ = ["router", "init_ai_system"]
