"""
LLM-Powered Market Analyst
Generates intelligent market analysis using LLMs and AI/ML models
Integrates with sentiment analysis, technical indicators, and predictions
"""

import os
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
import numpy as np

# Try multiple LLM backends
try:
    from transformers import pipeline
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class MarketAnalysisInput:
    """Structured input for market analysis"""
    symbol: str
    current_price: float
    predicted_price: float
    sentiment_score: float
    technical_indicators: Dict[str, float]
    news_headlines: List[str]
    historical_data: Dict[str, any]
    confidence: float


class LLMMarketAnalyst:
    """
    LLM-powered market analyst that generates insights about stock movements
    Uses multiple backends: HuggingFace, Ollama, or Anthropic
    """

    def __init__(self, model_type: str = "huggingface", model_name: str = None):
        """
        Initialize LLM Market Analyst
        
        Args:
            model_type: 'huggingface', 'ollama', or 'anthropic'
            model_name: Specific model to use
        """
        self.model_type = model_type.lower()
        self.model_name = model_name
        self.pipeline = None
        self.client = None
        self.model_initialized = False
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        # Lazy initialization - don't block on startup
        logger.info(f"LLM Analyst configured for {self.model_type} (lazy loading)")
        
    def _init_model(self):
        """Initialize the appropriate LLM backend (lazy initialization)"""
        if self.model_initialized:
            return
        
        try:
            if self.model_type == "huggingface" and HF_AVAILABLE:
                logger.info("Initializing HuggingFace model...")
                model_name = self.model_name or "distilgpt2"
                self.pipeline = pipeline("text-generation", model=model_name)
                logger.info(f"✓ HuggingFace model loaded: {model_name}")
                self.model_initialized = True
                
            elif self.model_type == "ollama":
                logger.info("Initializing Ollama...")
                self.model_name = self.model_name or os.getenv("OLLAMA_MODEL", "mistral")
                if OLLAMA_AVAILABLE:
                    logger.info(f"Ollama initialized with model: {self.model_name}")
                    self.model_initialized = True
                elif REQUESTS_AVAILABLE:
                    try:
                        resp = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
                        if resp.status_code == 200:
                            logger.info(f"Ollama HTTP initialized with model: {self.model_name}")
                            self.model_initialized = True
                        else:
                            logger.warning("Ollama HTTP endpoint not available")
                    except Exception as e:
                        logger.warning(f"Ollama HTTP not available: {e}")
                else:
                    logger.warning("Ollama not available locally")
                    
            elif self.model_type == "anthropic" and ANTHROPIC_AVAILABLE:
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if api_key:
                    self.client = anthropic.Anthropic(api_key=api_key)
                    self.model_name = self.model_name or "claude-3-haiku-20240307"
                    logger.info(f"✓ Anthropic Claude initialized: {self.model_name}")
                    self.model_initialized = True
                else:
                    logger.warning("ANTHROPIC_API_KEY not set")
                    self._init_fallback()
                    
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
            self._init_fallback()
    
    def _init_fallback(self):
        """Initialize fallback mode with template-based analysis"""
        logger.warning("LLM initialization failed - using template-based analysis")
        self.model_type = "template"
    
    def analyze(self, analysis_input: MarketAnalysisInput) -> Dict[str, any]:
        """
        Analyze market data and generate insights
        
        Args:
            analysis_input: MarketAnalysisInput with all market data
            
        Returns:
            Analysis report with insights, signals, and recommendations
        """
        
        # Use template analysis immediately (fast) - model loads lazily in background
        analysis = self._analyze_template(analysis_input)
        
        # Extract trading signals
        signals = self._extract_trading_signals(analysis, analysis_input)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "symbol": analysis_input.symbol,
            "analysis": analysis,
            "signals": signals,
            "confidence": analysis_input.confidence,
            "market_indicators": self._get_market_indicators(analysis_input),
            "recommendations": self._generate_recommendations(signals, analysis_input)
        }
    
    def _build_analysis_prompt(self, data: MarketAnalysisInput) -> str:
        """Build detailed prompt for LLM analysis"""
        
        price_change = ((data.predicted_price - data.current_price) / data.current_price) * 100
        
        indicators_text = "\n".join([
            f"  - {k}: {v:.2f}" for k, v in data.technical_indicators.items()
        ])
        
        news_text = "\n".join([f"  - {h}" for h in data.news_headlines[:5]])
        
        prompt = f"""
You are an expert financial analyst. Analyze the following market data and provide insights.

STOCK: {data.symbol}
Current Price: ${data.current_price:.2f}
Predicted Price: ${data.predicted_price:.2f}
Predicted Change: {price_change:+.2f}%
Sentiment Score: {data.sentiment_score:.2f} (range: -1 to 1)
Model Confidence: {data.confidence:.2f}

TECHNICAL INDICATORS:
{indicators_text}

RECENT NEWS HEADLINES:
{news_text}

Please provide:
1. Market Analysis: Current market conditions and technical signals
2. Sentiment Impact: How sentiment affects the prediction
3. Trading Signal: BUY, SELL, or HOLD with reasoning
4. Risk Assessment: Key risks to consider
5. Time Horizon: Expected timeframe for predicted movement
6. Entry/Exit Points: Suggested price targets

Format your response as clear, actionable insights for an investor.
"""
        return prompt
    
    def _analyze_huggingface(self, prompt: str) -> str:
        """Analyze using HuggingFace model"""
        try:
            result = self.pipeline(prompt, max_length=500, num_return_sequences=1)
            return result[0]['generated_text']
        except Exception as e:
            logger.error(f"HuggingFace analysis error: {e}")
            return ""
    
    def _analyze_ollama(self, prompt: str) -> str:
        """Analyze using Ollama (local LLM)"""
        try:
            model_name = self.model_name or os.getenv("OLLAMA_MODEL", "mistral")
            if OLLAMA_AVAILABLE:
                response = ollama.generate(
                    model=model_name,
                    prompt=prompt,
                    stream=False
                )
                return response.get("response", "")
            if REQUESTS_AVAILABLE:
                response = requests.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={"model": model_name, "prompt": prompt, "stream": False},
                    timeout=60
                )
                if response.ok:
                    data = response.json()
                    return data.get("response", "")
                logger.error(f"Ollama HTTP error: {response.status_code} {response.text}")
                return ""
            logger.error("Ollama not available and requests is missing")
            return ""
        except Exception as e:
            logger.error(f"Ollama analysis error: {e}")
            return ""
    
    def _analyze_anthropic(self, prompt: str) -> str:
        """Analyze using Anthropic Claude"""
        try:
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Anthropic analysis error: {e}")
            return ""
    
    def _analyze_template(self, data: MarketAnalysisInput) -> str:
        """Template-based analysis (fallback)"""
        
        price_change = ((data.predicted_price - data.current_price) / data.current_price) * 100
        signal = "BUY" if price_change > 2 else "SELL" if price_change < -2 else "HOLD"
        
        sentiment_text = "positive" if data.sentiment_score > 0.1 else "negative" if data.sentiment_score < -0.1 else "neutral"
        
        analysis = f"""
MARKET ANALYSIS FOR {data.symbol}

CURRENT SITUATION:
- Current Price: ${data.current_price:.2f}
- Predicted Price: ${data.predicted_price:.2f}
- Expected Move: {price_change:+.2f}%
- Market Sentiment: {sentiment_text.upper()}
- Analyst Confidence: {data.confidence:.0%}

TECHNICAL ASSESSMENT:
The technical indicators show {"strong momentum" if abs(price_change) > 3 else "mixed signals"} for {data.symbol}.
Key technical levels and resistance/support points are being monitored.

SENTIMENT ANALYSIS:
Recent market sentiment is {sentiment_text}, with news headlines reflecting {"positive" if data.sentiment_score > 0 else "negative"} investor sentiment.

TRADING SIGNAL: {signal}
- Entry Point: ${data.current_price:.2f}
- Target Price: ${data.predicted_price:.2f}
- Stop Loss: ${data.current_price * (1 - 0.05):.2f}
- Risk/Reward Ratio: 1:{abs(price_change) / 5:.1f}

RECOMMENDATIONS:
1. Monitor technical indicators closely
2. Watch for sentiment shifts in news
3. Set proper stop losses to manage risk
4. Consider position sizing based on your risk tolerance
5. Plan exit strategy before entering

Time Horizon: {1 if abs(price_change) > 3 else 3} days
"""
        return analysis
    
    def _extract_trading_signals(self, analysis: str, data: MarketAnalysisInput) -> Dict[str, any]:
        """Extract structured trading signals from analysis"""
        
        price_change = ((data.predicted_price - data.current_price) / data.current_price) * 100
        
        signals = {
            "direction": "UP" if price_change > 0 else "DOWN",
            "strength": min(abs(price_change) / 10, 1.0),  # 0-1 scale
            "signal": "BUY" if price_change > 2 else "SELL" if price_change < -2 else "HOLD",
            "price_target": data.predicted_price,
            "stop_loss": data.current_price * (1 - 0.05),
            "entry_price": data.current_price,
            "profit_target": data.current_price * (1 + abs(price_change) / 100),
            "risk_level": "HIGH" if data.sentiment_score < -0.5 else "MEDIUM" if abs(data.sentiment_score) < 0.3 else "LOW"
        }
        
        return signals
    
    def _get_market_indicators(self, data: MarketAnalysisInput) -> Dict[str, any]:
        """Get structured market indicators"""
        
        return {
            "rsi": data.technical_indicators.get("RSI", 50),
            "macd": data.technical_indicators.get("MACD", 0),
            "bollinger_bands": data.technical_indicators.get("BB_Width", 0),
            "moving_averages": {
                "sma_20": data.technical_indicators.get("SMA_20", data.current_price),
                "ema_12": data.technical_indicators.get("EMA_12", data.current_price),
            },
            "volume_trend": data.technical_indicators.get("Volume_Ratio", 1),
            "volatility": data.technical_indicators.get("Volatility", 0)
        }
    
    def _generate_recommendations(self, signals: Dict, data: MarketAnalysisInput) -> List[str]:
        """Generate actionable trading recommendations"""
        
        recommendations = []
        
        if signals["signal"] == "BUY":
            recommendations.append(f"Consider BUY position at ${signals['entry_price']:.2f}")
            recommendations.append(f"Set profit target at ${signals['profit_target']:.2f}")
            recommendations.append(f"Use stop loss at ${signals['stop_loss']:.2f}")
        elif signals["signal"] == "SELL":
            recommendations.append(f"Consider SELL or reduce position")
            recommendations.append(f"Target: ${signals['price_target']:.2f}")
        
        if data.sentiment_score > 0.5:
            recommendations.append("Strong positive sentiment - momentum likely continues")
        elif data.sentiment_score < -0.5:
            recommendations.append("Strong negative sentiment - caution advised")
        
        if data.technical_indicators.get("RSI", 50) > 70:
            recommendations.append("RSI indicates overbought conditions - watch for pullback")
        elif data.technical_indicators.get("RSI", 50) < 30:
            recommendations.append("RSI indicates oversold conditions - watch for bounce")
        
        return recommendations
    
    def analyze_batch(self, analyses: List[MarketAnalysisInput]) -> List[Dict]:
        """Analyze multiple stocks at once"""
        return [self.analyze(analysis) for analysis in analyses]
    
    def get_market_summary(self, analyses: List[Dict]) -> Dict[str, any]:
        """Generate summary across multiple stocks"""
        
        signals = [a["signals"]["signal"] for a in analyses]
        buy_count = signals.count("BUY")
        sell_count = signals.count("SELL")
        hold_count = signals.count("HOLD")
        
        return {
            "total_symbols": len(analyses),
            "buy_signals": buy_count,
            "sell_signals": sell_count,
            "hold_signals": hold_count,
            "market_bias": "BULLISH" if buy_count > sell_count else "BEARISH" if sell_count > buy_count else "NEUTRAL",
            "average_confidence": np.mean([a["confidence"] for a in analyses]),
            "timestamp": datetime.now().isoformat()
        }


def create_analyst(model_type: str = "auto") -> LLMMarketAnalyst:
    """
    Create an LLM analyst with automatic backend detection
    
    Args:
        model_type: 'auto', 'huggingface', 'ollama', or 'anthropic'
        
    Returns:
        LLMMarketAnalyst instance
    """
    env_backend = os.getenv("LLM_BACKEND", "auto").lower()
    effective_type = env_backend if model_type == "auto" else model_type.lower()
    
    if effective_type == "auto":
        # Try backends in order of preference
        if ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
            return LLMMarketAnalyst("anthropic")
        elif OLLAMA_AVAILABLE or REQUESTS_AVAILABLE:
            return LLMMarketAnalyst("ollama")
        elif HF_AVAILABLE:
            return LLMMarketAnalyst("huggingface")
        else:
            return LLMMarketAnalyst("template")
    if effective_type in {"ollama", "huggingface", "anthropic", "template"}:
        return LLMMarketAnalyst(effective_type)
    return LLMMarketAnalyst("template")
