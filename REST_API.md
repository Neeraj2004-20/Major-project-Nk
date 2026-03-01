# REST API Documentation

Complete REST API for AI Market Predictor with 10+ endpoints.

## Base URL
```
http://localhost:8000
```

## API Routes

### Web Interface
- `GET /` - Main dashboard
- `GET /web/client` - Interactive API client  
- `GET /web/swagger` - API documentation

---

## Analysis Endpoints

### POST /api/ai/analyze
Analyze a stock and get trading signals.

**Request:**
```json
{
  "symbol": "AAPL",
  "current_price": 150.75,
  "predicted_price": 158.50,
  "sentiment_score": 0.65,
  "technical_indicators": {
    "RSI": 65,
    "MACD": 0.45
  },
  "news_headlines": ["Apple beats earnings"],
  "confidence": 0.82
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "symbol": "AAPL",
    "timestamp": "2026-02-21T10:30:00",
    "signals": {
      "direction": "UP",
      "signal": "BUY",
      "strength": 0.85,
      "price_target": 158.50,
      "entry_price": 150.75,
      "stop_loss": 143.21,
      "profit_target": 165.00,
      "risk_level": "LOW"
    },
    "recommendations": ["Consider BUY position..."]
  }
}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/api/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "current_price": 150.75,
    "predicted_price": 158.50,
    "confidence": 0.82
  }'
```

---

### GET /api/ai/analyze/{symbol}
Get cached analysis for a symbol.

**Parameters:**
- `symbol` (string, path) - Stock symbol (e.g., "AAPL")

**Response:**
```json
{
  "status": "success",
  "data": { ... } // Same as POST response
}
```

**cURL:**
```bash
curl http://localhost:8000/api/ai/analyze/AAPL
```

---

## Chat Endpoints

### POST /api/ai/chat
Chat with AI analyst.

**Request:**
```json
{
  "message": "What's the outlook for AAPL?"
}
```

**Response:**
```json
{
  "status": "success",
  "response": "AAPL shows strong bullish momentum...",
  "timestamp": "2026-02-21T10:30:00"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze AAPL"}'
```

**Python:**
```python
import requests
response = requests.post(
    'http://localhost:8000/api/ai/chat',
    json={'message': 'What should I trade?'}
)
print(response.json()['response'])
```

---

### GET /api/ai/conversation-history
Get conversation history.

**Parameters:**
- `limit` (integer, query) - Number of recent conversations (default: 10, max: 100)

**Response:**
```json
{
  "status": "success",
  "total": 10,
  "data": [
    {
      "user": "What's the market outlook?",
      "assistant": "The market shows...",
      "timestamp": "2026-02-21T10:30:00",
      "intent": "analyze"
    }
  ]
}
```

**cURL:**
```bash
curl "http://localhost:8000/api/ai/conversation-history?limit=20"
```

---

## Market Endpoints

### POST /api/ai/market-summary
Get market summary across multiple stocks.

**Request:**
```json
{
  "symbols": ["AAPL", "MSFT", "GOOGL"]
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_symbols": 3,
    "buy_signals": 2,
    "sell_signals": 1,
    "hold_signals": 0,
    "market_bias": "BULLISH",
    "average_confidence": 0.78,
    "insights": [
      "📈 Bullish bias with 2 buy signals detected"
    ],
    "recommendations": [
      "Diversify across multiple sectors",
      "Use stop losses on all positions"
    ]
  }
}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/api/ai/market-summary \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["AAPL", "MSFT", "GOOGL"]}'
```

---

### GET /api/ai/alerts
Get trading alerts for symbols.

**Parameters:**
- `symbols` (string[], query) - List of stock symbols

**Response:**
```json
{
  "status": "success",
  "total_alerts": 2,
  "data": [
    {
      "symbol": "AAPL",
      "signal": "BUY",
      "strength": 0.85,
      "price_target": 158.50,
      "entry_price": 150.75,
      "stop_loss": 143.21,
      "confidence": 0.82,
      "action": "BUY at $150.75",
      "take_profit": 165.00
    }
  ]
}
```

**cURL:**
```bash
curl "http://localhost:8000/api/ai/alerts?symbols=AAPL&symbols=MSFT&symbols=GOOGL"
```

---

## System Endpoints

### GET /api/ai/health
System health check.

**Response:**
```json
{
  "status": "healthy",
  "models": {
    "analyst": "huggingface",
    "conversation": "active"
  },
  "timestamp": "2026-02-21T10:30:00"
}
```

