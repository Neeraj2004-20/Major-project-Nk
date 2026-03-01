# ⚡ Quick Reference Guide

## 🚀 Start Server

```bash
python run_local_server.py
```

## 📊 Access Points

| Purpose | URL |
|---------|-----|
| Web UI | http://localhost:5501 |
| API Docs | http://localhost:5501/docs |
| Health | http://localhost:5501/health |
| Metrics | http://localhost:5501/metrics |

## 🧪 Test Server

```bash
python test_server.py
```

## ⚙️ Configuration

Edit `.env` file to customize:

```env
# Server Settings
PORT=5501
ENV=development
DEBUG=true

# Security
API_RATE_LIMIT=100
RATE_LIMIT_WINDOW=60

# Features
ENABLE_CACHING=true
ENABLE_MONITORING=true
```

## 📝 Logs

View logs in `logs/` directory:
```bash
# Linux/Mac
tail -f logs/app_*.log

# Windows
Get-Content logs/app_*.log -Tail 10
```

## 🔍 Check Health

```bash
curl http://localhost:5501/health
```

Response:
```json
{
  "status": "healthy",
  "uptime_formatted": "2m 15s",
  "system": {
    "cpu_percent": 45.2,
    "memory_percent": 62.5
  }
}
```

## 📈 View Metrics

```bash
curl http://localhost:5501/metrics
```

## 🛑 Stop Server

Press `CTRL+C` in terminal

## 🐛 Debug Issues

1. **Check logs:**
   ```bash
   ls logs/
   ```

2. **Test endpoints:**
   ```bash
   curl http://localhost:5501/health
   ```

3. **View configuration:**
   Check `.env` file

4. **Port in use:**
   ```bash
   # Windows
   netstat -ano | findstr :5501
   
   # Linux/Mac
   lsof -i :5501
   ```

## 📦 Install Optional Features

```bash
# Full production setup
pip install sqlalchemy redis psutil

# Or install from requirements
pip install -r requirements-optional.txt
```

## 🔐 Enable API Key Auth

1. Update `.env`:
   ```env
   API_KEY_ENABLED=true
   API_KEY=your-secret-key
   ```

2. Use in requests:
   ```bash
   curl -H "X-API-Key: your-secret-key" \
        http://localhost:5501/api/predict
   ```

## 💾 Database Operations

Check `database.py` for models, or use:
```bash
python -c "from database import init_db; init_db()"
```

## 🔄 Environment Variables

| Name | Default | Type |
|------|---------|------|
| PORT | 5501 | int |
| HOST | 0.0.0.0 | str |
| ENV | development | str |
| DEBUG | true | bool |
| LOG_LEVEL | INFO | str |
| API_RATE_LIMIT | 100 | int |
| ENABLE_CACHING | true | bool |
| CACHE_TYPE | memory | str |
| ENABLE_MONITORING | true | bool |

## 📚 More Info

See `PRODUCTION_SETUP.md` for detailed documentation.

---

**Version:** 2.0.0 | **Status:** Production Ready ✅
