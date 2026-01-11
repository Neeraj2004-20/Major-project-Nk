# Deployment Guide - Advanced Market Predictor

This guide covers multiple deployment options for the Advanced Market Predictor API.

## 🚀 Quick Deployment Options

### Option 1: Local Deployment (Development)

**Prerequisites:**
- Python 3.8+
- Virtual environment activated

**Steps:**
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the server
python serve.py
```

Access at: `http://localhost:8000`  
API Docs: `http://localhost:8000/docs`

---

## 🐳 Option 2: Docker Deployment (Recommended)

### Build and Run Docker Container

```bash
# Build the Docker image
docker build -t market-predictor .

# Run the container
docker run -p 8000:8000 market-predictor

# Run with volume mounting (to persist outputs)
docker run -p 8000:8000 -v $(pwd)/outputs:/app/outputs market-predictor

# Run in detached mode
docker run -d -p 8000:8000 --name market-predictor-api market-predictor
```

### Docker Compose (Multiple Services)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access at: `http://localhost:8000`

---

## ☁️ Option 3: Cloud Deployment

### A. AWS Deployment

#### AWS EC2 (Virtual Machine)

1. **Launch EC2 Instance:**
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.medium (recommended) or t2.micro (free tier)
   - Security Group: Allow inbound on port 8000

2. **SSH into instance:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Setup environment:**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Docker
   sudo apt install docker.io -y
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker ubuntu
   
   # Clone your repository
   git clone <your-repo-url>
   cd <project-folder>
   
   # Build and run
   docker build -t market-predictor .
   docker run -d -p 8000:8000 --name market-predictor-api market-predictor
   ```

4. **Configure security group:**
   - Inbound rule: Custom TCP, Port 8000, Source 0.0.0.0/0

Access at: `http://your-ec2-ip:8000`

#### AWS ECS (Elastic Container Service)

See [aws-ecs-deployment.md](aws-ecs-deployment.md)

#### AWS Lambda + API Gateway (Serverless)

See [aws-lambda-deployment.md](aws-lambda-deployment.md)

---

### B. Google Cloud Platform (GCP)

#### GCP Cloud Run (Serverless Containers)

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy market-predictor \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

Access at the URL provided by Cloud Run.

#### GCP Compute Engine (VM)

```bash
# Create VM instance
gcloud compute instances create market-predictor-vm \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --machine-type=e2-medium \
  --zone=us-central1-a

# SSH into VM
gcloud compute ssh market-predictor-vm --zone=us-central1-a

# Follow similar steps as AWS EC2
```

---

### C. Microsoft Azure

#### Azure Container Instances

```bash
# Login to Azure
az login

# Create resource group
az group create --name market-predictor-rg --location eastus

# Create container registry
az acr create --resource-group market-predictor-rg \
  --name marketpredictorregistry --sku Basic

# Build and push image
az acr build --registry marketpredictorregistry \
  --image market-predictor:latest .

# Deploy to Container Instances
az container create \
  --resource-group market-predictor-rg \
  --name market-predictor-api \
  --image marketpredictorregistry.azurecr.io/market-predictor:latest \
  --cpu 2 --memory 4 \
  --registry-login-server marketpredictorregistry.azurecr.io \
  --ports 8000 \
  --dns-name-label market-predictor-unique
```

Access at: `http://market-predictor-unique.eastus.azurecontainer.io:8000`

---

## 🌐 Option 4: Platform-as-a-Service (PaaS)

### A. Heroku

1. **Install Heroku CLI:**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Procfile:**
   Already created in project root.

3. **Deploy:**
   ```bash
   # Login
   heroku login
   
   # Create app
   heroku create market-predictor-api
   
   # Deploy
   git push heroku main
   
   # Scale dynos
   heroku ps:scale web=1
   
   # Open app
   heroku open
   ```

### B. Railway.app

1. **Connect GitHub repository to Railway**
2. **Railway auto-detects Dockerfile**
3. **Deploy with one click**

