"""
REST API Client & Utilities
Provides simple functions to call the REST API
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class AIMarketAPIClient:
    """Simple client for AI Market Predictor REST API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize API client
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def analyze(self, symbol: str, current_price: float, 
                predicted_price: float, confidence: float = 0.7) -> Dict[str, Any]:
        """
        Analyze a stock via API
        
        Args:
            symbol: Stock symbol
            current_price: Current price
            predicted_price: Predicted price
            confidence: Model confidence (0-1)
            
        Returns:
            Analysis response
        """
        url = f"{self.base_url}/api/ai/analyze"
        payload = {
            "symbol": symbol,
            "current_price": current_price,
            "predicted_price": predicted_price,
            "confidence": confidence
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_analysis(self, symbol: str) -> Dict[str, Any]:
        """
        Get cached analysis for a symbol
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Cached analysis or error
        """
        url = f"{self.base_url}/api/ai/analyze/{symbol}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def chat(self, message: str) -> str:
        """
        Chat with AI analyst
        
        Args:
            message: User message
            
        Returns:
            AI response
        """
        url = f"{self.base_url}/api/ai/chat"
        payload = {"message": message}
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict]:
        """
        Get conversation history
        
        Args:
            limit: Number of recent conversations
            
        Returns:
            List of conversation turns
        """
        url = f"{self.base_url}/api/ai/conversation-history"
        response = self.session.get(url, params={"limit": limit})
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    
    def get_market_summary(self, symbols: List[str]) -> Dict[str, Any]:
        """
        Get market summary for symbols
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            Market summary
        """
        url = f"{self.base_url}/api/ai/market-summary"
        payload = {"symbols": symbols}
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_alerts(self, symbols: List[str]) -> List[Dict]:
        """
        Get trading alerts
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            List of trading alerts
        """
        url = f"{self.base_url}/api/ai/alerts"
        response = self.session.get(url, params={"symbols": symbols})
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    
    def get_performance(self) -> Dict[str, Any]:
        """
        Get system performance metrics
        
        Returns:
            Performance metrics
        """
        url = f"{self.base_url}/api/ai/performance"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("data", {})
    
    def export_analysis(self, filepath: str, format: str = "json") -> Dict[str, Any]:
        """
        Export analysis data
        
        Args:
            filepath: Where to save
            format: Export format (json or csv)
            
        Returns:
            Export status
        """
        url = f"{self.base_url}/api/ai/export"
        response = self.session.post(url, params={
            "filepath": filepath,
            "format": format
        })
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> bool:
        """
        Check API health
        
        Returns:
            True if healthy
        """
        try:
            url = f"{self.base_url}/api/ai/health"
            response = self.session.get(url, timeout=5)
            return response.json().get("status") == "healthy"
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get system information
        
        Returns:
            System information
        """
        url = f"{self.base_url}/api/ai/info"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()


# Convenience functions
def create_client(base_url: str = "http://localhost:8000") -> AIMarketAPIClient:
    """Create an API client"""
    return AIMarketAPIClient(base_url)


def quick_analyze(symbol: str, current: float, predicted: float) -> str:
    """Quick analysis with one function"""
    client = AIMarketAPIClient()
    result = client.analyze(symbol, current, predicted)
    if result.get("status") == "success":
        signal = result["data"]["signals"]["signal"]
        target = result["data"]["signals"]["price_target"]
        return f"{symbol}: {signal} (Target: ${target:.2f})"
    return "Error analyzing"


def quick_chat(message: str) -> str:
    """Quick chat with one function"""
    client = AIMarketAPIClient()
    return client.chat(message)


def quick_alerts(symbols: List[str]) -> List[str]:
    """Quick alerts with one function"""
    client = AIMarketAPIClient()
    alerts = client.get_alerts(symbols)
    return [f"{a['symbol']}: {a['signal']}" for a in alerts]


# Demo usage
if __name__ == "__main__":
    print("\n" + "="*60)
    print("AI Market Predictor - REST API Client Demo")
    print("="*60 + "\n")
    
    try:
        client = AIMarketAPIClient()
        
        # Check health
        print("[1/6] Checking API health...")
        if client.health_check():
            print("     OK - API is healthy\n")
        else:
            print("     FAIL - API is not responding")
            print("     Make sure the server is running:")
            print("     python run_local_server.py\n")
            exit(1)
        
        # Get system info
        print("[2/6] Getting system information...")
        info = client.get_info()
        print(f"     System: {info.get('system')}")
        print(f"     Version: {info.get('version')}\n")
        
        # Analyze stock
        print("[3/6] Analyzing stock (AAPL)...")
        result = client.analyze("AAPL", 150.75, 158.50, confidence=0.82)
        if result.get("status") == "success":
            signal = result["data"]["signals"]["signal"]
            target = result["data"]["signals"]["price_target"]
            print(f"     Signal: {signal}")
            print(f"     Target: ${target:.2f}\n")
        
        # Chat
        print("[4/6] Chatting with AI...")
        response = client.chat("What is the market outlook?")
        print(f"     Response: {response[:100]}...\n")
        
        # Get alerts
        print("[5/6] Getting trading alerts...")
        alerts = client.get_alerts(["AAPL", "MSFT"])
        print(f"     Found {len(alerts)} alerts\n")
        
        # Performance
        print("[6/6] Getting performance metrics...")
        perf = client.get_performance()
        print(f"     Total analyses: {perf.get('total_analyses', 0)}")
        print(f"     Average confidence: {perf.get('average_confidence', 0):.0%}\n")
        
        print("="*60)
        print("All API tests passed!")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to API server")
        print("Make sure the server is running:")
        print("  python run_local_server.py\n")
    except Exception as e:
        print(f"ERROR: {e}\n")
        import traceback
        traceback.print_exc()
