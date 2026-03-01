# AI/LLM Market Intelligence - Complete Guide

## Overview

Your AI Market Predictor now includes **powerful LLM-enhanced AI capabilities** for:
- 🤖 **LLM-powered market analysis** with intelligent insights
- 💬 **Conversational AI** for interactive market queries
- 📊 **Advanced trading signals** based on ML + LLM
- 📈 **Market sentiment integration** with AI analysis
- 🎯 **Automated recommendations** and alerts

## New Components

### 1. **LLM Market Analyst** (`llm_market_analyst.py`)
Intelligent market analysis using Large Language Models

**Features:**
- Multi-backend support: HuggingFace, Ollama, Anthropic Claude
- Analyzes price predictions, technical indicators, sentiment
- Generates human-readable market insights
- Provides structured trading signals
- Risk assessment and recommendations

**Usage:**
```python
from llm_market_analyst import create_analyst, MarketAnalysisInput

# Create analyst (auto-selects best available backend)
analyst = create_analyst()

# Prepare analysis input
analysis_input = MarketAnalysisInput(
    symbol="AAPL",
    current_price=150.75,
    predicted_price=158.50,
    sentiment_score=0.65,
    technical_indicators={
        "RSI": 65,
        "MACD": 0.45,
        "SMA_20": 148.30,
        "Volatility": 0.018
    },
    news_headlines=["Apple beats earnings", "Strong iPhone demand"],
    historical_data={},
    confidence=0.82
)

# Get analysis
analysis = analyst.analyze(analysis_input)
print(f"Signal: {analysis['signals']['signal']}")
print(f"Target: ${analysis['signals']['price_target']:.2f}")
```

### 2. **AI Conversation Agent** (`ai_conversation.py`)
Interactive conversational interface for market insights

**Features:**
- Natural language understanding
- Intent detection (analyze, predict, sentiment, signal, help)
- Context-aware responses
- Conversation history tracking
- Export conversation

**Usage:**
```python
from ai_conversation import create_conversation_agent

agent = create_conversation_agent()
agent.set_market_data(market_data_dict)

# Chat with the agent
response = agent.chat("What's the prediction for AAPL?")
print(response)

# Get history
history = agent.get_conversation_history(limit=10)

# Save conversation
agent.save_conversation("chat_history.json")
```

### 3. **AI Market Intelligence** (`ai_llm_integration.py`)
Unified system combining all AI capabilities

**Features:**
- Centralized AI system management
- Market analysis with context
- Trading alerts and summaries
- Performance metrics
- Data export/import

**Usage:**
```python
from ai_llm_integration import create_ai_intelligence

ai = create_ai_intelligence()

# Analyze stock
analysis = ai.analyze_stock(
    symbol="AAPL",
    current_price=150.75,
    predicted_price=158.50,
    technical_indicators={...},
    news_headlines=[...],
    confidence=0.82
)

# Chat
response = ai.chat("What's happening with AAPL?")

# Get market summary
summary = ai.get_market_summary(["AAPL", "MSFT", "GOOGL"])

# Get alerts
alerts = ai.get_trading_alerts(["AAPL", "MSFT"])

# Export
ai.export_analysis("analysis.json")
```

### 4. **API Endpoints** (`api_llm.py`)
FastAPI endpoints for the AI system

**Endpoints:**
```
POST   /api/ai/analyze              - Analyze stock
GET    /api/ai/analyze/{symbol}     - Get cached analysis
POST   /api/ai/chat                 - Chat with analyst
GET    /api/ai/conversation-history - Get chat history
POST   /api/ai/market-summary       - Market overview
GET    /api/ai/alerts               - Trading alerts
GET    /api/ai/performance          - Performance metrics
POST   /api/ai/export               - Export analysis
GET    /api/ai/health               - Health check
GET    /api/ai/info                 - System info
```

## Backend Options

The system automatically selects the best available LLM backend:

### 1. **HuggingFace Transformers** (Default - No API key needed)
- **Model:** DistilGPT2 or custom
- **Pros:** Free, runs locally, no API calls
- **Cons:** Medium quality, slower
- **Setup:** Already included in requirements.txt

