"""
Advanced Analytics Module
Provides anomaly detection, technical indicators, backtesting, and RBAC
"""

import numpy as np
from typing import List, Dict

class AnomalyDetector:
    """Detect market anomalies using statistical methods"""
    def __init__(self, threshold=2.5):
        self.threshold = threshold
    
    def detect(self, prices: List[float]) -> Dict:
        if len(prices) < 3:
            return {"anomalies": [], "scores": []}
        
        prices = np.array(prices)
        mean = np.mean(prices)
        std = np.std(prices)
        
        anomalies = []
        scores = []
        for i, price in enumerate(prices):
            z_score = abs((price - mean) / std) if std > 0 else 0
            scores.append(z_score)
            if z_score > self.threshold:
                anomalies.append({
                    "index": i,
                    "value": float(price),
                    "severity": "HIGH" if z_score > 3 else "MEDIUM",
                    "z_score": float(z_score)
                })
        
        return {"anomalies": anomalies, "scores": scores}

class TechnicalIndicators:
    """Calculate technical indicators"""
    @staticmethod
    def sma(prices: List[float], period: int = 20) -> List[float]:
        """Simple Moving Average"""
        if len(prices) < period:
            return []
        return [np.mean(prices[i-period:i]) for i in range(period, len(prices)+1)]
    
    @staticmethod
    def ema(prices: List[float], period: int = 20) -> List[float]:
        """Exponential Moving Average"""
        if len(prices) < period:
            return []
        ema_values = [np.mean(prices[:period])]
        multiplier = 2 / (period + 1)
        for i in range(period, len(prices)):
            ema = (prices[i] - ema_values[-1]) * multiplier + ema_values[-1]
            ema_values.append(ema)
        return ema_values
    
    @staticmethod
    def rsi(prices: List[float], period: int = 14) -> List[float]:
        """Relative Strength Index"""
        if len(prices) < period + 1:
            return []
        
        rsi_values = []
        for i in range(period, len(prices)):
            gains = sum([max(0, prices[j] - prices[j-1]) for j in range(i-period+1, i+1)])
            losses = sum([max(0, prices[j-1] - prices[j]) for j in range(i-period+1, i+1)])
            
            avg_gain = gains / period
            avg_loss = losses / period
            
            rs = avg_gain / avg_loss if avg_loss > 0 else 0
            rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)
        
        return rsi_values
    
    @staticmethod
    def macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9):
        """MACD Indicator"""
        ema_fast = TechnicalIndicators.ema(prices, fast)
        ema_slow = TechnicalIndicators.ema(prices, slow)
        
        if len(ema_fast) < len(ema_slow):
            ema_fast = [None] * (len(ema_slow) - len(ema_fast)) + ema_fast
        else:
            ema_slow = [None] * (len(ema_fast) - len(ema_slow)) + ema_slow
        
        macd_line = [f - s if f and s else None for f, s in zip(ema_fast, ema_slow)]
        macd_line = [x for x in macd_line if x is not None]
        
        signal_line = TechnicalIndicators.ema(macd_line, signal) if macd_line else []
        
        return {"macd": macd_line, "signal": signal_line}
    
    @staticmethod
    def bollinger_bands(prices: List[float], period: int = 20, std_dev: int = 2):
        """Bollinger Bands"""
        sma_values = TechnicalIndicators.sma(prices, period)
        
        bands = []
        for i in range(period, len(prices)+1):
            sma = sma_values[i-period]
            std = np.std(prices[i-period:i])
            upper = sma + (std_dev * std)
            lower = sma - (std_dev * std)
            bands.append({
                "upper": float(upper),
                "middle": float(sma),
                "lower": float(lower)
            })
        
        return bands

class BasicBacktester:
    """Simple backtesting engine"""
    @staticmethod
    def backtest(predictions: List[float], actuals: List[float]) -> Dict:
        """Test predictions against actual values"""
        if len(predictions) != len(actuals):
            return {"error": "Length mismatch"}
        
        correct = sum(1 for p, a in zip(predictions, actuals) if (p > 0 and a > 0) or (p < 0 and a < 0))
        total = len(predictions)
        win_rate = (correct / total * 100) if total > 0 else 0
        
        returns = [a * 0.01 for a in actuals]  # Assume 1% return per correct prediction
        total_return = sum(returns)
        
        return {
            "total_trades": total,
            "win_rate": float(win_rate),
            "total_return": float(total_return),
            "avg_return": float(total_return / total) if total > 0 else 0,
            "sharpe_ratio": float(np.std(returns) if len(returns) > 1 else 0)
        }

class RoleBasedAccessControl:
    """User role management"""
    ROLES = {
        "admin": ["view", "trade", "manage_users", "manage_models"],
        "trader": ["view", "trade"],
        "viewer": ["view"]
    }
    
    @staticmethod
    def has_permission(role: str, action: str) -> bool:
        return action in RoleBasedAccessControl.ROLES.get(role, [])
    
    @staticmethod
    def get_permissions(role: str) -> List[str]:
        return RoleBasedAccessControl.ROLES.get(role, [])
