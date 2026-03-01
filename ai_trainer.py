"""
AI Training Module - Learn from user feedback to improve prediction accuracy
"""

from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path

class AITrainer:
    """AI training system that learns from user feedback"""
    
    def __init__(self, model_file="ai_model.json"):
        self.model_file = Path(model_file)
        self.model = {
            'buy_threshold': 0.7,
            'sell_threshold': 0.3,
            'confidence_boost': {},  # Per symbol confidence adjustments
            'signal_accuracy': {'BUY': 0.5, 'SELL': 0.5, 'HOLD': 0.5},
            'training_samples': 0,
            'last_updated': None
        }
        self.load_model()
    
    def load_model(self):
        """Load trained model from file"""
        if self.model_file.exists():
            try:
                self.model = json.loads(self.model_file.read_text())
            except:
                pass
    
    def save_model(self):
        """Save trained model to file"""
        self.model['last_updated'] = datetime.now().isoformat()
        self.model_file.write_text(json.dumps(self.model, indent=2))
    
    def process_feedback(self, feedback_list: List[Dict]) -> Dict:
        """Process user feedback and update model"""
        if not feedback_list:
            return {'status': 'no_feedback', 'updated': False}
        
        correct_count = 0
        signal_results = {'BUY': [], 'SELL': [], 'HOLD': []}
        
        for feedback in feedback_list:
            if feedback['correct']:
                correct_count += 1
                signal = feedback.get('signal', 'HOLD')
                signal_results[signal].append(True)
            else:
                signal = feedback.get('signal', 'HOLD')
                signal_results[signal].append(False)
        
        # Update signal accuracy
        for signal, results in signal_results.items():
            if results:
                accuracy = sum(results) / len(results)
                # Weighted average with existing accuracy
                old_accuracy = self.model['signal_accuracy'].get(signal, 0.5)
                self.model['signal_accuracy'][signal] = (
                    old_accuracy * 0.7 + accuracy * 0.3
                )
        
        # Update training samples
        self.model['training_samples'] += len(feedback_list)
        
        self.save_model()
        
        return {
            'status': 'success',
            'updated': True,
            'correct_feedback': correct_count,
            'total_feedback': len(feedback_list),
            'accuracy_rate': round(correct_count / len(feedback_list) * 100, 2),
            'signal_accuracy': {k: round(v, 3) for k, v in self.model['signal_accuracy'].items()}
        }
    
    def adjust_prediction(self, symbol: str, signal: str, base_confidence: float) -> Dict:
        """Adjust prediction based on trained model"""
        # Get symbol-specific boost
        boost = self.model.get('confidence_boost', {}).get(symbol, 0)
        
        # Get signal accuracy factor
        signal_factor = self.model['signal_accuracy'].get(signal, 0.5)
        
        # Adjust confidence
        adjusted_confidence = base_confidence * signal_factor + boost
        adjusted_confidence = min(0.99, max(0.1, adjusted_confidence))
        
        return {
            'original_confidence': base_confidence,
            'adjusted_confidence': round(adjusted_confidence, 2),
            'signal_factor': round(signal_factor, 3),
            'symbol_boost': boost,
            'trained_on_samples': self.model['training_samples']
        }
    
    def suggest_improvement(self, symbol: str, feedback: List[Dict]) -> Dict:
        """Suggest model improvements based on feedback"""
        suggestions = []
        
        # Analyze by signal type
        buy_feedback = [f for f in feedback if f.get('signal') == 'BUY']
        sell_feedback = [f for f in feedback if f.get('signal') == 'SELL']
        
        if buy_feedback:
            buy_accuracy = sum(1 for f in buy_feedback if f['correct']) / len(buy_feedback)
            if buy_accuracy < 0.5:
                suggestions.append({
                    'issue': 'Low BUY signal accuracy',
                    'accuracy': round(buy_accuracy, 2),
                    'recommendation': 'Increase BUY threshold or adjust signal parameters'
                })
        
        if sell_feedback:
            sell_accuracy = sum(1 for f in sell_feedback if f['correct']) / len(sell_feedback)
            if sell_accuracy < 0.5:
                suggestions.append({
                    'issue': 'Low SELL signal accuracy',
                    'accuracy': round(sell_accuracy, 2),
                    'recommendation': 'Decrease SELL threshold or adjust signal parameters'
                })
        
        if not suggestions:
            suggestions.append({
                'status': 'model_performing_well',
                'accuracy': round(
                    sum(1 for f in feedback if f['correct']) / len(feedback) * 100, 2
                )
            })
        
        return {
            'symbol': symbol,
            'suggestions': suggestions,
            'total_feedback_samples': len(feedback)
        }
    
    def get_model_stats(self) -> Dict:
        """Get current model statistics"""
        return {
            'training_samples': self.model['training_samples'],
            'buy_threshold': self.model['buy_threshold'],
            'sell_threshold': self.model['sell_threshold'],
            'signal_accuracy': {
                k: round(v, 3) for k, v in self.model['signal_accuracy'].items()
            },
            'symbols_tuned': len(self.model.get('confidence_boost', {})),
            'last_updated': self.model.get('last_updated', 'never')
        }
    
    def improve_for_symbol(self, symbol: str, adjust_value: float):
        """Improve confidence for specific symbol based on performance"""
        if 'confidence_boost' not in self.model:
            self.model['confidence_boost'] = {}
        
        current = self.model['confidence_boost'].get(symbol, 0)
        self.model['confidence_boost'][symbol] = min(0.2, max(-0.2, current + adjust_value))
        
        self.save_model()

# Global AI trainer instance
ai_trainer = AITrainer()
