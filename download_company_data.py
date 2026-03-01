import yfinance as yf
import pandas as pd


companies = {
    'apple': 'AAPL',
    'microsoft': 'MSFT',
    'google': 'GOOGL',
    'amazon': 'AMZN',
    'meta': 'META',
    'tcs': 'TCS.NS',
    'hcl': 'HCLTECH.NS',
    'infosys': 'INFY.NS',
    'reliance': 'RELIANCE.NS',
    'wipro': 'WIPRO.NS'
}

start_date = '2015-01-01'
end_date = '2024-01-01'

for name, ticker in companies.items():
    print(f"Downloading data for {name.title()} ({ticker})...")
    data = yf.download(ticker, start=start_date, end=end_date)
    if not data.empty:
        csv_path = f"{name}.csv"
        data.to_csv(csv_path)
        print(f"Saved {csv_path}")
    else:
        print(f"No data found for {ticker}")
