"""
AI System Initialization Module
Simple one-line setup for LLM integration
"""

import logging
import os
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AISystemInitializer:
    """Simple initialization interface for AI systems"""
    
    _instance = None
    _initialized = False
    
    def __init__(self):
        self.ai = None
        self.conversation = None
        self.analyst = None
    
    @classmethod
    def get_instance(cls):
        """Get singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def initialize(cls, backend: str = "auto"):
        """
        Initialize AI system with one line of code
        
        Args:
            backend: 'auto', 'huggingface', 'ollama', or 'anthropic'
            
        Returns:
            AIMarketIntelligence instance
        """
        instance = cls.get_instance()
        
        if not cls._initialized:
            try:
                logger.info(f"Initializing AI system with backend: {backend}")
                
                from ai_llm_integration import create_ai_intelligence
                
                instance.ai = create_ai_intelligence(backend)
                instance.conversation = instance.ai.conversation_agent
                instance.analyst = instance.ai.analyst
                
                cls._initialized = True
                logger.info("✓ AI system initialized successfully")
                
            except Exception as e:
                logger.error(f"Failed to initialize AI system: {e}")
                raise
        
        return instance.ai
    
    @classmethod
    def analyze(cls, symbol: str, current_price: float, 
                predicted_price: float, confidence: float = 0.7):
        """Analyze stock with one function call"""
        if not cls._initialized:
            cls.initialize()
        
        instance = cls.get_instance()
        return instance.ai.analyze_stock(
            symbol=symbol,
            current_price=current_price,
            predicted_price=predicted_price,
            confidence=confidence
        )
    
    @classmethod
    def chat(cls, message: str) -> str:
        """Chat with AI with one function call"""
        if not cls._initialized:
            cls.initialize()
        
        instance = cls.get_instance()
        return instance.ai.chat(message)
    
    @classmethod
    def get_alerts(cls, symbols: list):
        """Get trading alerts"""
        if not cls._initialized:
            cls.initialize()
        
        instance = cls.get_instance()
        return instance.ai.get_trading_alerts(symbols)


# ============================================
# Simple API for Quick Usage
# ============================================

def init_ai(backend: str = "auto"):
    """Initialize AI system"""
    return AISystemInitializer.initialize(backend)


def ai_analyze(symbol: str, current_price: float, 
               predicted_price: float, confidence: float = 0.7):
    """Quick analysis"""
    return AISystemInitializer.analyze(symbol, current_price, predicted_price, confidence)


def ai_chat(message: str) -> str:
    """Quick chat"""
    return AISystemInitializer.chat(message)


def ai_alerts(symbols: list):
    """Get alerts"""
    return AISystemInitializer.get_alerts(symbols)


# ============================================
# Usage Examples
# ============================================

if __name__ == "__main__":
    print("AI System Initializer")
    print("=" * 50)
    
    # Example 1: Initialize
    print("\n1. Initializing AI system...")
    ai = init_ai()
    print("✓ AI system ready")
    
    # Example 2: Quick analysis
    print("\n2. Quick stock analysis...")
    result = ai_analyze("AAPL", 150.75, 158.50, confidence=0.82)
    print(f"Signal: {result['signals']['signal']}")
    print(f"Target: ${result['signals']['price_target']:.2f}")
    
    # Example 3: Chat
    print("\n3. Chat with AI...")
    response = ai_chat("What's happening with AAPL?")
    print(f"Response: {response[:200]}...")
    
    # Example 4: Alerts
    print("\n4. Get trading alerts...")
    alerts = ai_alerts(["AAPL", "MSFT"])
    print(f"Found {len(alerts)} alerts")
    
    print("\n" + "=" * 50)
    print("All examples completed successfully!")
