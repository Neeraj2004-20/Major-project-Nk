"""
Graph Generator - Create price trend charts showing up/down movements
Uses matplotlib to generate ASCII and image charts
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
from pathlib import Path

class GraphGenerator:
    """Generate prediction graphs and trend charts"""
    
    @staticmethod
    def create_ascii_chart(data: List[float], title: str = "Price Trend", width: int = 60, height: int = 10) -> str:
        """Create ASCII chart for terminal display"""
        if not data or len(data) == 0:
            return "No data available"
        
        min_val = min(data)
        max_val = max(data)
        range_val = max_val - min_val if max_val != min_val else 1
        
        chart = f"\n{title}\n"
        chart += "=" * width + "\n"
        
        # Create grid
        for row in range(height, 0, -1):
            chart += f"{min_val + range_val * row / height:7.2f} |"
            
            for i, val in enumerate(data):
                if len(data) > width - 10:
                    # Sample data if too much
                    idx = int(i * len(data) / (width - 10))
                    val = data[idx]
                
                normalized = (val - min_val) / range_val if range_val > 0 else 0.5
                
                if normalized * height >= row - 0.5:
                    chart += "█"
                else:
                    chart += " "
            
            chart += "\n"
        
        chart += f"{min_val:7.2f} |" + "-" * (width - 10) + "\n"
        
        # X-axis labels
        chart += "        " + "[Historical Data →]\n"
        return chart
    
    @staticmethod
    def create_trend_analysis(prices: List[float]) -> Dict:
        """Analyze price trend (up/down/stable)"""
        if len(prices) < 2:
            return {'trend': 'insufficient_data', 'change_percent': 0}
        
        start = prices[0]
        end = prices[-1]
        change = end - start
        change_percent = (change / start * 100) if start != 0 else 0
        
        # Determine trend
        if change_percent > 2:
            trend = 'UPTREND'
        elif change_percent < -2:
            trend = 'DOWNTREND'
        else:
            trend = 'STABLE'
        
        # Calculate moving average
        ma_5 = sum(prices[-5:]) / min(5, len(prices))
        
        return {
            'trend': trend,
            'change_percent': round(change_percent, 2),
            'start_price': round(start, 2),
            'end_price': round(end, 2),
            'high': round(max(prices), 2),
            'low': round(min(prices), 2),
            'moving_average_5': round(ma_5, 2),
            'volatility': round(max(prices) - min(prices), 2)
        }
    
    @staticmethod
    def create_prediction_chart(predictions: List[Dict], title: str = "Price Predictions") -> str:
        """Create chart showing predictions vs actual prices"""
        if not predictions:
            return "No predictions available"
        
        # Extract data
        times = []
        predicted = []
        actual = []
        signals = []
        
        for i, pred in enumerate(predictions[-30:]):  # Last 30 predictions
            times.append(f"P{i+1}")
            predicted.append(pred.get('predicted_price', 0))
            actual.append(pred.get('actual_price', pred.get('predicted_price', 0)))
            signals.append(pred.get('signal', 'HOLD'))
        
        # Create visualization
        chart = f"\n{title}\n"
        chart += "=" * 70 + "\n"
        chart += "Time      | Predicted | Actual    | Signal | Change\n"
        chart += "-" * 70 + "\n"
        
        for i, (t, p, a, s) in enumerate(zip(times, predicted, actual, signals)):
            change = ((a - p) / p * 100) if p != 0 else 0
            change_symbol = "↑" if change > 0 else "↓" if change < 0 else "→"
            
            chart += f"{t:10}| {p:9.2f} | {a:9.2f} | {s:6} | {change_symbol} {change:+.2f}%\n"
        
        return chart
    
    @staticmethod
    def generate_html_chart(symbol: str, predictions: List[Dict]) -> str:
        """Generate HTML chart for web display"""
        if not predictions:
            return "<p>No predictions available</p>"
        
        # Prepare data
        labels = [f"P{i+1}" for i in range(len(predictions[-30:]))]
        predicted_prices = [p.get('predicted_price', 0) for p in predictions[-30:]]
        actual_prices = [p.get('actual_price', p.get('predicted_price', 0)) for p in predictions[-30:]]
        signals = [p.get('signal', 'HOLD') for p in predictions[-30:]]
        
        # Colors for signals
        signal_colors = {"BUY": "#00ff00", "SELL": "#ff0000", "HOLD": "#ffff00"}
        
        html = f"""
        <div style="margin: 20px;">
            <h2>{symbol} Prediction Chart</h2>
            <canvas id="prediction-chart"></canvas>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script>
                const ctx = document.getElementById('prediction-chart').getContext('2d');
                const chart = new Chart(ctx, {{
                    type: 'line',
                    data: {{
                        labels: {json.dumps(labels)},
                        datasets: [
                            {{
                                label: 'Predicted Price',
                                data: {json.dumps(predicted_prices)},
                                borderColor: '#2196f3',
                                backgroundColor: 'rgba(33, 150, 243, 0.1)',
                                borderWidth: 2,
                                fill: true
                            }},
                            {{
                                label: 'Actual Price',
                                data: {json.dumps(actual_prices)},
                                borderColor: '#ff9800',
                                backgroundColor: 'rgba(255, 152, 0, 0.1)',
                                borderWidth: 2,
                                fill: true
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        plugins: {{
                            title: {{
                                display: true,
                                text: '{symbol} Predictions vs Actual'
                            }},
                            legend: {{
                                display: true,
                                position: 'top'
                            }}
                        }},
                        scales: {{
                            y: {{
                                title: {{
                                    display: true,
                                    text: 'Price ($)'
                                }}
                            }}
                        }}
                    }}
                }});
            </script>
        </div>
        """
        
        return html

# Utility functions
def format_chart_data(predictions: List[Dict]) -> Dict:
    """Format predictions for chart display"""
    return {
        'labels': [f"P{i+1}" for i in range(len(predictions))],
        'predicted': [p.get('predicted_price') for p in predictions],
        'actual': [p.get('actual_price') for p in predictions],
        'signals': [p.get('signal') for p in predictions],
        'confidence': [p.get('confidence') for p in predictions],
    }

def detect_pattern(prices: List[float]) -> str:
    """Detect price patterns"""
    if len(prices) < 3:
        return "insufficient_data"
    
    # Check for peaks and troughs
    ups = sum(1 for i in range(1, len(prices)) if prices[i] > prices[i-1])
    downs = sum(1 for i in range(1, len(prices)) if prices[i] < prices[i-1])
    
    if ups > downs * 1.5:
        return "strong_uptrend"
    elif downs > ups * 1.5:
        return "strong_downtrend"
    elif abs(ups - downs) < 2:
        return "oscillating"
    else:
        return "mixed"