**cURL:**
```bash
curl http://localhost:8000/api/ai/health
```

---

### GET /api/ai/info
System information.

**Response:**
```json
{
  "system": "AI Market Intelligence",
  "version": "1.0.0",
  "components": {
    "analyst": {
      "type": "huggingface",
      "description": "LLM-powered market analyst"
    },
    "conversation": {
      "type": "conversational_agent",
      "description": "Interactive chat for market insights"
    }
  },
  "features": [
    "Stock analysis with LLM insights",
    "Trading signals and recommendations",
    ...
  ],
  "endpoints": [10 endpoints listed]
}
```

**cURL:**
```bash
curl http://localhost:8000/api/ai/info
```

---

### GET /api/ai/performance
Performance metrics.

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_analyses": 42,
    "buy_signals": 28,
    "sell_signals": 10,
    "hold_signals": 4,
    "buy_ratio": 0.67,
    "average_confidence": 0.78,
    "unique_symbols": 15
  }
}
```

**cURL:**
```bash
curl http://localhost:8000/api/ai/performance
```

---

### POST /api/ai/export
Export analysis data.

**Parameters (query):**
- `filepath` (string) - Where to save file
- `format` (string) - "json" or "csv" (default: "json")

**Response:**
```json
{
  "status": "success",
  "message": "Analysis exported to results.json",
  "format": "json"
}
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/ai/export?filepath=results.json&format=json"
```

---

## Usage Examples

### Python Client

```python
from rest_api_client import AIMarketAPIClient

# Create client
client = AIMarketAPIClient()

# Analyze stock
result = client.analyze("AAPL", 150.75, 158.50)
print(f"Signal: {result['data']['signals']['signal']}")

# Chat
response = client.chat("What's the market outlook?")
print(response)

# Get alerts
alerts = client.get_alerts(["AAPL", "MSFT"])
for alert in alerts:
    print(f"{alert['symbol']}: {alert['signal']}")

# Market summary
summary = client.get_market_summary(["AAPL", "MSFT"])
print(f"Market bias: {summary['data']['market_bias']}")

# Performance
perf = client.get_performance()
print(f"Total analyses: {perf['total_analyses']}")
```

### JavaScript Client

```javascript
// Quick analyze
const response = await fetch('http://localhost:8000/api/ai/analyze', {
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
console.log(data.data.signals.signal);

// Quick chat
const chatResp = await fetch('http://localhost:8000/api/ai/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: 'Analyze AAPL'})
});
const chatData = await chatResp.json();
console.log(chatData.response);
```

### cURL Script

```bash
#!/bin/bash

# Analyze
curl -X POST http://localhost:8000/api/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol":"AAPL","current_price":150.75,"predicted_price":158.50,"confidence":0.82}'

# Chat
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What should I trade?"}'

# Alerts
curl "http://localhost:8000/api/ai/alerts?symbols=AAPL&symbols=MSFT"

# Health
curl http://localhost:8000/api/ai/health
```

---

## Error Handling

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

**400 Bad Request** - Missing or invalid parameters
```json
{"detail": "Invalid stock symbol"}
```

**404 Not Found** - Endpoint or resource not found
```json
{"detail": "No analysis cached for AAPL"}
```

**500 Internal Server Error** - Server error
```json
{"detail": "LLM analysis failed"}
```

---

## Rate Limiting & Performance

- No rate limiting by default
- Analyses are cached (same symbol returns cached result)
- Batch requests supported (POST /market-summary)
- Average response time: 500ms - 3s depending on LLM backend

---

## Authentication

Currently no authentication required. For production, add JWT or API key authentication.

---

## CORS

CORS is enabled for all origins. Configure in production:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing

### Interactive Web Client
Open: `http://localhost:8000/web/client`

### API Documentation
Open: `http://localhost:8000/docs` (Swagger UI)

### Documentation
Open: `http://localhost:8000/web/swagger` (ReDoc)

### Python Testing
```bash
python rest_api_client.py
```

---

## Integration

### With Existing FastAPI App
```python
from api_llm import router, init_ai_system
from web_api_client import web_router

app = FastAPI()
init_ai_system()
app.include_router(router)
app.include_router(web_router)
```

### Standalone Python Module
```python
from rest_api_client import create_client

client = create_client()
result = client.analyze("AAPL", 150, 160)
```

---

## Support

- **Web Client:** `/web/client`
- **API Docs:** `/docs`
- **Status:** `/api/ai/health`
- **Info:** `/api/ai/info`

---

**API Version:** 1.0.0
**Last Updated:** February 2026
