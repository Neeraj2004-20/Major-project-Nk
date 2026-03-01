"""
AI/LLM Integration Module
Integrates LLM analysis with existing prediction system
Provides unified interface for market intelligence
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

# Lazy imports - will be loaded when needed
LLMMarketAnalyst = None
MarketAnalysisInput = None
create_analyst = None
AIMarketConversationAgent = None
create_conversation_agent = None


def _ensure_imports():
    """Load heavy dependencies lazily"""
    global LLMMarketAnalyst, MarketAnalysisInput, create_analyst
    global AIMarketConversationAgent, create_conversation_agent
    
    if LLMMarketAnalyst is None:
        try:
            import numpy as np
            from llm_market_analyst import LLMMarketAnalyst as LMA, MarketAnalysisInput as MAI, create_analyst as ca
            from ai_conversation import AIMarketConversationAgent as AMCA, create_conversation_agent as cca
            LLMMarketAnalyst = LMA
            MarketAnalysisInput = MAI
            create_analyst = ca
            AIMarketConversationAgent = AMCA
            create_conversation_agent = cca
        except ImportError as e:
            logger.warning(f"Could not load AI modules: {e}")
            raise


class AIMarketIntelligence:
    """
    Unified AI system combining LLM analysis, sentiment analysis,
    and prediction models
    """
    
    def __init__(self, analyst: 'LLMMarketAnalyst' = None, 
                 conversation_agent: 'AIMarketConversationAgent' = None):
        """
        Initialize AI Market Intelligence
        
        Args:
            analyst: LLMMarketAnalyst instance (auto-creates if None)
            conversation_agent: AIMarketConversationAgent (auto-creates if None)
        """
        _ensure_imports()
        self.analyst = analyst or create_analyst()
        self.conversation_agent = conversation_agent or create_conversation_agent()
        self.analysis_cache = {}
        self.insights_log = []
        
    def analyze_stock(self, 
                     symbol: str,
                     current_price: float,
                     predicted_price: float,
                     sentiment_analyzer=None,
                     technical_indicators: Dict = None,
                     news_headlines: List[str] = None,
                     confidence: float = 0.7) -> Dict:
        """
        Comprehensive stock analysis combining ML and LLM
        
        Args:
            symbol: Stock symbol
            current_price: Current price
            predicted_price: Predicted price from ML model
            sentiment_analyzer: Sentiment analyzer instance
            technical_indicators: Dict of technical indicators
            news_headlines: List of relevant news headlines
            confidence: Model confidence
            
        Returns:
            Complete analysis report
        """
        
        # Get sentiment scores
        sentiment_score = 0
        top_sentiments = []
        if sentiment_analyzer and news_headlines:
            try:
                sentiments = sentiment_analyzer.analyze_multiple(news_headlines)
                sentiment_score = np.mean([s['score'] for s in sentiments])
                top_sentiments = sentiments[:3]
            except:
                sentiment_score = 0
        
        # Prepare analysis input
        analysis_input = MarketAnalysisInput(
            symbol=symbol,
            current_price=current_price,
            predicted_price=predicted_price,
            sentiment_score=sentiment_score,
            technical_indicators=technical_indicators or {},
            news_headlines=news_headlines or [],
            historical_data={},
            confidence=confidence
        )
        
        # Get LLM analysis
        analysis = self.analyst.analyze(analysis_input)
        
        # Enhance with conversation-ready format
        analysis["conversational_summary"] = self._create_conversational_summary(
            analysis, symbol, sentiment_score
        )
        
        # Cache analysis
        self.analysis_cache[symbol] = analysis
        
        # Log insights
        self.insights_log.append({
            "timestamp": datetime.now().isoformat(),
            "symbol": symbol,
            "signal": analysis["signals"]["signal"],
            "confidence": confidence
        })
        
        return analysis
    
    def _create_conversational_summary(self, analysis: Dict, symbol: str, 
                                      sentiment_score: float) -> str:
        """Create conversational summary of analysis"""
        
        signals = analysis["signals"]
        
        summary = f"""
{symbol} Trading Analysis Summary:
- Signal: {signals['signal']} (Strength: {signals['strength']:.0%})
- Target: ${signals['price_target']:.2f}
- Entry: ${signals['entry_price']:.2f}
- Stop Loss: ${signals['stop_loss']:.2f}
- Risk Level: {signals['risk_level']}
"""
        return summary
    
    def get_market_summary(self, symbols: List[str]) -> Dict:
        """Get summary across multiple stocks"""
        
        market_data = [
            self.analysis_cache.get(sym) 
            for sym in symbols 
            if sym in self.analysis_cache
        ]
        
        if not market_data:
            return {"error": "No analysis data available"}
        
        summary = self.analyst.get_market_summary(market_data)
        
        # Add insights
        summary["insights"] = self._generate_market_insights(market_data)
        summary["recommendations"] = self._generate_portfolio_recommendations(market_data)
        
        return summary
    
    def _generate_market_insights(self, analyses: List[Dict]) -> List[str]:
        """Generate market insights from multiple analyses"""
        
        insights = []
        
        # Calculate statistics
        signals = [a["signals"]["signal"] for a in analyses]
        buy_count = signals.count("BUY")
        sell_count = signals.count("SELL")
        strengths = [a["signals"]["strength"] for a in analyses]
        avg_strength = np.mean(strengths) if strengths else 0
        
        # Generate insights
        if buy_count > sell_count:
            insights.append(f"📈 Bullish bias with {buy_count} buy signals detected")
        elif sell_count > buy_count:
            insights.append(f"📉 Bearish bias with {sell_count} sell signals detected")
        
        if avg_strength > 0.7:
            insights.append("💪 Strong signal strength across the board")
        elif avg_strength < 0.3:
            insights.append("⚠️ Weak signals - wait for clearer patterns")
        
        # Volatility insight
        volatilities = [a["market_indicators"].get("volatility", 0) for a in analyses]
        if volatilities:
            avg_vol = np.mean(volatilities)
            if avg_vol > 0.02:
                insights.append("⚡ High volatility - manage position sizes")
            else:
                insights.append("😌 Low volatility - stable market conditions")
        
        return insights
    
    def _generate_portfolio_recommendations(self, analyses: List[Dict]) -> List[str]:
        """Generate portfolio-level recommendations"""
        
        recommendations = [
            "✅ Diversify across multiple sectors",
            "✅ Use stop losses on all positions",
            "✅ Don't risk more than 2% per trade",
            "✅ Review positions weekly",
            "✅ Keep profits locked in with trailing stops"
        ]
        
        # Add specific recommendations based on analysis
        signals = [a["signals"]["signal"] for a in analyses]
        if signals.count("BUY") >= 3:
            recommendations.append("🚀 Market momentum is strong - consider increasing exposure")
        
        high_risk = sum(1 for a in analyses if a["signals"]["risk_level"] == "HIGH")
        if high_risk > len(analyses) / 2:
            recommendations.append("⚠️ High risk environment - reduce position sizes")
        
        return recommendations
    
    def chat(self, user_message: str) -> str:
        """
        Chat with AI market analyst
        
        Args:
            user_message: User's question or command
            
        Returns:
            Assistant's response
        """
        # Update market data for conversation
        self.conversation_agent.set_market_data(self.analysis_cache)
        
        # Get response
        response = self.conversation_agent.chat(user_message)
        
        return response
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_agent.get_conversation_history()
    
    def get_trading_alerts(self, symbols: List[str]) -> List[Dict]:
        """Get trading alerts for symbols"""
        
        alerts = []
        
        for symbol in symbols:
            if symbol not in self.analysis_cache:
                continue
            
            analysis = self.analysis_cache[symbol]
            signals = analysis["signals"]
            
            if signals["signal"] != "HOLD":
                alert = {
                    "symbol": symbol,
                    "signal": signals["signal"],
                    "strength": signals["strength"],
                    "price_target": signals["price_target"],
                    "confidence": analysis["confidence"],
                    "timestamp": analysis["timestamp"],
                    "action": f"{signals['signal']} at ${signals['entry_price']:.2f}",
                    "take_profit": signals["profit_target"],
                    "stop_loss": signals["stop_loss"]
                }
                alerts.append(alert)
        
        return sorted(alerts, key=lambda x: x["strength"], reverse=True)
    
    def export_analysis(self, filepath: str, format: str = "json"):
        """
        Export analysis to file
        
        Args:
            filepath: Path to save file
            format: 'json' or 'csv'
        """
        if format == "json":
            data = {
                "analyses": self.analysis_cache,
                "insights_log": self.insights_log,
                "conversation_history": self.conversation_agent.get_conversation_history(),
                "exported_at": datetime.now().isoformat()
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        
        logger.info(f"Analysis exported to {filepath}")
    
    def import_market_data(self, filepath: str):
        """Import market data from file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            logger.info(f"Imported market data from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Error importing data: {e}")
            return None
    
    def get_performance_metrics(self) -> Dict:
        """Get system performance metrics"""
        import numpy as np
        
        if not self.insights_log:
            return {"error": "No analysis history"}
        
        signals = [log["signal"] for log in self.insights_log]
        buy_count = signals.count("BUY")
        sell_count = signals.count("SELL")
        hold_count = signals.count("HOLD")
        
        metrics = {
            "total_analyses": len(self.insights_log),
            "buy_signals": buy_count,
            "sell_signals": sell_count,
            "hold_signals": hold_count,
            "buy_ratio": buy_count / len(signals) if signals else 0,
            "average_confidence": np.mean([log.get("confidence", 0.5) 
                                          for log in self.insights_log]),
            "unique_symbols": len(self.analysis_cache)
        }
        
        return metrics


def create_ai_intelligence(analyst_type: str = "auto") -> AIMarketIntelligence:
    """
    Create AI Market Intelligence system
    
    Args:
        analyst_type: Type of LLM analyst to use
        
    Returns:
        AIMarketIntelligence instance
    """
    _ensure_imports()
    analyst = create_analyst(analyst_type)
    conversation = create_conversation_agent()
    return AIMarketIntelligence(analyst, conversation)
