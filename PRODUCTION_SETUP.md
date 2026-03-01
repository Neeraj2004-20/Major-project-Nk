# 🚀 Production-Ready Server Setup Guide

## 📋 Overview

Your server now includes enterprise-grade features:
- ✅ Health checks & system monitoring
- ✅ Rate limiting & request validation
- ✅ Structured logging & performance tracking
- ✅ Error handling & custom exceptions
- ✅ Optional database persistence
- ✅ Optional caching (Redis/Memory)
- ✅ Optional authentication
- ✅ WebSocket support
- ✅ Detailed metrics dashboard

---

## 🔧 Quick Start

### 1. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Optional Features (Recommended)

```bash
# For database persistence
pip install sqlalchemy

# For caching
pip install redis

# For system monitoring
pip install psutil

# All optional features
pip install -r requirements-optional.txt
```

### 3. Configure Environment

Edit `.env` file to customize:

```env
# Server
PORT=5501
ENV=development
DEBUG=true
LOG_LEVEL=INFO

# Security
API_RATE_LIMIT=100
RATE_LIMIT_WINDOW=60

# Features
ENABLE_CACHING=true
ENABLE_WEBSOCKET=true
ENABLE_MONITORING=true
```

### 4. Start the Server

```bash
python run_local_server.py
```

---

## 📊 Available Endpoints

### System Health & Monitoring

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | System health status |
| `/metrics` | GET | Performance metrics & stats |
| `/api/status` | GET | API operational status |
| `/docs` | GET | Interactive API documentation |
| `/redoc` | GET | API documentation (ReDoc) |

### Example Requests

```bash
# Check health
curl http://localhost:5501/health

# Get metrics
curl http://localhost:5501/metrics

# Check status
curl http://localhost:5501/api/status
```

---

## ⚙️ Configuration Details

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | true | Enable debug mode |
| `HOST` | 0.0.0.0 | Server host |
| `PORT` | 5501 | Server port |
| `ENV` | development | Environment (development/production) |
| `LOG_LEVEL` | INFO | Logging level (DEBUG/INFO/WARNING/ERROR) |
| `API_RATE_LIMIT` | 100 | Max requests per window |
| `RATE_LIMIT_WINDOW` | 60 | Rate limit window in seconds |
| `ENABLE_CORS` | true | Enable CORS |
| `ENABLE_CACHING` | true | Enable caching |
| `ENABLE_MONITORING` | true | Enable performance monitoring |
| `CACHE_TYPE` | memory | Cache backend (memory/redis) |

### Example: Strict Rate Limiting

```env
API_RATE_LIMIT=50
RATE_LIMIT_WINDOW=60
```

### Example: Production Settings

```env
ENV=production
DEBUG=false
LOG_LEVEL=WARNING
ENABLE_CORS=false
CACHE_TYPE=redis
```

---

## 📈 Performance Monitoring

### Real-Time Metrics

Access `http://localhost:5501/metrics` to view:
- Total requests processed
- Average response times per endpoint
- Min/Max response times
- Status code distribution
- Error counts & types

### Example Response

```json
{
  "performance": {
    "total_requests": 156,
    "endpoints": {
      "/api/predict": {
        "count": 42,
        "avg_duration": 0.245,
        "min_duration": 0.102,
        "max_duration": 1.523
      }
    },
    "status_codes": {
      "200": 150,
      "400": 4,
      "500": 2
    },
    "errors_count": 2
  },
  "health": { ... }
}
```

---

## 🔐 Security Features

### Rate Limiting

Prevents abuse by limiting requests:

```python
# Default: 100 requests per 60 seconds per IP
API_RATE_LIMIT=100
RATE_LIMIT_WINDOW=60
```

Response when limit exceeded:
```json
{
  "detail": "Too many requests. Max 100 per 60s"
}
```

### Request Validation

All inputs validated using Pydantic models:
- Type validation
- Range validation
- Format validation
- Automatic documentation

---

## 💾 Database (Optional)

### Setup SQLite (Default)

Already configured, just run:
```bash
python run_local_server.py
```

