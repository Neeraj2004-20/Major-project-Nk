"""
AI Explainer Module - Generates Natural Language Explanations
Converts attention weights, technical indicators, and model predictions into human-readable insights
"""

import numpy as np
import torch
from typing import Dict, List, Tuple, Optional

class AIExplainer:
    """
    Explainable AI module that generates natural language explanations
    for transformer-based market predictions
    """
    
    def __init__(self):
        self.feature_names = [
            'Open', 'High', 'Low', 'Close', 'Volume',
            'SMA_5', 'SMA_10', 'SMA_20', 'EMA_12', 'EMA_26',
            'MACD', 'MACD_Signal', 'MACD_Hist',
            'RSI', 'BB_Middle', 'BB_Upper', 'BB_Lower', 'BB_Width',
            'Momentum', 'ROC', 'Volume_SMA', 'Volume_Ratio',
            'Volatility', 'Daily_Range', 'Daily_Return', 'ATR'
        ]
    
    def explain_prediction(
        self,
        prediction: float,
        current_price: float,
        sequence_data: np.ndarray,
        attention_weights: Optional[np.ndarray] = None,
        confidence: Optional[float] = None
    ) -> Dict[str, any]:
        """
        Generate comprehensive explanation for a prediction
        
        Args:
            prediction: Predicted next price
            current_price: Current/last known price
            sequence_data: Input sequence (seq_len, n_features)
            attention_weights: Attention weights from transformer (optional)
            confidence: Model confidence score (optional)
            
        Returns:
            Dictionary containing explanation components
        """
        
        # Calculate prediction metrics
        price_change = prediction - current_price
        price_change_pct = (price_change / current_price) * 100
        direction = "BULLISH 📈" if price_change > 0 else "BEARISH 📉" if price_change < 0 else "NEUTRAL ➡️"
        
        # Analyze technical indicators from latest data
        latest_data = sequence_data[-1]
        technical_analysis = self._analyze_technical_indicators(latest_data)
        
        # Analyze attention patterns
        attention_insights = self._analyze_attention(attention_weights) if attention_weights is not None else None
        
        # Generate natural language explanation
        explanation = self._generate_explanation(
            prediction, current_price, price_change_pct, 
            direction, technical_analysis, attention_insights, confidence
        )
        
        # Get key factors
        key_factors = self._identify_key_factors(technical_analysis, attention_insights)
        
        return {
            'summary': explanation,
            'direction': direction,
            'price_change': round(price_change, 2),
            'price_change_pct': round(price_change_pct, 2),
            'predicted_price': round(prediction, 2),
            'current_price': round(current_price, 2),
            'confidence': confidence,
            'technical_signals': technical_analysis,
            'attention_insights': attention_insights,
            'key_factors': key_factors,
            'risk_level': self._assess_risk(technical_analysis)
        }
    
    def _analyze_technical_indicators(self, latest_data: np.ndarray) -> Dict[str, any]:
        """Analyze technical indicators and generate signals"""
        
        # Ensure we have enough features
        n_features = min(len(latest_data), len(self.feature_names))
        
        indicators = {}
        
        # RSI Analysis (typically index 13)
        if n_features > 13:
            rsi = latest_data[13]
            rsi_denorm = rsi * 100  # Approximate denormalization
            
            if rsi_denorm < 30:
                rsi_signal = "OVERSOLD - Strong Buy Signal"
                rsi_strength = "strong_bullish"
            elif rsi_denorm < 45:
                rsi_signal = "Moderately Oversold - Buy Signal"
                rsi_strength = "bullish"
            elif rsi_denorm > 70:
                rsi_signal = "OVERBOUGHT - Strong Sell Signal"
                rsi_strength = "strong_bearish"
            elif rsi_denorm > 55:
                rsi_signal = "Moderately Overbought - Sell Signal"
                rsi_strength = "bearish"
            else:
                rsi_signal = "Neutral Range"
                rsi_strength = "neutral"
            
            indicators['RSI'] = {
                'value': round(rsi, 4),
                'signal': rsi_signal,
                'strength': rsi_strength
            }
        
        # MACD Analysis (indices 10-12)
        if n_features > 12:
            macd = latest_data[10]
            macd_signal = latest_data[11]
            macd_hist = latest_data[12]
            
            if macd_hist > 0.01:
                macd_signal_text = "Bullish Crossover - Momentum Increasing"
                macd_strength = "bullish"
            elif macd_hist < -0.01:
                macd_signal_text = "Bearish Crossover - Momentum Decreasing"
                macd_strength = "bearish"
            else:
                macd_signal_text = "No Clear Signal"
                macd_strength = "neutral"
            
            indicators['MACD'] = {
                'histogram': round(macd_hist, 4),
                'signal': macd_signal_text,
                'strength': macd_strength
            }
        
        # Moving Average Crossover (SMA_5 vs SMA_20)
        if n_features > 7:
            sma_5 = latest_data[5]
            sma_20 = latest_data[7]
            
            if sma_5 > sma_20:
                ma_signal = "Golden Cross Pattern - Bullish Trend"
                ma_strength = "bullish"
            elif sma_5 < sma_20:
                ma_signal = "Death Cross Pattern - Bearish Trend"
                ma_strength = "bearish"
            else:
                ma_signal = "Sideways Movement"
                ma_strength = "neutral"
            
            indicators['Moving_Averages'] = {
                'signal': ma_signal,
                'strength': ma_strength
            }
        
        # Volume Analysis
        if n_features > 21:
            volume_ratio = latest_data[21]
            
            if volume_ratio > 1.5:
                vol_signal = "HIGH Volume - Strong Conviction"
                vol_strength = "high_conviction"
            elif volume_ratio > 1.2:
                vol_signal = "Above Average Volume"
                vol_strength = "medium_conviction"
            elif volume_ratio < 0.8:
                vol_signal = "LOW Volume - Weak Conviction"
                vol_strength = "low_conviction"
            else:
                vol_signal = "Normal Volume"
                vol_strength = "medium_conviction"
            
            indicators['Volume'] = {
                'ratio': round(volume_ratio, 2),
                'signal': vol_signal,
                'strength': vol_strength
            }
        
        # Bollinger Bands (check if price near bands)
        if n_features > 17:
            bb_upper = latest_data[15]
            bb_lower = latest_data[16]
            close = latest_data[3]
            
            # Calculate relative position
            bb_range = bb_upper - bb_lower
            if bb_range > 0:
                position = (close - bb_lower) / bb_range
                
                if position > 0.9:
                    bb_signal = "Near Upper Band - Potential Reversal"
                    bb_strength = "bearish"
                elif position < 0.1:
                    bb_signal = "Near Lower Band - Potential Bounce"
                    bb_strength = "bullish"
                else:
                    bb_signal = "Within Normal Range"
                    bb_strength = "neutral"
                
                indicators['Bollinger_Bands'] = {
                    'position': round(position, 2),
                    'signal': bb_signal,
                    'strength': bb_strength
                }
        
        # Volatility Analysis
        if n_features > 22:
            volatility = latest_data[22]
            
            if volatility > 0.8:
                vol_signal = "HIGH Volatility - Risky"
            elif volatility < 0.3:
                vol_signal = "LOW Volatility - Stable"
            else:
                vol_signal = "MODERATE Volatility"
            
            indicators['Volatility'] = {
                'level': round(volatility, 4),
                'signal': vol_signal
            }
        
        return indicators
    
    def _analyze_attention(self, attention_weights: np.ndarray) -> Dict[str, any]:
        """Analyze attention patterns to understand what the model focuses on"""
        
        if attention_weights is None or len(attention_weights) == 0:
            return None
        
        # Average attention across all heads and layers
        avg_attention = np.mean(attention_weights, axis=0) if len(attention_weights.shape) > 1 else attention_weights
        
        # Find most attended positions
        top_positions = np.argsort(avg_attention)[-3:][::-1]  # Top 3 positions
        
        # Analyze temporal focus
        recent_focus = np.mean(avg_attention[-5:])  # Last 5 timesteps
        distant_focus = np.mean(avg_attention[:-5]) if len(avg_attention) > 5 else 0
        
        if recent_focus > distant_focus * 1.5:
            temporal_focus = "Model heavily weights RECENT market movements"
        elif distant_focus > recent_focus * 1.5:
            temporal_focus = "Model considers HISTORICAL patterns"
        else:
            temporal_focus = "Model balances recent and historical data"
        
        return {
            'top_attended_positions': top_positions.tolist(),
            'recent_focus_strength': round(float(recent_focus), 4),
            'temporal_pattern': temporal_focus,
            'attention_distribution': 'focused' if np.std(avg_attention) > 0.1 else 'distributed'
        }
    
    def _generate_explanation(
        self,
        prediction: float,
        current_price: float,
        price_change_pct: float,
        direction: str,
        technical_analysis: Dict,
        attention_insights: Optional[Dict],
        confidence: Optional[float]
    ) -> str:
        """Generate natural language explanation"""
        
        explanation_parts = []
        
        # Main prediction statement
        if abs(price_change_pct) < 0.5:
            movement = "remain relatively stable"
        elif abs(price_change_pct) < 2:
            movement = f"{'increase' if price_change_pct > 0 else 'decrease'} moderately"
        else:
            movement = f"{'rise' if price_change_pct > 0 else 'fall'} significantly"
        
        intro = f"🎯 The AI predicts the stock will {movement} by {abs(price_change_pct):.2f}% "
        intro += f"to ₹{prediction:.2f} (currently ₹{current_price:.2f})."
        
        if confidence:
            intro += f" Confidence: {confidence*100:.1f}%."
        
        explanation_parts.append(intro)
        
        # Technical indicator reasoning
        bullish_signals = 0
        bearish_signals = 0
        reasons = []
        
        for indicator_name, indicator_data in technical_analysis.items():
            strength = indicator_data.get('strength', 'neutral')
            signal = indicator_data.get('signal', '')
            
            if 'bullish' in strength:
                bullish_signals += 2 if 'strong' in strength else 1
                reasons.append(f"✓ {indicator_name}: {signal}")
            elif 'bearish' in strength:
                bearish_signals += 2 if 'strong' in strength else 1
                reasons.append(f"✗ {indicator_name}: {signal}")
        
        # Add key reasons
        if reasons:
            explanation_parts.append("\n📊 Key Technical Signals:")
            explanation_parts.extend(reasons[:4])  # Top 4 reasons
        
        # Overall sentiment
        if bullish_signals > bearish_signals + 2:
            sentiment = "The technical indicators are STRONGLY BULLISH"
        elif bullish_signals > bearish_signals:
            sentiment = "The technical indicators lean BULLISH"
        elif bearish_signals > bullish_signals + 2:
            sentiment = "The technical indicators are STRONGLY BEARISH"
        elif bearish_signals > bullish_signals:
            sentiment = "The technical indicators lean BEARISH"
        else:
            sentiment = "The technical indicators show MIXED SIGNALS"
        
        explanation_parts.append(f"\n💡 {sentiment}.")
        
        # Attention insights
        if attention_insights:
            explanation_parts.append(f"\n🧠 {attention_insights['temporal_pattern']}.")
        
        return "\n".join(explanation_parts)
    
    def _identify_key_factors(
        self,
        technical_analysis: Dict,
        attention_insights: Optional[Dict]
    ) -> List[str]:
        """Identify and rank key factors driving the prediction"""
        
        factors = []
        
        # Sort by signal strength
        for indicator_name, indicator_data in technical_analysis.items():
            strength = indicator_data.get('strength', 'neutral')
            signal = indicator_data.get('signal', '')
            
            if 'strong' in strength or 'high' in strength:
                factors.append(f"{indicator_name}: {signal}")
        
        # Add attention insight if significant
        if attention_insights and attention_insights.get('recent_focus_strength', 0) > 0.3:
            factors.append(f"Model Focus: {attention_insights['temporal_pattern']}")
        
        return factors[:5]  # Top 5 factors
    
    def _assess_risk(self, technical_analysis: Dict) -> str:
        """Assess overall risk level based on technical indicators"""
        
        risk_score = 0
        
        # High volatility increases risk
        if 'Volatility' in technical_analysis:
            vol_level = technical_analysis['Volatility'].get('level', 0)
            if vol_level > 0.7:
                risk_score += 2
            elif vol_level > 0.5:
                risk_score += 1
        
        # Low volume increases risk
        if 'Volume' in technical_analysis:
            vol_strength = technical_analysis['Volume'].get('strength', '')
            if 'low' in vol_strength:
                risk_score += 1
        
        # Overbought/oversold conditions
        if 'RSI' in technical_analysis:
            rsi_strength = technical_analysis['RSI'].get('strength', '')
            if 'strong' in rsi_strength:
                risk_score += 1
        
        # Determine risk level
        if risk_score >= 3:
            return "HIGH ⚠️"
        elif risk_score >= 2:
            return "MODERATE ⚡"
        else:
            return "LOW ✅"


