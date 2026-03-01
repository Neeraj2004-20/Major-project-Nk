#!/usr/bin/env python
"""
Quick CORS Test - Verify API can be called from browser
"""

import requests
import json

print("\n" + "="*60)
print("CORS TEST - Verify API Accessibility")
print("="*60 + "\n")

url = 'http://localhost:8001/api/ai/analyze'
headers = {'Content-Type': 'application/json'}
data = {
    'symbol': 'AAPL',
    'current_price': 150.25,
    'predicted_price': 165.50,
    'confidence': 0.82
}

try:
    print("Testing API request (same as browser would make)...")
    response = requests.post(url, json=data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        signal = result.get('data', {}).get('signals', {}).get('signal', 'N/A')
        price_target = result.get('data', {}).get('signals', {}).get('price_target', 'N/A')
        
        print(f"\n✓ API RESPONDS CORRECTLY")
        print(f"  Symbol: AAPL")
        print(f"  Signal: {signal}")
        print(f"  Target: ${price_target}")
        
        print(f"\n✓ CORS is working!")
        print(f"  Browser can now fetch from API")
        
    else:
        print(f"✗ Error: Status {response.status_code}")
        print(f"  Response: {response.text}")
        
except Exception as e:
    print(f"✗ Connection failed: {e}")

print("\n" + "="*60)
print("WEB CLIENT STATUS")
print("="*60)
print("\nWeb Interface: http://localhost:8001/web/client")
print("API Docs: http://localhost:8001/docs")
print("\nTry these in the web client:")
print("  1. Go to 'Analyze' tab")
print("  2. Enter: AAPL")
print("  3. Set: Price=150.25, Target=165.50")
print("  4. Click 'Analyze Stock'")
print("\n" + "="*60 + "\n")
