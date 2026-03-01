"""
Simple Fallback Sentiment Analyzer
Used when advanced sentiment libraries are not available
"""

import random
from datetime import datetime
from typing import Dict, List, Optional


class SimpleSentimentAnalyzer:
    """Fallback sentiment analyzer for when full dependencies aren't available"""
    
    def __init__(self):
        self.history = []
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment from text"""
        if not text:
            return self._neutral_sentiment()
        
        # Simple keyword-based sentiment
        positive_words = ['buy', 'bullish', 'gain', 'profit', 'strong', 'growth', 'surge', 'soars', 'excellent']
        negative_words = ['sell', 'bearish', 'loss', 'decline', 'weak', 'fall', 'crash', 'plunge', 'poor']
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        total = pos_count + neg_count
        
        if total == 0:
            return self._neutral_sentiment()
        
        compound = (pos_count - neg_count) / total if total > 0 else 0
        
        result = {
            "compound": max(-1, min(1, compound)),
            "sentiment": "positive" if compound > 0.1 else "negative" if compound < -0.1 else "neutral",
            "confidence": min(0.99, abs(compound) * 0.5 + 0.3),
            "method": "keyword_based",
            "timestamp": datetime.now().isoformat()
        }
        
        self.history.append(result)
        return result
    
    def _neutral_sentiment(self) -> Dict:
        """Return neutral sentiment"""
        return {
            "compound": 0.0,
            "sentiment": "neutral",
            "confidence": 0.5,
            "method": "keyword_based",
            "timestamp": datetime.now().isoformat()
        }
    
    def analyze_multiple_texts(self, texts: List[str]) -> Dict:
        """Analyze sentiment for multiple texts"""
        sentiments = [self.analyze_sentiment(text) for text in texts]
        
        if not sentiments:
            return self._neutral_sentiment()
        
        avg_compound = sum(s["compound"] for s in sentiments) / len(sentiments)
        
        return {
            "compound": avg_compound,
            "sentiment": "positive" if avg_compound > 0.1 else "negative" if avg_compound < -0.1 else "neutral",
            "confidence": sum(s["confidence"] for s in sentiments) / len(sentiments),
            "texts_analyzed": len(sentiments),
            "method": "keyword_based",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_sentiment_trend(self, window: int = 7) -> Dict:
        """Get sentiment trend"""
        if not self.history:
            return {
                "trend": "neutral",
                "recent_sentiment": "no data",
                "data_points": 0
            }
        
        recent = self.history[-window:] if len(self.history) >= window else self.history
        compounds = [s["compound"] for s in recent]
        
        return {
            "trend": "bullish" if sum(compounds) > 0 else "bearish" if sum(compounds) < 0 else "neutral",
            "recent_sentiment": recent[-1]["sentiment"] if recent else "neutral",
            "data_points": len(recent),
            "average": sum(compounds) / len(compounds) if compounds else 0
        }


# Global instance
simple_analyzer = SimpleSentimentAnalyzer()