### 2. **Ollama** (Recommended for local use)
- **Model:** Mistral, Llama 2, or others
- **Pros:** Fast, completely local, good quality
- **Cons:** Requires Ollama installation
- **Setup:**
  ```bash
  # Install Ollama from https://ollama.ai
  ollama pull mistral
  ollama serve
  ```

### 3. **Anthropic Claude** (Best quality - Paid)
- **Model:** Claude 3 Haiku
- **Pros:** Highest quality, fastest
- **Cons:** Requires API key and credit
- **Setup:**
  ```bash
  # Set environment variable
  export ANTHROPIC_API_KEY="sk-..."
  ```

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Choose your LLM backend:**

**For HuggingFace (default):**
```bash
# No extra steps needed - transformers already in requirements
```

**For Ollama (recommended):**
```bash
# Install Ollama
# Then uncomment ollama line in requirements.txt
pip install ollama>=0.1.0

# Start Ollama in another terminal
ollama serve

# Pull a model
ollama pull mistral
```

**For Anthropic:**
```bash
# Uncomment anthropic line in requirements.txt
pip install anthropic>=0.7.0

# Set API key
export ANTHROPIC_API_KEY="your-key-here"
```

## Usage Examples

### Example 1: Simple Stock Analysis
```python
from ai_llm_integration import create_ai_intelligence

ai = create_ai_intelligence()

# Analyze AAPL
analysis = ai.analyze_stock(
    symbol="AAPL",
    current_price=150.75,
    predicted_price=158.50,
    confidence=0.82
)

print(analysis['signals']['signal'])  # BUY, SELL, or HOLD
print(analysis['recommendations'])
```

### Example 2: Market Conversation
```python
ai = create_ai_intelligence()

# Pre-load some data
ai.analyze_stock('AAPL', 150.75, 158.50, confidence=0.82)
ai.analyze_stock('MSFT', 380, 392, confidence=0.75)

# Chat
print(ai.chat("What's the outlook for AAPL?"))
print(ai.chat("Which stock is stronger?"))
print(ai.chat("Show me trading signals"))
```

### Example 3: API Usage
```bash
# Analyze stock
curl -X POST http://localhost:8000/api/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "current_price": 150.75,
    "predicted_price": 158.50,
    "confidence": 0.82
  }'

# Chat
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your analysis for AAPL?"}'

# Get alerts
curl "http://localhost:8000/api/ai/alerts?symbols=AAPL&symbols=MSFT"
```

## Running Demos

```bash
python demo_llm_features.py
```

This runs all demo scenarios:
1. Basic stock analysis
2. Conversational interaction
3. Market summary
4. Trading alerts
5. Sentiment integration
6. Performance metrics
7. Export/import

## Integrating with Main App

To add LLM features to your main application:

### Option 1: Standalone Module
```python
from ai_llm_integration import create_ai_intelligence

# In your main app
ai_system = create_ai_intelligence()

# Use it wherever needed
analysis = ai_system.analyze_stock(...)
response = ai_system.chat(...)
```

### Option 2: FastAPI Integration
```python
from fastapi import FastAPI
from api_llm import router, init_ai_system

app = FastAPI()

# Initialize AI system
init_ai_system()

# Include routes
app.include_router(router)

# Now you have all /api/ai/* endpoints
```

### Option 3: Combined with Existing API
```python
# In your serve.py or main FastAPI file
from fastapi import FastAPI
from api_llm import router as ai_router, init_ai_system

app = FastAPI()

# Your existing routes...
app.include_router(existing_routes)

# Add AI routes
init_ai_system()
app.include_router(ai_router)
```

## Output Examples

### Trading Signal Output
```json
{
  "symbol": "AAPL",
  "signal": "BUY",
  "strength": 0.85,
  "entry_price": 150.75,
  "price_target": 158.50,
  "stop_loss": 143.21,
  "profit_target": 165.00,
  "risk_level": "LOW"
}
```

