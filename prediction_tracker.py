"""
Prediction Accuracy Tracker
Stores predictions and tracks accuracy over time
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import yfinance as yf
import numpy as np

class PredictionTracker:
    """
    Tracks predictions and measures accuracy against actual prices
    """
    
    def __init__(self, storage_file: str = "predictions_log.json"):
        self.storage_file = storage_file
        self.predictions = self._load_predictions()
    
    def _load_predictions(self) -> List[Dict]:
        """Load predictions from storage"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_predictions(self):
        """Save predictions to storage"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.predictions, f, indent=2)
    
    def log_prediction(
        self,
        symbol: str,
        current_price: float,
        predicted_price: float,
        prediction_date: str,
        target_date: Optional[str] = None,
        days_ahead: int = 1,
        confidence: Optional[float] = None,
        explanation: Optional[str] = None
    ) -> Dict:
        """
        Log a new prediction
        
        Args:
            symbol: Stock symbol
            current_price: Current price at prediction time
            predicted_price: Predicted future price
            prediction_date: When prediction was made
            target_date: Target date for prediction
            days_ahead: Days ahead predicted
            confidence: Model confidence
            explanation: AI explanation
            
        Returns:
            Logged prediction record
        """
        
        # Calculate target date if not provided
        if not target_date:
            pred_dt = datetime.fromisoformat(prediction_date.replace('Z', '+00:00'))
            target_dt = pred_dt + timedelta(days=days_ahead)
            target_date = target_dt.isoformat()
        
        prediction_record = {
            'id': len(self.predictions) + 1,
            'symbol': symbol,
            'prediction_date': prediction_date,
            'target_date': target_date,
            'days_ahead': days_ahead,
            'current_price': round(current_price, 2),
            'predicted_price': round(predicted_price, 2),
            'predicted_change_pct': round(((predicted_price - current_price) / current_price) * 100, 2),
            'actual_price': None,
            'actual_change_pct': None,
            'accuracy_error': None,
            'status': 'pending',
            'confidence': confidence,
            'explanation_summary': explanation[:200] if explanation else None,
            'verified': False,
            'verified_date': None
        }
        
        self.predictions.append(prediction_record)
        self._save_predictions()
        
        return prediction_record
    
    def verify_predictions(self, symbol: Optional[str] = None) -> Dict:
        """
        Verify pending predictions by fetching actual prices
        
        Args:
            symbol: Specific symbol to verify, or None for all
            
        Returns:
            Verification results
        """
        
        verified_count = 0
        updated_predictions = []
        
        for pred in self.predictions:
            # Skip if already verified or wrong symbol
            if pred['verified']:
                continue
            if symbol and pred['symbol'] != symbol:
                continue
            
            # Check if target date has passed
            target_dt = datetime.fromisoformat(pred['target_date'].replace('Z', '+00:00'))
            if target_dt > datetime.now():
                continue  # Not yet time to verify
            
            # Fetch actual price
            try:
                actual_price = self._get_actual_price(pred['symbol'], pred['target_date'])
                if actual_price:
                    # Update prediction with actual data
                    pred['actual_price'] = round(actual_price, 2)
                    pred['actual_change_pct'] = round(
                        ((actual_price - pred['current_price']) / pred['current_price']) * 100, 2
                    )
                    
                    # Calculate accuracy metrics
                    pred['accuracy_error'] = round(
                        abs(pred['predicted_price'] - actual_price) / actual_price * 100, 2
                    )
                    
                    # Determine status
                    direction_correct = (
                        (pred['predicted_change_pct'] > 0 and pred['actual_change_pct'] > 0) or
                        (pred['predicted_change_pct'] < 0 and pred['actual_change_pct'] < 0)
                    )
                    
                    if pred['accuracy_error'] < 2:
                        pred['status'] = 'excellent'
                    elif pred['accuracy_error'] < 5:
                        pred['status'] = 'good'
                    elif direction_correct:
                        pred['status'] = 'direction_correct'
                    else:
                        pred['status'] = 'incorrect'
                    
                    pred['verified'] = True
                    pred['verified_date'] = datetime.now().isoformat()
                    
                    verified_count += 1
                    updated_predictions.append(pred)
            except Exception as e:
                print(f"Error verifying {pred['symbol']}: {e}")
                continue
        
        self._save_predictions()
        
        return {
            'verified_count': verified_count,
            'updated_predictions': updated_predictions
        }
    
    def _get_actual_price(self, symbol: str, target_date: str) -> Optional[float]:
        """Fetch actual price for a symbol on a specific date"""
        try:
            target_dt = datetime.fromisoformat(target_date.replace('Z', '+00:00'))
            # Get data for a few days around target date
            start_date = (target_dt - timedelta(days=2)).strftime('%Y-%m-%d')
            end_date = (target_dt + timedelta(days=2)).strftime('%Y-%m-%d')
            
            df = yf.download(symbol, start=start_date, end=end_date, progress=False)
            
            if not df.empty:
                # Get closest date
                target_date_str = target_dt.strftime('%Y-%m-%d')
                if target_date_str in df.index.strftime('%Y-%m-%d'):
                    return float(df.loc[df.index.strftime('%Y-%m-%d') == target_date_str]['Close'].iloc[0])
                else:
                    # Return most recent close price
                    return float(df['Close'].iloc[-1])
            return None
        except Exception as e:
            print(f"Error fetching price: {e}")
            return None
    
    def get_accuracy_stats(self, symbol: Optional[str] = None, days: int = 30) -> Dict:
        """
        Calculate accuracy statistics
        
        Args:
            symbol: Filter by symbol (None for all)
            days: Look back period in days
            
        Returns:
            Accuracy statistics
        """
        
        # Filter predictions
        cutoff_date = datetime.now() - timedelta(days=days)
        filtered = [
            p for p in self.predictions
            if p['verified'] and
            (not symbol or p['symbol'] == symbol) and
            datetime.fromisoformat(p['prediction_date'].replace('Z', '+00:00')) >= cutoff_date
        ]
        
        if not filtered:
            return {
                'total_predictions': 0,
                'verified_predictions': 0,
                'accuracy_rate': 0,
                'avg_error': 0,
                'direction_accuracy': 0,
                'status_breakdown': {}
            }
        
        # Calculate stats
        total = len(filtered)
        direction_correct = sum(1 for p in filtered if p['status'] in ['excellent', 'good', 'direction_correct'])
        excellent = sum(1 for p in filtered if p['status'] == 'excellent')
        good = sum(1 for p in filtered if p['status'] == 'good')
        
        errors = [p['accuracy_error'] for p in filtered if p['accuracy_error'] is not None]
        avg_error = np.mean(errors) if errors else 0
        
        return {
            'total_predictions': total,
            'verified_predictions': total,
            'accuracy_rate': round((excellent + good) / total * 100, 2) if total > 0 else 0,
            'avg_error': round(avg_error, 2),
            'direction_accuracy': round(direction_correct / total * 100, 2) if total > 0 else 0,
            'status_breakdown': {
                'excellent': sum(1 for p in filtered if p['status'] == 'excellent'),
                'good': sum(1 for p in filtered if p['status'] == 'good'),
                'direction_correct': sum(1 for p in filtered if p['status'] == 'direction_correct'),
                'incorrect': sum(1 for p in filtered if p['status'] == 'incorrect')
            },
            'recent_predictions': filtered[-10:][::-1]  # Last 10, most recent first
        }
    
    def get_all_predictions(
        self,
        symbol: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get predictions with optional filtering
        
        Args:
            symbol: Filter by symbol
            status: Filter by status (pending, excellent, good, etc.)
            limit: Maximum number to return
            
        Returns:
            List of predictions
        """
        
        filtered = self.predictions
        
        if symbol:
            filtered = [p for p in filtered if p['symbol'] == symbol]
        
        if status:
            filtered = [p for p in filtered if p['status'] == status]
        
        # Sort by date (most recent first)
        filtered.sort(key=lambda x: x['prediction_date'], reverse=True)
        
        return filtered[:limit]
    
    def get_performance_chart_data(self, symbol: Optional[str] = None) -> Dict:
        """
        Get data for accuracy performance chart
        
        Args:
            symbol: Filter by symbol
            
        Returns:
            Chart data
        """
        
        verified = [p for p in self.predictions if p['verified']]
        if symbol:
            verified = [p for p in verified if p['symbol'] == symbol]
        
        if not verified:
            return {'dates': [], 'accuracy': [], 'errors': []}
        
        # Sort by date
        verified.sort(key=lambda x: x['verified_date'])
        
        # Calculate cumulative accuracy
        dates = []
        accuracy_rates = []
        errors = []
        
        for i, pred in enumerate(verified):
            dates.append(pred['verified_date'][:10])  # Date only
            
            # Calculate accuracy up to this point
            subset = verified[:i+1]
            accurate = sum(1 for p in subset if p['status'] in ['excellent', 'good'])
            acc_rate = (accurate / len(subset)) * 100
            accuracy_rates.append(round(acc_rate, 2))
            
            # Average error up to this point
            errs = [p['accuracy_error'] for p in subset if p['accuracy_error'] is not None]
            avg_err = np.mean(errs) if errs else 0
            errors.append(round(avg_err, 2))
        
        return {
            'dates': dates,
            'accuracy_rates': accuracy_rates,
            'average_errors': errors
        }
