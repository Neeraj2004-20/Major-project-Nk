import requests
import os

# Create logos directory if it doesn't exist
os.makedirs('logos', exist_ok=True)

# Real company logo URLs from trusted CDNs
logos = {
    'RELIANCE.NS': 'https://logo.clearbit.com/ril.com',
    'TCS.NS': 'https://logo.clearbit.com/tcs.com',
    'INFY.NS': 'https://logo.clearbit.com/infosys.com',
    'HDFCBANK.NS': 'https://logo.clearbit.com/hdfcbank.com',
    'LT.NS': 'https://logo.clearbit.com/larsentoubro.com',
    'TATASTEEL.NS': 'https://logo.clearbit.com/tatasteel.com',
    'VEDL.NS': 'https://logo.clearbit.com/vedantalimited.com',
    'ZEEL.NS': 'https://logo.clearbit.com/zeel.com',
    'YESBANK.NS': 'https://logo.clearbit.com/yesbank.in',
    'ADANIPORTS.NS': 'https://logo.clearbit.com/adani.com',
    'BAJFINANCE.NS': 'https://logo.clearbit.com/bajajfinserv.in',
    'ASIANPAINT.NS': 'https://logo.clearbit.com/asianpaints.com',
    'MARUTI.NS': 'https://logo.clearbit.com/marutisuzuki.com',
    'HINDUNILVR.NS': 'https://logo.clearbit.com/hul.co.in',
    'WIPRO.NS': 'https://logo.clearbit.com/wipro.com',
    'ICICIBANK.NS': 'https://logo.clearbit.com/icicibank.com',
    'SBIN.NS': 'https://logo.clearbit.com/sbi.co.in',
    'BHARTIARTL.NS': 'https://logo.clearbit.com/airtel.in',
    'ITC.NS': 'https://logo.clearbit.com/itcportal.com',
    'TATAMOTORS.NS': 'https://logo.clearbit.com/tatamotors.com'
}

print("🎨 Downloading real company logos...")
print("=" * 50)

for symbol, url in logos.items():
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Save as PNG
            filename = f'logos/{symbol}.png'
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ {symbol.ljust(20)} - Downloaded!")
        else:
            print(f"⚠️  {symbol.ljust(20)} - Not found, using fallback")
    except Exception as e:
        print(f"❌ {symbol.ljust(20)} - Error: {str(e)[:30]}")

print("=" * 50)
print("✨ Logo download complete!")
print(f"📁 Saved to: {os.path.abspath('logos')}")
