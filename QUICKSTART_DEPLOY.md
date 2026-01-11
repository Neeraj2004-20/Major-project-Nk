# Quick Deployment Commands

## 🚀 Choose Your Deployment Method:

### 1️⃣ Docker (Easiest)
```bash
docker build -t market-predictor .
docker run -p 8000:8000 market-predictor
```
**Access:** http://localhost:8000

---

### 2️⃣ Docker Compose (Recommended for Production)
```bash
docker-compose up -d
```
**Includes:** API + Nginx + Redis + PostgreSQL

---

### 3️⃣ Heroku (One-Click Deploy)
```bash
heroku login
heroku create market-predictor-api
git push heroku main
heroku open
```

---

### 4️⃣ Railway.app
1. Go to https://railway.app
2. Connect GitHub repo
3. Click "Deploy"
**Done!** Auto-deploys from GitHub

---

### 5️⃣ Render.com
1. Go to https://render.com
2. New Web Service
3. Connect repo
4. Start Command: `uvicorn serve:app --host 0.0.0.0 --port $PORT`
**Done!**

---

### 6️⃣ AWS EC2
```bash
# SSH to EC2
ssh -i key.pem ubuntu@YOUR-EC2-IP

# Install Docker
sudo apt update
sudo apt install docker.io -y

# Clone and run
git clone YOUR-REPO
cd YOUR-REPO
sudo docker build -t market-predictor .
sudo docker run -d -p 8000:8000 market-predictor
```
**Access:** http://YOUR-EC2-IP:8000

---

### 7️⃣ Google Cloud Run (Serverless)
```bash
gcloud run deploy market-predictor \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

### 8️⃣ Local Development
```bash
python serve.py
```
**Access:** http://localhost:8000

---

## 🧪 Test Your Deployment

```bash
# Health check
curl http://YOUR-URL/health

# API docs
# Visit: http://YOUR-URL/docs

# Test prediction
curl -X POST http://YOUR-URL/predict/live \
  -H "Content-Type: application/json" \
  -d '{"symbol":"AAPL","days_ahead":1}'
```

---

## 📊 Recommended Setup by Use Case

| Use Case | Recommended Platform | Cost |
|----------|---------------------|------|
| Development | Local/Docker | Free |
| Small project | Railway/Render | $5-7/mo |
| Production API | AWS/GCP | $15-50/mo |
| Enterprise | Kubernetes | $100+/mo |

---

## ⚠️ Before Deploying

- [ ] Update `config.json` with your settings
- [ ] Set environment variables (copy `.env.example` to `.env`)
- [ ] Train model: `python main.py`
- [ ] Test locally: `python serve.py`
- [ ] Check API docs: http://localhost:8000/docs

---

**Full documentation:** See [DEPLOYMENT.md](DEPLOYMENT.md)