### Market Summary Output
```json
{
  "total_symbols": 4,
  "buy_signals": 3,
  "sell_signals": 1,
  "hold_signals": 0,
  "market_bias": "BULLISH",
  "average_confidence": 0.78,
  "insights": [
    "📈 Bullish bias with 3 buy signals detected",
    "💪 Strong signal strength across the board"
  ],
  "recommendations": [
    "✅ Diversify across multiple sectors",
    "✅ Use stop losses on all positions",
    "✅ Don't risk more than 2% per trade"
  ]
}
```

## Performance & Optimization

### Caching
- Analyses are cached by symbol for quick retrieval
- Reduces redundant LLM calls
- `ai.analysis_cache[symbol]` stores results

### Batch Processing
```python
# Analyze multiple stocks efficiently
analyses = [
    MarketAnalysisInput(symbol="AAPL", ...),
    MarketAnalysisInput(symbol="MSFT", ...),
]
results = analyst.analyze_batch(analyses)
```

### Backend Performance
- **HuggingFace:** ~2-3 sec per analysis
- **Ollama:** ~1-2 sec per analysis
- **Anthropic:** ~500ms per analysis

## Troubleshooting

### Issue: "No module named 'transformers'"
**Solution:**
```bash
pip install transformers>=4.35.0
```

### Issue: Ollama connection failed
**Solution:**
```bash
# Make sure Ollama is running
ollama serve

# In another terminal
ollama pull mistral
```

### Issue: ANTHROPIC_API_KEY not found
**Solution:**
```bash
export ANTHROPIC_API_KEY="sk-..."
# Or add to .env file
```

### Issue: LLM responses too slow
**Solution:**
- Use Ollama for local speed
- Or use Anthropic Claude for cloud speed
- Adjust model size (smaller = faster)

## Advanced Usage

### Custom Prompts
```python
analyst = create_analyst()
custom_prompt = analyst._build_analysis_prompt(analysis_input)
# Modify prompt before analysis
```

### Sentiment Integration
```python
from sentiment_analyzer import SentimentAnalyzer

sentiment = SentimentAnalyzer()
sentiments = sentiment.analyze_multiple(headlines)
sentiment_score = np.mean([s['score'] for s in sentiments])
```

### Export and Analysis
```python
ai.export_analysis("my_analysis.json", format="json")
data = ai.import_market_data("my_analysis.json")
```

## Configuration

Set environment variables for customization:

```bash
# Choose LLM backend (auto, huggingface, ollama, anthropic)
export LLM_BACKEND="ollama"

# HuggingFace model
export HF_MODEL="distilgpt2"

# Ollama model
export OLLAMA_MODEL="mistral"

# Anthropic API key
export ANTHROPIC_API_KEY="sk-..."

# NewsAPI key (for sentiment)
export NEWSAPI_KEY="..."
```

## Best Practices

1. **Always use stop losses** when trading
2. **Risk only 2% per trade** of your account
3. **Diversify across sectors** - don't put all in one stock
4. **Monitor sentiment shifts** - news can change fast
5. **Use proper position sizing** based on risk/reward
6. **Keep trading logs** - review what worked and what didn't
7. **Don't over-trade** - wait for clear signals
8. **Update models regularly** with new data

## Support & Resources

- **GitHub Issues:** Report bugs or request features
- **Documentation:** Check individual module docstrings
- **Examples:** Run `demo_llm_features.py` for full examples
- **API Docs:** Visit `http://localhost:8000/docs` when API is running

## License & Attribution

This LLM integration is part of the AI Market Predictor project.

**Backend Attribution:**
- HuggingFace Transformers: https://huggingface.co/
- Ollama: https://ollama.ai/
- Anthropic Claude: https://anthropic.com/

## Next Steps

1. ✅ Install dependencies
2. ✅ Choose your LLM backend
3. ✅ Run demo: `python demo_llm_features.py`
4. ✅ Integrate into your main app
5. ✅ Start analyzing and trading!

---

**Happy trading with AI! 🚀📈**