Or via CLI:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### C. Render.com

1. **Create new Web Service on Render**
2. **Connect GitHub repository**
3. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn serve:app --host 0.0.0.0 --port $PORT`
4. **Deploy automatically**

### D. Fly.io

```bash
# Install flyctl
# https://fly.io/docs/hands-on/install-flyctl/

# Login
flyctl auth login

# Launch app
flyctl launch

# Deploy
flyctl deploy
```

---

## 🔒 Production Best Practices

### 1. Environment Variables

Create `.env` file:
```env
API_KEY=your-secret-api-key
ALLOWED_ORIGINS=https://yourdomain.com
MODEL_PATH=outputs/model_AAPL_latest.pt
LOG_LEVEL=INFO
```

Update `serve.py` to use environment variables.

### 2. HTTPS/SSL

For production, use:
- **Nginx** as reverse proxy with SSL
- **Let's Encrypt** for free SSL certificates
- **Cloudflare** for CDN and DDoS protection

### 3. Monitoring & Logging

```bash
# Add to requirements.txt
sentry-sdk[fastapi]
prometheus-client
python-json-logger
```

### 4. API Rate Limiting

```python
# Add to serve.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

### 5. Database for Logs

Use PostgreSQL, MongoDB, or Redis for storing:
- Prediction history
- API usage metrics
- Model performance

### 6. CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/deploy.yml`) already configured.

---

## 🧪 Testing Deployment

```bash
# Health check
curl http://your-deployment-url/health

# Get model info
curl http://your-deployment-url/model/info

# Make prediction
curl -X POST http://your-deployment-url/predict/live \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "days_ahead": 1}'

# View API docs
# Visit: http://your-deployment-url/docs
```

---

## 📊 Scaling Considerations

### Horizontal Scaling
- Use **Load Balancer** (AWS ALB, GCP Load Balancing)
- Deploy multiple instances
- Use **Kubernetes** for orchestration

### Vertical Scaling
- Increase CPU/RAM
- Use GPU instances for faster predictions (AWS p3, GCP with GPU)

### Database Caching
- Use **Redis** for caching predictions
- Store frequently accessed data

### Model Serving
- Use **TorchServe** or **TensorFlow Serving**
- Separate model inference from API logic

---

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Find and kill process
   lsof -ti:8000 | xargs kill -9  # Linux/Mac
   netstat -ano | findstr :8000   # Windows
   ```

2. **Memory issues:**
   - Reduce `MODEL_DIM` in config.json
   - Use CPU instead of GPU
   - Increase container memory

3. **Model not loading:**
   - Check model file exists
   - Verify file permissions
   - Ensure correct path in config

4. **CORS errors:**
   - Update CORS settings in serve.py
   - Allow your frontend domain

---

## 🔄 Updating Deployment

```bash
# Pull latest changes
git pull origin main

# Rebuild Docker image
docker build -t market-predictor .

# Stop old container
docker stop market-predictor-api

# Remove old container
docker rm market-predictor-api

# Run new container
docker run -d -p 8000:8000 --name market-predictor-api market-predictor
```

Or use Docker Compose:
```bash
docker-compose down
docker-compose up -d --build
```

---

## 📚 Additional Resources

- [FastAPI Deployment Docs](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [AWS ECS Tutorial](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/)
- [Kubernetes Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

---

## 💰 Cost Estimation

| Platform | Free Tier | Paid (Monthly) |
|----------|-----------|----------------|
| Heroku | 550 hrs/month | $7-25+ |
| Railway | 500 hrs + $5 credit | $5-20+ |
| Render | 750 hrs/month | $7-85+ |
| Fly.io | 3 VMs shared CPU | $5-30+ |
| AWS EC2 t2.micro | 750 hrs (1 year) | $10-50+ |
| GCP Cloud Run | 2M requests | $5-50+ |
| Azure Container | N/A | $15-60+ |

---

**Need help?** Open an issue or contact support.
