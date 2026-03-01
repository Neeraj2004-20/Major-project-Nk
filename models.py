"""
Request/Response Models with Validation
Pydantic models for data validation and serialization
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class TradingSignal(str, Enum):
    """Trading signal types"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class PredictionRequest(BaseModel):
    """Stock prediction request model"""
    symbol: str = Field(..., min_length=1, max_length=10, example="AAPL")
    current_price: float = Field(..., gt=0, example=150.50)
    timeframe: str = Field("1d", example="1d")
    include_sentiment: bool = Field(False, example=True)
    include_technicals: bool = Field(True, example=True)
    
    @validator('symbol')
    def symbol_uppercase(cls, v):
        return v.upper()


class PredictionResponse(BaseModel):
    """Stock prediction response model"""
    symbol: str
    current_price: float
    predicted_price: float
    confidence: float = Field(..., ge=0, le=1)
    signal: TradingSignal
    timeframe: str
    reasoning: str
    timestamp: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AnalysisRequest(BaseModel):
    """Stock analysis request"""
    symbol: str = Field(..., example="AAPL")
    analysis_type: str = Field("comprehensive", example="comprehensive")
    include_sentiment: bool = False
    include_news: bool = False


class AnalysisResponse(BaseModel):
    """Stock analysis response"""
    symbol: str
    analysis: Dict[str, Any]
    sentiment: Optional[Dict[str, Any]] = None
    confidence: float
    timestamp: datetime


class HealthStatus(BaseModel):
    """System health status"""
    status: str = Field(..., example="healthy")
    timestamp: datetime
    uptime_seconds: float
    uptime_formatted: str
    system: Dict[str, Any]
    server: Dict[str, Any]
    api: Dict[str, Any]
    features: Dict[str, Any]


class MetricsResponse(BaseModel):
    """Performance metrics response"""
    performance: Dict[str, Any]
    health: HealthStatus


class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str
    error_type: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class PortfolioOptimizationRequest(BaseModel):
    """Portfolio optimization request"""
    symbols: List[str] = Field(..., min_items=1, max_items=50)
    amounts: List[float] = Field(..., min_items=1, max_items=50)
    risk_level: str = Field("medium", example="low|medium|high")


class PortfolioOptimizationResponse(BaseModel):
    """Portfolio optimization response"""
    original_allocation: Dict[str, float]
    optimized_allocation: Dict[str, float]
    expected_return: float
    risk_score: float
    recommendations: List[str]
    timestamp: datetime


class BulkPredictionRequest(BaseModel):
    """Bulk prediction for multiple stocks"""
    symbols: List[str] = Field(..., min_items=1, max_items=100)
    timeframe: str = "1d"


class BulkPredictionResponse(BaseModel):
    """Bulk prediction response"""
    predictions: List[PredictionResponse]
    total: int
    timestamp: datetime


class AlertRequest(BaseModel):
    """Trading alert configuration"""
    symbol: str
    alert_type: str = Field("price", example="price|sentiment|signal")
    threshold: float
    action: str = Field("notify", example="notify|execute")


class AlertResponse(BaseModel):
    """Trading alert response"""
    alert_id: str
    symbol: str
    alert_type: str
    threshold: float
    is_active: bool
    created_at: datetime


class BacktestRequest(BaseModel):
    """Backtesting request"""
    symbol: str
    start_date: datetime
    end_date: datetime
    strategy: str = "momentum"
    initial_capital: float = 10000


class BacktestResponse(BaseModel):
    """Backtesting results"""
    symbol: str
    period: Dict[str, str]
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    trades: int
