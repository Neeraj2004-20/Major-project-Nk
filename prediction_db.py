"""
Enhanced Prediction Database - Store predictions and history for AI training
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
from pathlib import Path

class PredictionDatabase:
    """In-memory and file-based prediction storage"""
    
    def __init__(self, db_file="predictions_db.json"):
        self.db_file = Path(db_file)
        self.predictions = {}
        self.accuracy_scores = {}
        self.user_feedback = []
        self.load_from_file()
    
    def load_from_file(self):
        """Load existing predictions from file"""
        if self.db_file.exists():
            try:
                data = json.loads(self.db_file.read_text())
                self.predictions = data.get('predictions', {})
                self.accuracy_scores = data.get('accuracy_scores', {})
                self.user_feedback = data.get('user_feedback', [])
            except:
                pass
    
    def save_to_file(self):
        """Save predictions to file"""
        data = {
            'predictions': self.predictions,
            'accuracy_scores': self.accuracy_scores,
            'user_feedback': self.user_feedback
        }
        self.db_file.write_text(json.dumps(data, indent=2))
    
    def store_prediction(self, symbol: str, prediction: Dict):
        """Store a prediction"""
        if symbol not in self.predictions:
            self.predictions[symbol] = []
        
        record = {
            'timestamp': datetime.now().isoformat(),
            'predicted_price': prediction.get('predicted_price'),
            'current_price': prediction.get('current_price'),
            'signal': prediction.get('signal'),
            'confidence': prediction.get('confidence'),
            'engine': prediction.get('engine'),
            'actual_price': None,  # Updated later
            'accuracy': None  # Updated when actual price known
        }
        
        self.predictions[symbol].append(record)
        self.save_to_file()
        return record
    
    def update_prediction_accuracy(self, symbol: str, idx: int, actual_price: float):
        """Update prediction with actual price and calculate accuracy"""
        if symbol in self.predictions and idx < len(self.predictions[symbol]):
            pred = self.predictions[symbol][idx]
            pred['actual_price'] = actual_price
            
            # Calculate accuracy
            predicted = pred['predicted_price']
            actual = actual_price
            error = abs(predicted - actual) / actual * 100
            accuracy = max(0, 100 - error)
            
            pred['accuracy'] = round(accuracy, 2)
            
            # Update symbol accuracy
            if symbol not in self.accuracy_scores:
                self.accuracy_scores[symbol] = []
            self.accuracy_scores[symbol].append(accuracy)
            
            self.save_to_file()
    
    def get_predictions_history(self, symbol: str, days: int = 30) -> List[Dict]:
        """Get prediction history for symbol"""
        if symbol not in self.predictions:
            return []
        
        cutoff = datetime.now() - timedelta(days=days)
        return [
            p for p in self.predictions[symbol]
            if datetime.fromisoformat(p['timestamp']) > cutoff
        ]
    
    def get_accuracy(self, symbol: str) -> Dict:
        """Get accuracy metrics for symbol"""
        if symbol not in self.accuracy_scores or not self.accuracy_scores[symbol]:
            return {'average': 0, 'count': 0}
        
        scores = [s for s in self.accuracy_scores[symbol] if s is not None]
        return {
            'average': round(sum(scores) / len(scores), 2) if scores else 0,
            'best': round(max(scores), 2) if scores else 0,
            'worst': round(min(scores), 2) if scores else 0,
            'count': len(scores)
        }
    
    def add_feedback(self, symbol: str, prediction_idx: int, correct: bool, notes: str = ""):
        """Store user feedback for AI training"""
        feedback = {
            'symbol': symbol,
            'prediction_idx': prediction_idx,
            'timestamp': datetime.now().isoformat(),
            'correct': correct,
            'notes': notes
        }
        self.user_feedback.append(feedback)
        self.save_to_file()
    
    def get_feedback(self, symbol: str = None) -> List[Dict]:
        """Get user feedback for training"""
        if symbol:
            return [f for f in self.user_feedback if f['symbol'] == symbol]
        return self.user_feedback
    
    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        total_predictions = sum(
            len(preds) for preds in self.predictions.values()
        )
        
        all_accuracies = []
        for scores in self.accuracy_scores.values():
            all_accuracies.extend([s for s in scores if s is not None])
        
        accurate_feedback = len([f for f in self.user_feedback if f['correct']])
        
        return {
            'total_predictions': total_predictions,
            'symbols_tracked': len(self.predictions),
            'average_accuracy': round(
                sum(all_accuracies) / len(all_accuracies), 2
            ) if all_accuracies else 0,
            'total_feedback': len(self.user_feedback),
            'accurate_feedback': accurate_feedback,
            'feedback_accuracy_rate': round(
                accurate_feedback / len(self.user_feedback) * 100, 2
            ) if self.user_feedback else 0
        }

# Global instance
prediction_db = PredictionDatabase()
