"""
Advanced Market Anomaly Detection & Risk Scenario Engine
Detects unusual market patterns and generates AI-powered what-if scenarios
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class MarketAnomalyDetector:
    """
    Detects market anomalies using statistical methods and pattern recognition
    """
    
    def __init__(self):
        self.anomaly_types = {
            'volume_spike': 'Unusual trading volume detected',
            'price_jump': 'Abnormal price movement',
            'volatility_surge': 'Extreme volatility detected',
            'trend_reversal': 'Potential trend reversal',
            'divergence': 'Price-indicator divergence',
            'flash_crash': 'Rapid price decline detected',
            'pump_pattern': 'Potential pump pattern detected'
        }
    
    def detect_anomalies(self, sequence_data: np.ndarray, current_price: float) -> Dict:
        """
        Detect multiple types of market anomalies
        
        Args:
            sequence_data: Historical data sequence (seq_len, n_features)
            current_price: Current market price
            
        Returns:
            Dictionary with anomaly detection results
        """
        
        anomalies = []
        risk_score = 0
        warnings = []
        
        # Extract recent data
        recent_data = sequence_data[-10:]  # Last 10 periods
        older_data = sequence_data[:-10] if len(sequence_data) > 10 else sequence_data
        
        # 1. Volume Spike Detection
        if len(sequence_data[0]) > 4:  # Has volume data
            volume_anomaly = self._detect_volume_anomaly(sequence_data)
            if volume_anomaly:
                anomalies.append(volume_anomaly)
                risk_score += 15
        
        # 2. Price Jump Detection
        price_anomaly = self._detect_price_jump(sequence_data)
        if price_anomaly:
            anomalies.append(price_anomaly)
            risk_score += 25
        
        # 3. Volatility Surge
        volatility_anomaly = self._detect_volatility_surge(sequence_data)
        if volatility_anomaly:
            anomalies.append(volatility_anomaly)
            risk_score += 20
        
        # 4. Trend Reversal Pattern
        reversal = self._detect_trend_reversal(sequence_data)
        if reversal:
            anomalies.append(reversal)
            risk_score += 18
        
        # 5. Technical Divergence
        divergence = self._detect_divergence(sequence_data)
        if divergence:
            anomalies.append(divergence)
            risk_score += 12
        
        # 6. Flash Crash Pattern
        flash_crash = self._detect_flash_crash(sequence_data)
        if flash_crash:
            anomalies.append(flash_crash)
            risk_score += 40
            warnings.append("⚠️ CRITICAL: Flash crash pattern detected!")
        
        # Generate warnings based on risk score
        if risk_score > 50:
            warnings.append("🚨 HIGH RISK: Multiple severe anomalies detected")
        elif risk_score > 30:
            warnings.append("⚡ MODERATE RISK: Unusual market behavior")
        elif risk_score > 15:
            warnings.append("⚠️ LOW RISK: Minor anomalies detected")
        
        # Calculate anomaly severity
        severity = 'CRITICAL' if risk_score > 50 else 'HIGH' if risk_score > 30 else 'MODERATE' if risk_score > 15 else 'LOW'
        
        return {
            'anomalies_detected': len(anomalies),
            'anomalies': anomalies,
            'risk_score': min(risk_score, 100),
            'severity': severity,
            'warnings': warnings,
            'is_safe': risk_score < 20,
            'timestamp': datetime.now().isoformat()
        }
    
    def _detect_volume_anomaly(self, data: np.ndarray) -> Optional[Dict]:
        """Detect unusual volume spikes"""
        if len(data[0]) <= 4:
            return None
        
        volumes = data[:, 4]  # Volume column
        recent_vol = volumes[-1]
        avg_vol = np.mean(volumes[:-1])
        std_vol = np.std(volumes[:-1])
        
        # Z-score approach
        if std_vol > 0:
            z_score = (recent_vol - avg_vol) / std_vol
            if abs(z_score) > 3:  # 3 sigma event
                return {
                    'type': 'volume_spike',
                    'severity': 'high' if abs(z_score) > 4 else 'moderate',
                    'description': f'Volume spike detected ({abs(z_score):.1f}σ above normal)',
                    'z_score': float(z_score),
                    'impact': 'High volume indicates strong conviction - potential major move'
                }
        return None  
    
    def _detect_price_jump(self, data: np.ndarray) -> Optional[Dict]:
        """Detect abnormal price movements"""
        prices = data[:, 3]  # Close prices
        
        # Calculate returns
        returns = np.diff(prices) / prices[:-1]
        recent_return = returns[-1] if len(returns) > 0 else 0
        avg_return = np.mean(returns[:-1]) if len(returns) > 1 else 0
        std_return = np.std(returns[:-1]) if len(returns) > 1 else 0.01
        
        if std_return > 0:
            z_score = (recent_return - avg_return) / std_return
            if abs(z_score) > 2.5:
                direction = 'upward' if recent_return > 0 else 'downward'
                return {
                    'type': 'price_jump',
                    'severity': 'high' if abs(z_score) > 3.5 else 'moderate',
                    'description': f'Abnormal {direction} price movement ({abs(z_score):.1f}σ)',
                    'z_score': float(z_score),
                    'impact': f'Unusual {direction} momentum - potential overreaction'
                }
        return None
    
    def _detect_volatility_surge(self, data: np.ndarray) -> Optional[Dict]:
        """Detect extreme volatility"""
        if len(data[0]) <= 22:  # Need volatility column
            return None
        
        volatilities = data[:, 22]  # Volatility column
        current_vol = volatilities[-1]
        avg_vol = np.mean(volatilities[:-5])
        
        if current_vol > avg_vol * 2:
            return {
                'type': 'volatility_surge',
                'severity': 'high' if current_vol > avg_vol * 3 else 'moderate',
                'description': f'Volatility surge: {(current_vol/avg_vol):.1f}x normal levels',
                'multiplier': float(current_vol / avg_vol),
                'impact': 'High volatility increases risk - expect larger price swings'
            }
        return None
    
    def _detect_trend_reversal(self, data: np.ndarray) -> Optional[Dict]:
        """Detect potential trend reversals"""
        if len(data) < 10:
            return None
        
        prices = data[:, 3]
        
        # Check for reversal pattern
        recent_prices = prices[-5:]
        older_prices = prices[-10:-5]
        
        recent_trend = np.polyfit(range(len(recent_prices)), recent_prices, 1)[0]
        older_trend = np.polyfit(range(len(older_prices)), older_prices, 1)[0]
        
        # Opposite trends
        if recent_trend * older_trend < 0 and abs(recent_trend) > abs(older_trend) * 0.5:
            reversal_type = 'bullish' if recent_trend > 0 else 'bearish'
            return {
                'type': 'trend_reversal',
                'severity': 'moderate',
                'description': f'Potential {reversal_type} reversal detected',
                'reversal_type': reversal_type,
                'impact': f'Trend changing from {"-" if older_trend < 0 else "+"} to {"-" if recent_trend < 0 else "+"}'
            }
        return None
    
    def _detect_divergence(self, data: np.ndarray) -> Optional[Dict]:
        """Detect price-indicator divergence"""
        if len(data[0]) <= 13 or len(data) < 10:
            return None
        
        prices = data[-10:, 3]
        rsi = data[-10:, 13]  # RSI column
        
        price_trend = prices[-1] - prices[0]
        rsi_trend = rsi[-1] - rsi[0]
        
        # Bearish divergence: price up, RSI down
        if price_trend > 0 and rsi_trend < -0.05:
            return {
                'type': 'divergence',
                'severity': 'moderate',
                'description': 'Bearish divergence: Price rising but RSI falling',
                'divergence_type': 'bearish',
                'impact': 'Momentum weakening despite price increase - potential reversal'
            }
        
        # Bullish divergence: price down, RSI up
        if price_trend < 0 and rsi_trend > 0.05:
            return {
                'type': 'divergence',
                'severity': 'moderate',
                'description': 'Bullish divergence: Price falling but RSI rising',
                'divergence_type': 'bullish',
                'impact': 'Momentum strengthening despite price decrease - potential recovery'
            }
        
        return None
    
    def _detect_flash_crash(self, data: np.ndarray) -> Optional[Dict]:
        """Detect rapid price decline (flash crash)"""
        if len(data) < 5:
            return None
        
        prices = data[-5:, 3]
        
        # Check for rapid consecutive declines
        declines = 0
        total_decline = 0
        
        for i in range(1, len(prices)):
            change = (prices[i] - prices[i-1]) / prices[i-1]
            if change < -0.02:  # More than 2% decline
                declines += 1
                total_decline += abs(change)
        
        if declines >= 3 and total_decline > 0.08:  # 3+ declines, 8%+ total
            return {
                'type': 'flash_crash',
                'severity': 'critical',
                'description': f'Flash crash pattern: {declines} consecutive declines',
                'total_decline_pct': float(total_decline * 100),
                'impact': 'CRITICAL: Rapid sell-off detected - extreme caution advised'
            }
        
        return None


class RiskScenarioEngine:
    """
    Generates AI-powered what-if scenarios for risk assessment
    """
    
    def __init__(self):
        self.scenarios = []
    
    def generate_scenarios(
        self, 
        current_price: float, 
        predicted_price: float,
        sequence_data: np.ndarray,
        technical_signals: Dict
    ) -> List[Dict]:
        """
        Generate multiple what-if scenarios
        
        Returns:
            List of scenario dictionaries
        """
        
        scenarios = []
        
        # Scenario 1: Best Case
        best_case = self._best_case_scenario(current_price, predicted_price, technical_signals)
        scenarios.append(best_case)
        
        # Scenario 2: Worst Case
        worst_case = self._worst_case_scenario(current_price, predicted_price, technical_signals)
        scenarios.append(worst_case)
        
        # Scenario 3: Most Likely
        most_likely = self._most_likely_scenario(current_price, predicted_price, technical_signals)
        scenarios.append(most_likely)
        
        # Scenario 4: Black Swan Event
        black_swan = self._black_swan_scenario(current_price, sequence_data)
        scenarios.append(black_swan)
        
        # Scenario 5: Market Correction
        correction = self._correction_scenario(current_price, predicted_price)
        scenarios.append(correction)
        
        return scenarios
    
    def _best_case_scenario(self, current: float, predicted: float, signals: Dict) -> Dict:
        """Generate optimistic scenario"""
        
        # Count bullish signals
        bullish_count = sum(1 for s in signals.values() if 'bullish' in str(s.get('strength', '')).lower())
        
        multiplier = 1.5 + (bullish_count * 0.2)
        price_change = predicted - current
        best_price = current + (price_change * multiplier)
        
        return {
            'name': '🚀 Best Case (Bull Run)',
            'probability': '15-20%',
            'target_price': round(best_price, 2),
            'change_pct': round(((best_price - current) / current) * 100, 2),
            'timeframe': '1-3 months',
            'conditions': [
                'All technical indicators align bullish',
                'Market sentiment extremely positive',
                'Volume confirms strong buying pressure',
                'No major negative catalysts'
            ],
            'actions': ['Consider increasing position', 'Set trailing stop-loss', 'Take partial profits at targets']
        }
    
    def _worst_case_scenario(self, current: float, predicted: float, signals: Dict) -> Dict:
        """Generate pessimistic scenario"""
        
        # Count bearish signals
        bearish_count = sum(1 for s in signals.values() if 'bearish' in str(s.get('strength', '')).lower())
        
        multiplier = -1.2 - (bearish_count * 0.15)
        price_change = abs(predicted - current)
        worst_price = current + (price_change * multiplier)
        
        return {
            'name': '📉 Worst Case (Bear Market)',
            'probability': '10-15%',
            'target_price': round(worst_price, 2),
            'change_pct': round(((worst_price - current) / current) * 100, 2),
            'timeframe': '1-2 months',
            'conditions': [
                'Major market correction underway',
                'Technical breakdown confirmed',
                'High volume sell-off',
                'Negative catalyst triggers panic'
            ],
            'actions': ['Consider reducing exposure', 'Implement strict stop-loss', 'Prepare dry powder for recovery']
        }
    
    def _most_likely_scenario(self, current: float, predicted: float, signals: Dict) -> Dict:
        """Generate realistic scenario"""
        
        # Use predicted price as most likely
        change_pct = ((predicted - current) / current) * 100
        
        # Add some uncertainty range
        lower_bound = predicted * 0.95
        upper_bound = predicted * 1.05
        
        return {
            'name': '📊 Most Likely (Base Case)',
            'probability': '50-60%',
            'target_price': round(predicted, 2),
            'range': [round(lower_bound, 2), round(upper_bound, 2)],
            'change_pct': round(change_pct, 2),
            'timeframe': '1-4 weeks',
            'conditions': [
                'Market continues current trend',
                'No major surprises or shocks',
                'Technical indicators mostly aligned',
                'Normal trading volume'
            ],
            'actions': ['Follow trading plan', 'Monitor key support/resistance', 'Stay disciplined']
        }
    
    def _black_swan_scenario(self, current: float, sequence_data: np.ndarray) -> Dict:
        """Generate extreme unexpected event scenario"""
        
        # Calculate historical volatility
        prices = sequence_data[:, 3]
        volatility = np.std(np.diff(prices) / prices[:-1]) if len(prices) > 1 else 0.02
        
        # Extreme move: 3-5 standard deviations
        extreme_move = current * volatility * np.random.choice([-4, -3.5, 3.5, 4])
        black_swan_price = current + extreme_move
        
        return {
            'name': '🦢 Black Swan (Unexpected)',
            'probability': '2-5%',
            'target_price': round(black_swan_price, 2),
            'change_pct': round(((black_swan_price - current) / current) * 100, 2),
            'timeframe': 'Sudden (hours-days)',
            'conditions': [
                'Major unexpected news/event',
                'Geopolitical crisis',
                'Regulatory shock',
                'Company-specific bombshell'
            ],
            'actions': ['Have emergency exit plan', 'Use position sizing', 'Never risk more than you can lose']
        }
    
    def _correction_scenario(self, current: float, predicted: float) -> Dict:
        """Generate market correction scenario"""
        
        # Typical correction: 10-20% pullback
        correction_pct = -0.12  # 12% correction
        correction_price = current * (1 + correction_pct)
        
        return {
            'name': '⚠️ Correction (Pullback)',
            'probability': '20-25%',
            'target_price': round(correction_price, 2),
            'change_pct': round(correction_pct * 100, 2),
            'timeframe': '2-6 weeks',
            'conditions': [
                'Market overbought conditions',
                'Profit-taking by institutions',
                'Technical resistance levels',
                'Healthy consolidation'
            ],
            'actions': ['View as buying opportunity', 'Average down strategically', 'Wait for reversal signals']
        }


def analyze_market_health(sequence_data: np.ndarray, current_price: float) -> Dict:
    """
    Comprehensive market health analysis combining anomaly detection and scenarios
    """
    
    detector = MarketAnomalyDetector()
    scenario_engine = RiskScenarioEngine()
    
    # Detect anomalies
    anomaly_results = detector.detect_anomalies(sequence_data, current_price)
    
    # Calculate market health score (0-100)
    health_score = 100 - anomaly_results['risk_score']
    
    # Determine market condition
    if health_score >= 80:
        condition = 'HEALTHY 💚'
        description = 'Market showing normal, stable behavior'
    elif health_score >= 60:
        condition = 'CAUTIOUS 🟡'
        description = 'Some unusual patterns detected, monitor closely'
    elif health_score >= 40:
        condition = 'UNSTABLE 🟠'
        description = 'Multiple anomalies present, elevated risk'
    else:
        condition = 'DANGEROUS 🔴'
        description = 'Severe anomalies detected, extreme caution required'
    
    return {
        'health_score': health_score,
        'condition': condition,
        'description': description,
        'anomaly_analysis': anomaly_results,
        'timestamp': datetime.now().isoformat()
    }
