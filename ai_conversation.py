"""
AI Conversation Module
Enables conversational interaction with the market predictor
Provides natural language interface to market data and predictions
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

try:
    from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class ConversationTurn:
    """Single turn in conversation"""
    user_message: str
    assistant_response: str
    timestamp: str
    symbols_mentioned: List[str]
    intent: str  # 'analyze', 'predict', 'sentiment', 'signal', 'help'


class AIMarketConversationAgent:
    """
    Conversational AI system for stock market analysis
    Maintains conversation history and context
    """
    
    def __init__(self, model_name: str = "distilgpt2"):
        """Initialize conversation agent"""
        self.model_name = model_name
        self.conversation_history: List[ConversationTurn] = []
        self.context = {}
        self.market_data = None
        
        self._init_model()
        
    def _init_model(self):
        """Initialize language model"""
        try:
            if HF_AVAILABLE:
                logger.info(f"Initializing conversation model: {self.model_name}")
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
                logger.info("✓ Conversation model loaded")
        except Exception as e:
            logger.warning(f"Model initialization failed: {e}")
            self.model = None
            self.tokenizer = None
    
    def set_market_data(self, market_data: Dict):
        """Set current market data for context"""
        self.market_data = market_data
    
    def chat(self, user_message: str) -> str:
        """
        Process user message and generate response
        
        Args:
            user_message: User's query or command
            
        Returns:
            Assistant's response
        """
        # Parse user intent
        intent, symbols = self._parse_intent(user_message)
        
        # Generate contextual response
        if intent == "analyze":
            response = self._handle_analyze(user_message, symbols)
        elif intent == "predict":
            response = self._handle_predict(user_message, symbols)
        elif intent == "sentiment":
            response = self._handle_sentiment(user_message, symbols)
        elif intent == "signal":
            response = self._handle_signal(user_message, symbols)
        elif intent == "help":
            response = self._handle_help()
        else:
            response = self._generate_general_response(user_message)
        
        # Store in history
        turn = ConversationTurn(
            user_message=user_message,
            assistant_response=response,
            timestamp=datetime.now().isoformat(),
            symbols_mentioned=symbols,
            intent=intent
        )
        self.conversation_history.append(turn)
        
        return response
    
    def _parse_intent(self, message: str) -> Tuple[str, List[str]]:
        """Parse user intent and extract stock symbols"""
        
        message_lower = message.lower()
        symbols = self._extract_symbols(message)
        
        if any(word in message_lower for word in ["analyze", "analysis", "how", "what"]):
            intent = "analyze"
        elif any(word in message_lower for word in ["predict", "forecast", "expect", "will"]):
            intent = "predict"
        elif any(word in message_lower for word in ["sentiment", "news", "opinion", "mood"]):
            intent = "sentiment"
        elif any(word in message_lower for word in ["signal", "buy", "sell", "trade"]):
            intent = "signal"
        elif any(word in message_lower for word in ["help", "what can", "how to", "guide"]):
            intent = "help"
        else:
            intent = "general"
        
        return intent, symbols
    
    def _extract_symbols(self, message: str) -> List[str]:
        """Extract stock symbols from message"""
        
        common_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NFLX", "NVDA",
                         "RELIANCE", "TCS", "INFY", "WIPRO", "ICICIBANK", "SBIN"]
        
        symbols = [symbol for symbol in common_symbols if symbol in message.upper()]
        return symbols
    
    def _handle_analyze(self, message: str, symbols: List[str]) -> str:
        """Handle analyze request"""
        
        if not symbols:
            return "I'd be happy to analyze a stock for you! Please mention the stock symbol (e.g., AAPL, TCS, RELIANCE)."
        
        symbol = symbols[0]
        
        if not self.market_data or symbol not in self.market_data:
            return f"I don't have current data for {symbol}. Please load market data first."
        
        data = self.market_data[symbol]
        
        analysis = f"""
**Analysis for {symbol}:**

📊 **Current Status:**
- Price: ${data.get('price', 'N/A')}
- 52-Week Range: {data.get('range', 'N/A')}
- Market Cap: {data.get('market_cap', 'N/A')}

📈 **Technical Signals:**
- Trend: {data.get('trend', 'Unknown')}
- Momentum: {data.get('momentum', 'Neutral')}
- Key Levels: {data.get('key_levels', 'N/A')}

📰 **Market Sentiment:**
- Sentiment Score: {data.get('sentiment', 'Neutral')}
- Recent News Impact: {data.get('news_impact', 'Neutral')}

💡 **Recommendation:**
{data.get('recommendation', 'Monitor for further signals')}

Would you like me to dive deeper into any specific aspect?
"""
        return analysis
    
    def _handle_predict(self, message: str, symbols: List[str]) -> str:
        """Handle prediction request"""
        
        if not symbols:
            return "Which stock would you like me to predict? (e.g., AAPL, TCS, RELIANCE)"
        
        symbol = symbols[0]
        
        if not self.market_data or symbol not in self.market_data:
            return f"I don't have prediction data for {symbol} yet."
        
        data = self.market_data[symbol]
        
        prediction = f"""
**Price Prediction for {symbol}:**

🎯 **Next Period Forecast:**
- Expected Price: ${data.get('predicted_price', 'N/A')}
- Confidence: {data.get('confidence', 'N/A')}
- Expected Move: {data.get('expected_move', 'N/A')}

