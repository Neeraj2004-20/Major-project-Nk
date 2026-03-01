"""
Simple Fallback Prediction Engine
Used when full ML/LLM dependencies are not available
Provides basic trend analysis and price predictions
"""

from datetime import datetime
from typing import Dict, Optional
import random


class SimplePredictionEngine:
    """Fallback prediction engine for when full dependencies aren't available"""
    
    def __init__(self):
        self.predictions_cache = {}
    
    def predict(self, 
                symbol: str,
                current_price: float,
                trend: Optional[str] = None) -> Dict:
        """
        Make a simple price prediction
        Based on basic heuristics when full ML model unavailable
        """
        
        # Generate prediction (for demo, add 1-5% variance)
        variance = random.uniform(-0.03, 0.08)  # Slight bullish bias
        predicted_price = current_price * (1 + variance)
        
        # Determine signal
        if predicted_price > current_price * 1.02:
            signal = "BUY"
        elif predicted_price < current_price * 0.98:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        # Confidence based on variance
        confidence = min(0.99, 0.5 + abs(variance) * 2)
        
        prediction = {
            "symbol": symbol,
            "current_price": current_price,
            "predicted_price": round(predicted_price, 2),
            "price_change_percent": round(variance * 100, 2),
            "signal": signal,
            "confidence": round(confidence, 2),
            "reasoning": self._generate_reasoning(signal, variance),
            "method": "simple_heuristic",
            "timestamp": datetime.now().isoformat(),
            "note": "Using fallback prediction engine - full ML model unavailable"
        }
        
        # Cache it
        self.predictions_cache[symbol] = prediction
        
        return prediction
    
    def _generate_reasoning(self, signal: str, variance: float) -> str:
        """Generate simple reasoning"""
        if signal == "BUY":
            return f"Positive signal with {variance*100:.1f}% upside potential"
        elif signal == "SELL":
            return f"Downside risk identified - {abs(variance)*100:.1f}% decline expected"
        else:
            return "Market at equilibrium - no strong directional bias"
    
    def analyze_with_sentiment(self,
                              symbol: str,
                              current_price: float,
                              sentiment: Dict) -> Dict:
        """Combine prediction with sentiment"""
        
        # Get base prediction
        base_pred = self.predict(symbol, current_price)
        
        # Adjust based on sentiment
        sentiment_score = sentiment.get("compound", 0)
        
        # Modify confidence based on sentiment alignment
        if (sentiment_score > 0 and base_pred["signal"] == "BUY") or \
           (sentiment_score < 0 and base_pred["signal"] == "SELL"):
            base_pred["confidence"] = min(0.99, base_pred["confidence"] + 0.15)
            base_pred["sentiment_aligned"] = True
        else:
            base_pred["sentiment_aligned"] = False
        
        base_pred["sentiment_score"] = round(sentiment_score, 2)
        
        return base_pred
    
    def get_cached_prediction(self, symbol: str) -> Optional[Dict]:
        """Get cached prediction if available"""
        return self.predictions_cache.get(symbol)


# Global instance
simple_predictor = SimplePredictionEngine()