def explain_model_prediction(
    model,
    sequence_data: np.ndarray,
    scaler,
    return_attention: bool = True
) -> Dict:
    """
    Helper function to generate prediction with explanation
    
    Args:
        model: Trained transformer model
        sequence_data: Input sequence
        scaler: Data scaler for denormalization
        return_attention: Whether to extract attention weights
        
    Returns:
        Dictionary with prediction and explanation
    """
    
    explainer = AIExplainer()
    
    # Make prediction
    with torch.no_grad():
        x = torch.FloatTensor(sequence_data).unsqueeze(0)
        prediction = model(x).item()
        
        # Get attention weights if requested
        attention_weights = None
        if return_attention and hasattr(model, 'get_attention_weights'):
            attention_weights = model.get_attention_weights()
            if attention_weights is not None:
                attention_weights = attention_weights[0].cpu().numpy()  # First sample
    
    # Denormalize prediction and current price
    current_price = sequence_data[-1, 3]  # Close price from last timestep
    
    # Simple denormalization approximation
    # In production, you'd use the actual scaler inverse transform
    pred_denorm = prediction
    current_denorm = current_price
    
    # Generate explanation
    explanation = explainer.explain_prediction(
        prediction=pred_denorm,
        current_price=current_denorm,
        sequence_data=sequence_data,
        attention_weights=attention_weights,
        confidence=0.75  # Placeholder - calculate actual confidence in production
    )
    
    return explanation