⏱️ **Time Horizon:**
- Short-term (1-5 days): {data.get('short_term', 'Neutral')}
- Medium-term (1-3 months): {data.get('medium_term', 'Neutral')}
- Long-term (3+ months): {data.get('long_term', 'Neutral')}

⚠️ **Key Risks:**
{data.get('risks', '- Monitor for unexpected events')}

**Remember:** Predictions are probabilistic. Always use proper risk management!
"""
        return prediction
    
    def _handle_sentiment(self, message: str, symbols: List[str]) -> str:
        """Handle sentiment analysis request"""
        
        if not symbols:
            return "Which stock's sentiment would you like to know about?"
        
        symbol = symbols[0]
        
        sentiment_response = f"""
**Sentiment Analysis for {symbol}:**

📰 **Recent Headlines:**
- Positive mentions: {self.market_data.get(symbol, {}).get('positive_mentions', 'N/A')}
- Negative mentions: {self.market_data.get(symbol, {}).get('negative_mentions', 'N/A')}
- Neutral mentions: {self.market_data.get(symbol, {}).get('neutral_mentions', 'N/A')}

😊 **Overall Sentiment:** {self.market_data.get(symbol, {}).get('overall_sentiment', 'Neutral')}

🔍 **Key Topics:**
- {self.market_data.get(symbol, {}).get('topic_1', 'News topic')}
- {self.market_data.get(symbol, {}).get('topic_2', 'News topic')}

🎯 **Market Impact:**
{self.market_data.get(symbol, {}).get('market_impact', 'Sentiment appears neutral')}
"""
        return sentiment_response
    
    def _handle_signal(self, message: str, symbols: List[str]) -> str:
        """Handle trading signal request"""
        
        if not symbols:
            return "Which stock's trading signal would you like to know?"
        
        symbol = symbols[0]
        
        signal = self.market_data.get(symbol, {}).get('trading_signal', 'HOLD')
        
        signal_response = f"""
**Trading Signal for {symbol}:**

🚀 **Signal: {signal}**

Entry Strategy:
- Entry Price: {self.market_data.get(symbol, {}).get('entry_price', 'Current Market')}
- Position Size: Start small, average in on dips
- Stop Loss: {self.market_data.get(symbol, {}).get('stop_loss', 'Below key support')}

📊 **Exit Targets:**
- Target 1: {self.market_data.get(symbol, {}).get('target1', 'Untested')}
- Target 2: {self.market_data.get(symbol, {}).get('target2', 'Untested')}
- Target 3: {self.market_data.get(symbol, {}).get('target3', 'Untested')}

⚡ **Time Frame:** 
{self.market_data.get(symbol, {}).get('timeframe', 'Multiple days')}

💼 **Risk Management:**
- Position size based on your risk tolerance
- Use stop losses
- Take profits at intervals
- Diversify portfolio

Always remember: Past performance doesn't guarantee future results!
"""
        return signal_response
    
    def _handle_help(self) -> str:
        """Handle help request"""
        
        help_text = """
**AI Market Analyst - How to Use:**

I can help you with:

1️⃣ **Analysis** - Ask about market conditions
   - "Analyze AAPL"
   - "What's happening with TCS?"
   - "Give me analysis for RELIANCE"

2️⃣ **Predictions** - Get price forecasts
   - "What's the prediction for MSFT?"
   - "Where will GOOGL go?"
   - "Forecast for TSLA"

3️⃣ **Sentiment** - Understand market mood
   - "What's the sentiment for NFLX?"
   - "Show me news sentiment for INFY"
   - "Market mood for WIPRO?"

4️⃣ **Signals** - Get trading recommendations
   - "Buy or sell AMZN?"
   - "Trading signal for META"
   - "Should I trade NVDA?"

5️⃣ **Portfolio Insights** - Broader analysis
   - "Compare these stocks"
   - "Best performing today?"
   - "Market summary"

Just type your question naturally, and I'll help!
"""
        return help_text
    
    def _generate_general_response(self, message: str) -> str:
        """Generate response for general queries"""
        
        general_responses = {
            "hi": "Hello! I'm your AI market analyst. Ask me about any stock analysis, predictions, or trading signals!",
            "hello": "Hi there! Ready to analyze some stocks? Ask me about predictions, sentiment, or trading signals!",
            "thanks": "You're welcome! Feel free to ask more questions about the markets!",
            "bye": "Goodbye! Good luck with your trading!",
        }
        
        for key, response in general_responses.items():
            if key in message.lower():
                return response
        
        return "I can help you analyze stocks, get predictions, understand sentiment, and find trading signals. What would you like to know?"
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        
        return [
            {
                "user": turn.user_message,
                "assistant": turn.assistant_response,
                "timestamp": turn.timestamp,
                "intent": turn.intent
            }
            for turn in self.conversation_history[-limit:]
        ]
    
    def save_conversation(self, filepath: str):
        """Save conversation to file"""
        
        data = {
            "history": self.get_conversation_history(limit=None),
            "total_turns": len(self.conversation_history),
            "saved_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Conversation saved to {filepath}")
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


def create_conversation_agent() -> AIMarketConversationAgent:
    """Create a conversation agent"""
    return AIMarketConversationAgent()
