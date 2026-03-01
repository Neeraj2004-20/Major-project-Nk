"""
Backtesting Engine for Market Predictor
Validates model performance on historical data with trading simulation
"""

import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
import torch
from model import AdvancedTimeSeriesTransformer
from data_loader import add_technical_indicators


class BacktestingEngine:
    """
    Backtesting engine that simulates trading based on model predictions
    over historical data to validate real-world performance.
    """
    
    def __init__(self, model, scaler):
        """
        Initialize backtesting engine
        
        Args:
            model: Trained transformer model
            scaler: Fitted data scaler
        """
        self.model = model
        self.scaler = scaler
        self.results = {}
        
    def run_backtest(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        initial_capital: float = 100000.0,
        seq_length: int = 60,
        transaction_cost: float = 0.001,  # 0.1% per trade
        confidence_threshold: float = 0.02  # Only trade if predicted change > 2%
    ) -> Dict:
        """
        Run backtest on historical data
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE.NS')
            start_date: Start date for backtest (YYYY-MM-DD)
            end_date: End date for backtest (YYYY-MM-DD)
            initial_capital: Starting capital in INR
            seq_length: Sequence length for predictions
            transaction_cost: Transaction cost percentage
            confidence_threshold: Minimum predicted change to trigger trade
            
        Returns:
            Dictionary with backtest results and metrics
        """
        print(f"🔄 Running backtest for {symbol} from {start_date} to {end_date}...")
        
        # Download historical data with extra buffer for sequence
        buffer_days = seq_length + 30
        buffer_start = (datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=buffer_days)).strftime('%Y-%m-%d')
        
        data = yf.download(symbol, start=buffer_start, end=end_date, progress=False)
        
        if data.empty:
            raise ValueError(f"No data available for {symbol}")
        
        # Add technical indicators
        data_with_indicators = add_technical_indicators(data)
        
        # Prepare features
        feature_columns = [
            'Close', 'Volume', 'SMA_20', 'SMA_50', 'EMA_12', 'EMA_26',
            'RSI', 'MACD', 'MACD_Signal', 'BB_Upper', 'BB_Lower',
            'ATR', 'OBV', 'Stoch_K', 'Stoch_D', 'Williams_R',
            'ROC', 'MFI', 'CCI', 'ADX', 'Plus_DI', 'Minus_DI',
            'Ichimoku_Conversion', 'Ichimoku_Base', 'Parabolic_SAR',
            'Volume_SMA', 'Volume_Ratio', 'Price_SMA_Ratio', 'Volatility',
            'Upper_Shadow', 'Lower_Shadow'
        ]
        
        # Fill NaN values
        data_with_indicators = data_with_indicators.fillna(method='bfill').fillna(method='ffill')
        
        # Extract features
        features = data_with_indicators[feature_columns].values
        
        # Scale features
        scaled_features = self.scaler.transform(features)
        
        # Run simulation
        trades = []
        portfolio_values = []
        cash = initial_capital
        position = 0  # Number of shares held
        position_price = 0  # Price at which position was opened
        
        # Start from index where we have enough history
        start_idx = seq_length
        
        # Find actual start date index
        actual_start_date = datetime.strptime(start_date, '%Y-%m-%d')
        for idx in range(start_idx, len(data_with_indicators)):
            if data_with_indicators.index[idx] >= actual_start_date:
                start_idx = idx
                break
        
        for idx in range(start_idx, len(scaled_features) - 1):
            current_date = data_with_indicators.index[idx]
            current_price = data_with_indicators['Close'].iloc[idx]
            next_day_actual_price = data_with_indicators['Close'].iloc[idx + 1]
            
            # Get sequence for prediction
            sequence = scaled_features[idx - seq_length:idx]
            
            # Make prediction
            with torch.no_grad():
                sequence_tensor = torch.FloatTensor(sequence).unsqueeze(0)
                predicted_scaled = self.model(sequence_tensor).item()
            
            # Inverse transform prediction (only the Close price column - index 0)
            dummy_array = np.zeros((1, len(feature_columns)))
            dummy_array[0, 0] = predicted_scaled
            predicted_price = self.scaler.inverse_transform(dummy_array)[0, 0]
            
            # Calculate predicted change
            predicted_change = (predicted_price - current_price) / current_price
            
            # Trading logic
            if position == 0:  # Not holding any position
                if predicted_change > confidence_threshold:  # Buy signal
                    # Buy as many shares as possible
                    shares_to_buy = int(cash / (current_price * (1 + transaction_cost)))
                    if shares_to_buy > 0:
                        cost = shares_to_buy * current_price * (1 + transaction_cost)
                        cash -= cost
                        position = shares_to_buy
                        position_price = current_price
                        
                        trades.append({
                            'date': current_date.strftime('%Y-%m-%d'),
                            'type': 'BUY',
                            'price': current_price,
                            'shares': shares_to_buy,
                            'predicted_price': predicted_price,
                            'predicted_change': predicted_change * 100,
                            'cost': cost
                        })
            
            else:  # Holding position
                if predicted_change < -confidence_threshold:  # Sell signal
                    # Sell entire position
                    revenue = position * current_price * (1 - transaction_cost)
                    profit = revenue - (position * position_price * (1 + transaction_cost))
                    cash += revenue
                    
                    trades.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'type': 'SELL',
                        'price': current_price,
                        'shares': position,
                        'predicted_price': predicted_price,
                        'predicted_change': predicted_change * 100,
                        'revenue': revenue,
                        'profit': profit
                    })
                    
                    position = 0
                    position_price = 0
            
            # Calculate portfolio value
            portfolio_value = cash + (position * current_price if position > 0 else 0)
            portfolio_values.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'value': portfolio_value,
                'cash': cash,
                'holdings_value': position * current_price if position > 0 else 0,
                'price': current_price
            })
        
        # Close any remaining position at the end
        if position > 0:
            final_date = data_with_indicators.index[-1]
            final_price = data_with_indicators['Close'].iloc[-1]
            revenue = position * final_price * (1 - transaction_cost)
            profit = revenue - (position * position_price * (1 + transaction_cost))
            cash += revenue
            
            trades.append({
                'date': final_date.strftime('%Y-%m-%d'),
                'type': 'SELL (Close)',
                'price': final_price,
                'shares': position,
                'revenue': revenue,
                'profit': profit
            })
            
            position = 0
        
        # Calculate buy-and-hold benchmark
        benchmark_start_price = data_with_indicators['Close'].iloc[start_idx]
        benchmark_end_price = data_with_indicators['Close'].iloc[-1]
        benchmark_shares = int(initial_capital / (benchmark_start_price * (1 + transaction_cost)))
        benchmark_final_value = benchmark_shares * benchmark_end_price * (1 - transaction_cost)
        benchmark_return = ((benchmark_final_value - initial_capital) / initial_capital) * 100
        
        # Calculate metrics
        final_capital = cash
        total_return = ((final_capital - initial_capital) / initial_capital) * 100
        
        # Calculate win rate
        profitable_trades = [t for t in trades if t['type'] in ['SELL', 'SELL (Close)'] and t.get('profit', 0) > 0]
        total_closed_trades = len([t for t in trades if t['type'] in ['SELL', 'SELL (Close)']])
        win_rate = (len(profitable_trades) / total_closed_trades * 100) if total_closed_trades > 0 else 0
        
        # Calculate total profit/loss from trades
        total_profit = sum(t.get('profit', 0) for t in trades if t['type'] in ['SELL', 'SELL (Close)'])
        
        # Calculate Sharpe ratio (simplified)
        if len(portfolio_values) > 1:
            returns = []
            for i in range(1, len(portfolio_values)):
                ret = (portfolio_values[i]['value'] - portfolio_values[i-1]['value']) / portfolio_values[i-1]['value']
                returns.append(ret)
            
            if len(returns) > 0:
                returns_array = np.array(returns)
                avg_return = np.mean(returns_array)
                std_return = np.std(returns_array)
                sharpe_ratio = (avg_return / std_return * np.sqrt(252)) if std_return > 0 else 0
            else:
                sharpe_ratio = 0
        else:
            sharpe_ratio = 0
        
        # Calculate maximum drawdown
        if len(portfolio_values) > 0:
            values = [pv['value'] for pv in portfolio_values]
            peak = values[0]
            max_drawdown = 0
            
            for value in values:
                if value > peak:
                    peak = value
                drawdown = ((peak - value) / peak) * 100
                if drawdown > max_drawdown:
                    max_drawdown = drawdown
        else:
            max_drawdown = 0
        
        # Compile results
        results = {
            'symbol': symbol,
            'start_date': start_date,
            'end_date': end_date,
            'initial_capital': initial_capital,
            'final_capital': final_capital,
            'total_return_pct': round(total_return, 2),
            'total_profit': round(total_profit, 2),
            'benchmark_return_pct': round(benchmark_return, 2),
            'outperformance_pct': round(total_return - benchmark_return, 2),
            'total_trades': len(trades),
            'winning_trades': len(profitable_trades),
            'losing_trades': total_closed_trades - len(profitable_trades),
            'win_rate_pct': round(win_rate, 2),
            'sharpe_ratio': round(sharpe_ratio, 3),
            'max_drawdown_pct': round(max_drawdown, 2),
            'trades': trades,
            'portfolio_values': portfolio_values,
            'transaction_cost_pct': transaction_cost * 100,
            'confidence_threshold_pct': confidence_threshold * 100
        }
        
        self.results = results
        
        print(f"✅ Backtest complete!")
        print(f"   Total Return: {total_return:.2f}% | Benchmark: {benchmark_return:.2f}%")
        print(f"   Trades: {len(trades)} | Win Rate: {win_rate:.2f}%")
        
        return results
    
    def get_performance_summary(self) -> Dict:
        """
        Get a summary of backtest performance
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.results:
            return {"error": "No backtest results available"}
        
        return {
            'total_return': self.results['total_return_pct'],
            'benchmark_return': self.results['benchmark_return_pct'],
            'outperformance': self.results['outperformance_pct'],
            'win_rate': self.results['win_rate_pct'],
            'sharpe_ratio': self.results['sharpe_ratio'],
            'max_drawdown': self.results['max_drawdown_pct'],
            'total_trades': self.results['total_trades'],
            'final_capital': self.results['final_capital']
        }
    
    def get_trade_history(self, limit: int = 20) -> List[Dict]:
        """
        Get recent trade history
        
        Args:
            limit: Maximum number of trades to return
            
        Returns:
            List of recent trades
        """
        if not self.results:
            return []
        
        trades = self.results.get('trades', [])
        return trades[-limit:] if len(trades) > limit else trades
    
    def get_chart_data(self) -> Dict:
        """
        Get data formatted for charting
        
        Returns:
            Dictionary with chart data for portfolio value over time
        """
        if not self.results:
            return {"error": "No backtest results available"}
        
        portfolio_values = self.results.get('portfolio_values', [])
        
        # Calculate buy-and-hold for comparison
        if len(portfolio_values) > 0:
            start_price = portfolio_values[0]['price']
            initial_shares = self.results['initial_capital'] / start_price
            
            benchmark_values = [
                {
                    'date': pv['date'],
                    'value': initial_shares * pv['price']
                }
                for pv in portfolio_values
            ]
        else:
            benchmark_values = []
        
        return {
            'dates': [pv['date'] for pv in portfolio_values],
            'ai_strategy': [pv['value'] for pv in portfolio_values],
            'buy_hold_strategy': [bv['value'] for bv in benchmark_values],
            'initial_capital': self.results['initial_capital']
        }
    
    def save_results(self, filename: str = 'backtest_results.json'):
        """
        Save backtest results to file
        
        Args:
            filename: Output filename
        """
        if not self.results:
            print("No results to save")
            return
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"💾 Results saved to {filename}")


def compare_strategies(
    backtest_results: Dict,
    strategies: List[str] = ['AI', 'Buy-and-Hold']
) -> Dict:
    """
    Compare different trading strategies
    
    Args:
        backtest_results: Results from backtesting
        strategies: List of strategy names to compare
        
    Returns:
        Comparison metrics
    """
    comparison = {
        'AI Strategy': {
            'return': backtest_results['total_return_pct'],
            'sharpe': backtest_results['sharpe_ratio'],
            'max_drawdown': backtest_results['max_drawdown_pct'],
            'trades': backtest_results['total_trades']
        },
        'Buy-and-Hold': {
            'return': backtest_results['benchmark_return_pct'],
            'sharpe': 'N/A',
            'max_drawdown': 'N/A',
            'trades': 2  # Buy at start, sell at end
        }
    }
    
    return comparison
