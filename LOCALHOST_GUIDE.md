# 🚀 Local Server Setup Guide

## Quick Start

### Windows
**Double-click to start:**
```
run_server.bat
```

Or in PowerShell:
```powershell
python run_local_server.py
```

### Mac/Linux
```bash
python run_local_server.py
```

---

## What This Does

Starts a local FastAPI server with:
- ✅ Web interface at `http://localhost:8000`
- ✅ Interactive API docs at `http://localhost:8000/docs`
- ✅ 10 REST API endpoints
- ✅ LLM-powered analysis
- ✅ Real-time chat
- ✅ Trading alerts

---

## Access Points

| URL | Purpose |
|-----|---------|
| `http://localhost:8000` | Web interface |
| `http://localhost:8000/docs` | Interactive API (Swagger) |
| `http://localhost:8000/redoc` | API Documentation (ReDoc) |
| `http://localhost:8000/api/ai/*` | API endpoints |

---

## API Endpoints

### Analysis
```bash
# Analyze a stock
curl -X POST http://localhost:8000/api/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "current_price": 150.75,
    "predicted_price": 158.50,
    "confidence": 0.82
  }'
```

### Chat
```bash
# Chat with AI
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your analysis for AAPL?"}'
```

### Alerts
```bash
# Get trading alerts
curl "http://localhost:8000/api/ai/alerts?symbols=AAPL&symbols=MSFT"
```

### Market Summary
```bash
# Get market summary
curl -X POST http://localhost:8000/api/ai/market-summary \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["AAPL", "MSFT", "GOOGL"]}'
```

### System Info
```bash
# Check health
curl http://localhost:8000/api/ai/health

# Get system info
curl http://localhost:8000/api/ai/info
```

---

## Browser Testing

### 1. Web Interface
Open: `http://localhost:8000`
- Beautiful dashboard
- Feature overview
- Links to API docs

### 2. Interactive API (Swagger UI)
Open: `http://localhost:8000/docs`
- Try endpoints directly
- See request/response format
- Test with different parameters

### 3. API Documentation (ReDoc)
Open: `http://localhost:8000/redoc`
- Full endpoint documentation
- Parameter descriptions
- Example responses

---

## Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Analyze stock
response = requests.post(
    f"{BASE_URL}/api/ai/analyze",
    json={
        "symbol": "AAPL",
        "current_price": 150.75,
        "predicted_price": 158.50,
        "confidence": 0.82
    }
)
print(response.json())

# Chat
response = requests.post(
    f"{BASE_URL}/api/ai/chat",
    json={"message": "What should I trade?"}
)
print(response.json())

# Get alerts
response = requests.get(
    f"{BASE_URL}/api/ai/alerts",
    params={"symbols": ["AAPL", "MSFT"]}
)
print(response.json())
```

---

## JavaScript Client Example

```javascript
// Analyze stock
fetch('http://localhost:8000/api/ai/analyze', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        symbol: 'AAPL',
        current_price: 150.75,
        predicted_price: 158.50,
        confidence: 0.82
    })
})
.then(r => r.json())
.then(data => console.log(data))

// Chat
fetch('http://localhost:8000/api/ai/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: 'Analyze AAPL'})
})
.then(r => r.json())
.then(data => console.log(data.response))

// Get alerts
fetch('http://localhost:8000/api/ai/alerts?symbols=AAPL&symbols=MSFT')
    .then(r => r.json())
    .then(data => console.log(data.data))
```

---

## Troubleshooting

**Error: Port 8000 already in use**
```bash
# Change port in run_local_server.py:
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use 8001 instead
```

**Error: Module not found**
```bash
pip install -r requirements.txt
```

**Slow responses**
- Switch LLM backend (Ollama is faster)
- Edit `LLM_CONFIG.env`

**Server won't start**
- Check Python installation: `python --version`
- Check port availability: `netstat -an | grep 8000`
- Try different port: change port in script

---

## Stopping Server

Press `CTRL+C` in the terminal

---

## Features You Can Test

### 1. Stock Analysis
Input stock data → Get trading signal + insights

### 2. Trading Signals
- BUY, SELL, or HOLD
- Price target
- Entry/exit points
- Risk assessment

### 3. Chat
- Ask questions naturally
- Get market insights
- Get recommendations

### 4. Alerts
- Sorted by signal strength
- Entry/exit prices
- Risk levels

### 5. Market Summary
- Overall market bias
- Multiple stocks analyzed
- Portfolio recommendations

### 6. Performance Metrics
- Analysis statistics
- Signal distribution
- Confidence levels

---

## Next Steps

1. ✅ Start server: `python run_local_server.py`
2. ✅ Open: `http://localhost:8000`
3. ✅ Test API at: `http://localhost:8000/docs`
4. ✅ Read docs: `http://localhost:8000/docs`
5. ✅ Integrate into your app

---

## Production Deployment

When ready for production:

```bash
# Use gunicorn for production
gunicorn -w 4 -k uvicorn.workers.UvicornWorker run_local_server:app

# Or use Docker
docker build -t ai-predictor .
docker run -p 8000:8000 ai-predictor
```

---

## API Response Examples

### Analysis Response
```json
{
  "status": "success",
  "data": {
    "symbol": "AAPL",
    "signals": {
      "signal": "BUY",
      "strength": 0.85,
      "price_target": 158.50,
      "stop_loss": 143.21
    },
    "recommendations": [
      "Consider BUY position at $150.75",
      "Set profit target at $165.00"
    ]
  }
}
```

### Chat Response
```json
{
  "status": "success",
  "response": "AAPL shows strong bullish momentum...",
  "timestamp": "2026-02-21T10:30:00"
}
```

### Alerts Response
```json
{
  "status": "success",
  "total_alerts": 2,
  "data": [
    {
      "symbol": "AAPL",
      "signal": "BUY",
      "strength": 0.85,
      "action": "BUY at $150.75",
      "take_profit": 165.00,
      "stop_loss": 143.21
    }
  ]
}
```

---

## Performance Tips

1. **Cache enabled** - Analyses cached by symbol
2. **Batch processing** - Analyze multiple stocks at once
3. **Async support** - Non-blocking API calls
4. **Smart detection** - LLM backend auto-selected

---

## Monitoring

Check system health:
```bash
curl http://localhost:8000/api/ai/health
```

Get performance metrics:
```bash
curl http://localhost:8000/api/ai/performance
```

---

**Happy trading! 📈🚀**

Server running at: `http://localhost:8000`