### Use PostgreSQL

1. Install: `pip install sqlalchemy psycopg2-binary`
2. Update `.env`:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```
3. Tables auto-create on startup

### Database Models

- `Prediction` - Stock predictions
- `APIKey` - API key management
- `UserSession` - Session tracking
- `AnalyticsEvent` - Event logging

---

## 🚀 Caching (Optional)

### Memory Cache (Default)

Lightweight, no setup needed:
```env
CACHE_TYPE=memory
```

### Redis Cache

For distributed/production:

1. Install Redis: `pip install redis`
2. Install Redis server (Windows/Mac/Linux)
3. Update `.env`:
   ```env
   CACHE_TYPE=redis
   REDIS_URL=redis://localhost:6379/0
   ```

### Use Caching in Code

```python
from caching import cached

@cached(ttl=3600)  # Cache for 1 hour
async def expensive_operation():
    # Your code here
    return result
```

---

## 📝 Logging

### Log Levels

| Level | Usage |
|-------|-------|
| DEBUG | Detailed development info |
| INFO | Important events (default) |
| WARNING | Warning messages |
| ERROR | Error messages |

### Log Files

Located in `logs/` directory:
- Daily log files: `app_YYYYMMDD.log`
- Automatic cleanup after 30 days (configurable)

### Enable Detailed Logging

```env
LOG_LEVEL=DEBUG
LOG_REQUESTS=true
LOG_RESPONSES=false  # Set to true for verbose logging
```

---

## 🎯 Example: Custom API Key

To add API key authentication:

1. Enable in `.env`:
   ```env
   API_KEY_ENABLED=true
   API_KEY=your-secret-key-here
   ```

2. Use in requests:
   ```bash
   curl -H "X-API-Key: your-secret-key-here" \
        http://localhost:5501/api/predict
   ```

---

## 📊 Example: Monitoring Dashboard

Create a separate monitoring script:

```python
import requests
import time
from datetime import datetime

while True:
    response = requests.get('http://localhost:5501/health')
    health = response.json()
    
    print(f"\n{datetime.now()}")
    print(f"Status: {health['status']}")
    print(f"CPU: {health['system']['cpu_percent']}%")
    print(f"Memory: {health['system']['memory_percent']}%")
    print(f"Uptime: {health['uptime_formatted']}")
    
    time.sleep(5)
```

---

## 🔄 Production Deployment Checklist

- [ ] Set `ENV=production`
- [ ] Set `DEBUG=false`
- [ ] Set `LOG_LEVEL=WARNING`
- [ ] Configure `API_RATE_LIMIT` appropriately
- [ ] Enable Redis for `CACHE_TYPE`
- [ ] Setup PostgreSQL database
- [ ] Configure `API_KEY_ENABLED=true`
- [ ] Update CORS allowed origins
- [ ] Setup SSL/TLS (reverse proxy)
- [ ] Configure logging to external service
- [ ] Setup monitoring/alerting
- [ ] Test health endpoints
- [ ] Load test with rate limiting

---

## 🆘 Troubleshooting

### Port Already in Use

```bash
# Find process using port 5501
netstat -ano | findstr :5501

# Kill process (Windows)
taskkill /PID <PID> /F
```

### Rate Limit Errors

Increase limit in `.env`:
```env
API_RATE_LIMIT=500
```

### Memory Usage High

Enable Redis cache or reduce memory cache TTL:
```env
CACHE_TYPE=redis
CACHE_TTL=1800
```

### Slow Responses

Enable monitoring to identify bottlenecks:
```env
MONITOR_PERFORMANCE=true
LOG_REQUESTS=true
```

Then check `/metrics` endpoint.

---

## 📚 Additional Resources

- FastAPI: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/
- SQLAlchemy: https://www.sqlalchemy.org/
- Redis: https://redis.io/docs/

---

## 🤝 Support

For issues or questions:
1. Check `/metrics` for performance data
2. Review logs in `logs/` directory
3. Check health status at `/health`
4. Examine error responses for details

---

**Last Updated:** 2026-02-23
**Version:** 2.0.0 - Production Ready
