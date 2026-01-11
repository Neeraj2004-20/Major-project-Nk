import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

def download_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(symbol, start=start, end=end)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df = df.dropna()
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize features
    return (df - df.mean()) / df.std()

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add advanced technical indicators for better predictions"""
    df = df.copy()
    
    # Moving Averages
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    
    # MACD
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    
    # RSI (Relative Strength Index)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    bb_middle = df['Close'].rolling(window=20).mean()
    bb_std = df['Close'].rolling(window=20).std()
    df['BB_Middle'] = bb_middle
    df['BB_Upper'] = bb_middle + (bb_std * 2)
    df['BB_Lower'] = bb_middle - (bb_std * 2)
    df['BB_Width'] = df['BB_Upper'] - df['BB_Lower']
    
    # Price momentum
    df['Momentum'] = df['Close'] - df['Close'].shift(4)
    df['ROC'] = ((df['Close'] - df['Close'].shift(10)) / df['Close'].shift(10)) * 100
    
    # Volume indicators
    volume_sma = df['Volume'].rolling(window=20).mean()
    df['Volume_SMA'] = volume_sma
    df['Volume_Ratio'] = df['Volume'] / volume_sma
    
    # Volatility
    df['Volatility'] = df['Close'].rolling(window=10).std()
    
    # Price range indicators
    df['Daily_Range'] = df['High'] - df['Low']
    df['Daily_Return'] = df['Close'].pct_change()
    
    # ATR (Average True Range)
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['ATR'] = true_range.rolling(window=14).mean()
    
    # Drop NaN values created by indicators
    df = df.dropna()
    
    return df

def create_sequences(data, seq_length, target_col_idx=3):
    """Create sequences for time series prediction"""
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length, target_col_idx])  # Predict Close price
    return np.array(X), np.array(y)

def load_and_preprocess_data(symbol, start_date, end_date, sequence_length, use_technical_indicators=True):
    """Load, preprocess, and split data with optional technical indicators"""
    # Download data
    df = download_data(symbol, start_date, end_date)
    
    # Add technical indicators
    if use_technical_indicators:
        df = add_technical_indicators(df)
        print(f"✨ Added technical indicators. Features: {df.shape[1]}")
    
    # Find Close column index
    close_idx = df.columns.get_loc('Close')
    
    # Scale data
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df.values)
    
    # Create sequences
    X, y = create_sequences(scaled_data, sequence_length, target_col_idx=close_idx)
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )
    
    print(f"📊 Data shape - X_train: {X_train.shape}, X_test: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test, scaler

if __name__ == "__main__":
    symbol = "AAPL"
    start = "2015-01-01"
    end = "2024-01-01"
    df = download_data(symbol, start, end)
    df_enhanced = add_technical_indicators(df)
    print(df_enhanced.head())
    print(f"\nFeatures: {df_enhanced.columns.tolist()}")
