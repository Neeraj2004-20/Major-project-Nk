"""
Quick Integration Guide for Adding LLM AI Features

This file shows how to integrate the LLM AI system into your existing application.
"""

# ============================================
# OPTION 1: FastAPI Integration
# ============================================
# Add this to your main serve.py or app.py file:

"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api_llm import router as ai_router, init_ai_system

# Create your FastAPI app
app = FastAPI(title="AI Market Predictor")

# Your existing endpoints
@app.get("/")
async def read_root():
    return {"message": "AI Market Predictor with LLM"}

# Initialize AI system
init_ai_system()

# Add AI endpoints - this adds all /api/ai/* endpoints
app.include_router(ai_router)

# Run with: uvicorn serve:app --reload
"""


# ============================================
# OPTION 2: Standalone Python Module
# ============================================
# Use this in any Python script:

"""
from ai_llm_integration import create_ai_intelligence
from sentiment_analyzer import SentimentAnalyzer

# Initialize systems
ai = create_ai_intelligence()
sentiment = SentimentAnalyzer()

# Analyze a stock
analysis = ai.analyze_stock(
    symbol="AAPL",
    current_price=150.75,
    predicted_price=158.50,
    sentiment_analyzer=sentiment,
    news_headlines=[
        "Apple stock rises on strong earnings",
        "New iPhone models receive positive reviews"
    ],
    confidence=0.82
)

# Chat with AI
response = ai.chat("What's the outlook for AAPL?")
print(response)

# Get market summary
summary = ai.get_market_summary(["AAPL", "MSFT", "GOOGL"])
print(summary)

# Get trading alerts
alerts = ai.get_trading_alerts(["AAPL", "MSFT"])
for alert in alerts:
    print(f"{alert['symbol']}: {alert['signal']}")

# Export analysis
ai.export_analysis("results.json")
"""


# ============================================
# OPTION 3: With Existing Prediction Model
# ============================================
# Integrate with your model.py predictions:

"""
import numpy as np
from model import StockPredictor
from ai_llm_integration import create_ai_intelligence
from sentiment_analyzer import SentimentAnalyzer

# Load your models
predictor = StockPredictor()
ai = create_ai_intelligence()
sentiment = SentimentAnalyzer()

# Get prediction for a stock
symbol = "AAPL"
current_price = 150.75
predicted_price = predictor.predict(symbol)

# Get sentiment
news = sentiment.fetch_news(symbol, "Apple")
sentiments = sentiment.analyze_multiple([n['title'] for n in news])
sentiment_score = np.mean([s['score'] for s in sentiments])

# Get technical indicators (from your existing code)
technical_indicators = {
    "RSI": 65,
    "MACD": 0.45,
    "SMA_20": 148.30,
}

# Get AI analysis
analysis = ai.analyze_stock(
    symbol=symbol,
    current_price=current_price,
    predicted_price=predicted_price,
    sentiment_analyzer=sentiment,
    technical_indicators=technical_indicators,
    news_headlines=[n['title'] for n in news[:5]],
    confidence=0.82
)

# Get recommendation
signal = analysis['signals']['signal']
print(f"AI Recommendation: {signal}")
print(f"Target Price: ${analysis['signals']['price_target']:.2f}")
print(f"Stop Loss: ${analysis['signals']['stop_loss']:.2f}")
"""


# ============================================
# OPTION 4: Web Dashboard Integration
# ============================================
# Add this to your frontend HTML:

"""
<!-- In your frontend.html or index.html -->

<div id="ai-analysis">
    <h2>AI Market Analysis</h2>
    <button onclick="analyzeStock()">Analyze</button>
    <button onclick="chatWithAI()">Chat</button>
    <button onclick="getAlerts()">Get Alerts</button>
    <div id="results"></div>
</div>

<script>
async function analyzeStock() {
    const response = await fetch('/api/ai/analyze', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            symbol: 'AAPL',
            current_price: 150.75,
            predicted_price: 158.50,
            confidence: 0.82
        })
    });
    const data = await response.json();
    console.log('Analysis:', data.data);
    document.getElementById('results').innerHTML = 
        `<pre>${JSON.stringify(data.data, null, 2)}</pre>`;
}

async function chatWithAI() {
    const response = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            message: 'What is the best trade for today?'
        })
    });
    const data = await response.json();
    console.log('Response:', data.response);
    document.getElementById('results').innerHTML = data.response;
}

async function getAlerts() {
    const response = await fetch('/api/ai/alerts?symbols=AAPL&symbols=MSFT');
    const data = await response.json();
    console.log('Alerts:', data.data);
    document.getElementById('results').innerHTML = 
        `<pre>${JSON.stringify(data.data, null, 2)}</pre>`;
}
</script>
"""


# ============================================
# OPTION 5: Batch Analysis Script
# ============================================
# Create a batch_analysis.py:

"""
from ai_llm_integration import create_ai_intelligence
import pandas as pd

# Initialize AI
ai = create_ai_intelligence()

# Load stock list
stocks_df = pd.read_csv('stocks_to_analyze.csv')

# Analyze each stock
results = []
for idx, row in stocks_df.iterrows():
    print(f"Analyzing {row['symbol']}...")
    
    analysis = ai.analyze_stock(
        symbol=row['symbol'],
        current_price=row['current_price'],
        predicted_price=row['predicted_price'],
        confidence=row.get('confidence', 0.75)
    )
    
    results.append({
        'symbol': row['symbol'],
        'signal': analysis['signals']['signal'],
        'target': analysis['signals']['price_target'],
        'stop_loss': analysis['signals']['stop_loss'],
        'confidence': analysis['confidence']
    })

# Export results
results_df = pd.DataFrame(results)
results_df.to_csv('analysis_results.csv', index=False)
print("✓ Analysis complete - saved to analysis_results.csv")

# Get market summary
summary = ai.get_market_summary(stocks_df['symbol'].tolist())
print(f"\nMarket Summary:")
print(f"  Buy Signals: {summary['buy_signals']}")
print(f"  Sell Signals: {summary['sell_signals']}")
print(f"  Market Bias: {summary['market_bias']}")
"""


# ============================================
# STEP-BY-STEP INTEGRATION
# ============================================

"""
1. INSTALL DEPENDENCIES:
   pip install -r requirements.txt
   
2. CONFIGURE LLM BACKEND:
   # Option A: Use default (HuggingFace - no setup needed)
   # Option B: Use Ollama
   #   - Install from https://ollama.ai
   #   - ollama pull mistral
   #   - ollama serve
   # Option C: Use Anthropic Claude
   #   - export ANTHROPIC_API_KEY="sk-..."

3. CHOOSE INTEGRATION METHOD:
   - FastAPI: Add to serve.py
   - Standalone: Use in Python scripts
   - With Models: Combine with predictor
   - Web: Add JavaScript endpoints
   - Batch: Create analysis script

4. TEST YOUR INTEGRATION:
   python demo_llm_features.py
   
   Or test API:
   curl -X POST http://localhost:8000/api/ai/analyze \\
     -H "Content-Type: application/json" \\
     -d '{"symbol":"AAPL","current_price":150.75,"predicted_price":158.50,"confidence":0.82}'

5. DEPLOY TO PRODUCTION:
   - Update requirements.txt with chosen LLM backend
   - Set environment variables
   - Configure API endpoints
   - Add monitoring/logging
   - Test thoroughly

6. MONITOR & OPTIMIZE:
   - Check /api/ai/health for system status
   - Monitor /api/ai/performance for metrics
   - Adjust LLM backend if needed
   - Export and review analysis trends
"""


# ============================================
# COMMON INTEGRATION PATTERNS
# ============================================

# Pattern 1: Decorator for AI Analysis
def with_ai_analysis(func):
    """Decorator to add AI analysis to prediction functions"""
    from ai_llm_integration import create_ai_intelligence
    ai = create_ai_intelligence()
    
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        symbol = kwargs.get('symbol')
        if symbol and result:
            analysis = ai.analyze_stock(
                symbol=symbol,
                current_price=result['current_price'],
                predicted_price=result['predicted_price']
            )
            result['ai_analysis'] = analysis
        return result
    return wrapper


# Pattern 2: Context Manager for Batch Analysis
class AIAnalyzer:
    """Context manager for batch analysis with AI"""
    def __init__(self):
        self.ai = None
        self.results = []
    
    def __enter__(self):
        from ai_llm_integration import create_ai_intelligence
        self.ai = create_ai_intelligence()
        return self
    
    def __exit__(self, *args):
        # Export results automatically
        self.ai.export_analysis("batch_analysis.json")
    
    def analyze(self, symbol, current_price, predicted_price):
        result = self.ai.analyze_stock(
            symbol=symbol,
            current_price=current_price,
            predicted_price=predicted_price
        )
        self.results.append(result)
        return result

# Usage:
# with AIAnalyzer() as analyzer:
#     for stock in stocks:
#         analyzer.analyze(stock['symbol'], stock['price'], stock['prediction'])


# Pattern 3: Async/Background Processing
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def analyze_stocks_async(stocks):
    """Analyze multiple stocks asynchronously"""
    from ai_llm_integration import create_ai_intelligence
    
    ai = create_ai_intelligence()
    executor = ThreadPoolExecutor(max_workers=4)
    
    async def analyze_one(stock):
        return await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: ai.analyze_stock(**stock)
        )
    
    results = await asyncio.gather(*[analyze_one(s) for s in stocks])
    return results


# ============================================
# TROUBLESHOOTING
# ============================================

"""
Q: Getting "ModuleNotFoundError"?
A: pip install -r requirements.txt

Q: LLM responses are slow?
A: Switch to Ollama or Anthropic backend

Q: Ollama not connecting?
A: 
   - Make sure ollama serve is running
   - Check OLLAMA_BASE_URL=http://localhost:11434
   - Run: ollama pull mistral

Q: Anthropic API errors?
A:
   - Verify ANTHROPIC_API_KEY is set
   - Check you have credits in account
   - Ensure key is correct

Q: Memory issues?
A:
   - Reduce ANALYSIS_CACHE_SIZE
   - Use smaller model (distilgpt2 instead of gpt2)
   - Run on GPU if available

Q: API returns empty response?
A:
   - Make sure init_ai_system() is called
   - Check logs for error messages
   - Verify market data is loaded
"""

print(__doc__)
