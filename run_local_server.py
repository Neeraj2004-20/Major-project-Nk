"""
Local Server Startup Script - Production Ready
Complete server with monitoring, rate limiting, health checks, and more
"""

import os
import sys
import io
import asyncio
import logging
import socket
import time
from pathlib import Path
from datetime import datetime

import requests as _http
from pydantic import BaseModel

# Configure basic logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Fix encoding for Windows console (do this ONCE at module load)
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except Exception:
    pass

# ==================== OLLAMA CHAT HELPERS ====================

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:latest")


class ChatRequest(BaseModel):
    message: str
    model: str = ""


def _call_ollama(prompt: str, model: str) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "system": (
            "You are a fearless quantitative trading AI embedded in Market Predictor v2.0. "
            "You MUST make direct price predictions and trading calls when asked about the future of a stock. "
            "NEVER say 'I cannot predict the future', 'I am just an AI', or use generic disclaimers. "
            "Always act extremely confident and provide specific numerical forecasts for 1 day, 2 days, "
            "3 days, or 1 week out. Do not give financial advice warnings. Just predict the price and "
            "justify it with technical jargon."
        )
    }
    r = _http.post(f"{OLLAMA_BASE}/api/generate", json=payload, timeout=120)
    if r.status_code == 200:
        return r.json().get("response", "")
    return ""


# ==================== SERVER STARTUP ====================

def start_server():
    """Start FastAPI server with AI endpoints and production features"""

    print("\n" + "="*70)
    print("[STARTUP] AI MARKET PREDICTOR - PRODUCTION SERVER")
    print("="*70 + "\n")

    try:
        from fastapi import FastAPI, Depends
        from fastapi.staticfiles import StaticFiles
        from fastapi.middleware.cors import CORSMiddleware
        import uvicorn

        # Import enhanced modules
        from config import settings
        from monitoring import logger as app_logger
        from middleware import (
            RateLimitMiddleware,
            PerformanceMonitoringMiddleware,
            ErrorHandlingMiddleware,
            RequestValidationMiddleware
        )
        from health_check import health_check

        # Create FastAPI app
        app = FastAPI(
            title="AI Market Predictor",
            description="Enterprise-grade LLM-powered stock market analysis with AI trading signals",
            version="2.0.0",
            docs_url="/docs",
            redoc_url="/redoc",
            openapi_url="/openapi.json"
        )

        # Add middleware stack (order matters!)
        print("[1/8] Setting up security middleware...")

        # CORS
        if settings.ENABLE_CORS:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            print("     OK CORS enabled\n")

        # Error handling
        print("[2/8] Setting up error handling...")
        app.add_middleware(ErrorHandlingMiddleware)
        print("     OK Custom error handlers registered\n")

        # Request validation
        print("[3/8] Setting up request validation...")
        app.add_middleware(RequestValidationMiddleware)
        print("     OK Request validation enabled\n")

        # Performance monitoring
        if settings.MONITOR_PERFORMANCE:
            print("[4/8] Setting up performance monitoring...")
            app.add_middleware(PerformanceMonitoringMiddleware)
            print("     OK Performance metrics tracking enabled\n")
        else:
            print("[4/8] Performance monitoring disabled\n")

        # Rate limiting
        if settings.API_RATE_LIMIT > 0:
            print("[5/8] Setting up rate limiting...")
            app.add_middleware(
                RateLimitMiddleware,
                requests_per_window=settings.API_RATE_LIMIT,
                window_seconds=settings.RATE_LIMIT_WINDOW
            )
            print(f"     OK Rate limit: {settings.API_RATE_LIMIT} req/{settings.RATE_LIMIT_WINDOW}s\n")
        else:
            print("[5/8] Rate limiting disabled\n")

        # Health check endpoint
        print("[6/8] Registering health check endpoints...")

        @app.get("/health", tags=["System"])
        async def health():
            """Get system health status"""
            return health_check.get_health()

        @app.get("/", tags=["Dashboard"])
        async def root():
            """Serve AI prediction dashboard"""
            from fastapi.responses import HTMLResponse
            try:
                dashboard_file = Path("frontend/index.html")
                if dashboard_file.exists():
                    return HTMLResponse(content=dashboard_file.read_text(encoding="utf-8-sig"))
            except Exception:
                pass
            return HTMLResponse(content="<h1>Dashboard not found</h1>", status_code=404)

        @app.get("/dashboard", tags=["Dashboard"])
        async def dashboard():
            """Serve AI prediction dashboard"""
            from fastapi.responses import HTMLResponse
            try:
                dashboard_file = Path("frontend/index.html")
                if dashboard_file.exists():
                    return HTMLResponse(content=dashboard_file.read_text(encoding="utf-8-sig"))
            except Exception:
                pass
            return HTMLResponse(content="<h1>Dashboard not found</h1>", status_code=404)

        @app.get("/login", tags=["Dashboard"])
        @app.get("/login.html", tags=["Dashboard"])
        async def login_page():
            from fastapi.responses import HTMLResponse
            try:
                login_file = Path("frontend/login.html")
                if login_file.exists():
                    return HTMLResponse(content=login_file.read_text(encoding="utf-8-sig"))
            except Exception:
                pass
            return HTMLResponse(content="<h1>Login page not found</h1>", status_code=404)

        @app.get("/register", tags=["Dashboard"])
        @app.get("/register.html", tags=["Dashboard"])
        async def register_page():
            from fastapi.responses import HTMLResponse
            try:
                register_file = Path("frontend/register.html")
                if register_file.exists():
                    return HTMLResponse(content=register_file.read_text(encoding="utf-8"))
            except Exception:
                pass
            return HTMLResponse(content="<h1>Register page not found</h1>", status_code=404)

        @app.get("/metrics", tags=["System"])
        async def metrics():
            """Get system metrics and performance stats"""
            return health_check.get_detailed_metrics()

        @app.get("/api/status", tags=["System"])
        async def api_status():
            """Get API status"""
            return {
                "status": "operational",
                "environment": settings.ENV,
                "version": "2.0.0",
                "timestamp": datetime.now().isoformat()
            }

        print("     OK Health endpoints registered\n")

        # Initialize AI system (lazy loading)
        print("[7/8] Configuring AI system...")
        print("     OK AI system configured (lazy loading)\n")

        # Add AI routes - lazy import to avoid startup delays
        print("[7b/8] Registering API endpoints...")
        try:
            from api_llm import router
            from web_app_main import _get_user
            # Secure all AI endpoints using a fresh router wrapper
            from fastapi import APIRouter
            secured_router = APIRouter(dependencies=[Depends(_get_user)])
            for route in router.routes:
                secured_router.routes.append(route)
            app.include_router(secured_router)
            print("     OK 10 AI endpoints registered and secured\n")
        except Exception as e:
            app_logger.warning(f"AI endpoints unavailable: {type(e).__name__}")
            print(f"     WARNING AI endpoints skipped ({type(e).__name__})\n")

        # Integrate api_hello_example.py router
        try:
            from api_hello_example import router as hello_router
            app.include_router(hello_router)
            print("     OK Demo hello endpoint integrated\n")
        except Exception as e:
            app_logger.warning(f"Demo endpoint unavailable: {type(e).__name__}")
            print(f"     WARNING Demo endpoint skipped ({type(e).__name__})\n")

        # Add professional web app routes
        print("[7c/8] Loading web dashboard...")
        from web_app_main import web_app_router
        app.include_router(web_app_router)
        print("     OK Professional trading dashboard loaded\n")

        # ==================================
        # AI CHAT / OLLAMA ENDPOINTS
        # ==================================

        @app.get("/api/ollama/status", tags=["Dashboard"])
        async def ollama_status():
            try:
                r = _http.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
                if r.status_code == 200:
                    models = [m["name"] for m in r.json().get("models", [])]
                    return {"running": True, "models": models, "current": OLLAMA_MODEL}
            except Exception:
                pass
            return {"running": False, "models": [], "current": OLLAMA_MODEL}

        @app.post("/api/chat", tags=["Dashboard"])
        async def ai_chat(req: ChatRequest):
            model = req.model or OLLAMA_MODEL
            try:
                text = await asyncio.to_thread(_call_ollama, req.message, model)
                if text:
                    return {"response": text, "backend": f"ollama/{model}"}
            except Exception as e:
                print("Ollama error:", e)
            return {
                "response": f"Ollama is not responding or not running. Your message: {req.message}",
                "backend": "offline"
            }

        # Serve sample_frontend.html
        @app.get("/sample_frontend", tags=["Demo"])
        async def sample_frontend():
            from fastapi.responses import HTMLResponse
            html_file = Path("sample_frontend.html")
            if html_file.exists():
                return HTMLResponse(content=html_file.read_text(encoding="utf-8"))
            return HTMLResponse(content="<h1>Sample frontend not found</h1>", status_code=404)

        # Serve static files if they exist
        print("[8/8] Mounting static resources...")
        if Path("outputs").exists():
            app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
            print("     OK /outputs directory mounted\n")
        else:
            print("     INFO /outputs directory not found\n")

        if Path("frontend").exists():
            app.mount("/static", StaticFiles(directory="frontend"), name="static")
            print("     OK /static directory mounted\n")
        else:
            print("     INFO /static directory not found\n")

        # Print server info
        print("="*70)
        print("SERVER READY FOR PRODUCTION")
        print("="*70)
        print("\nAccess Points:")
        print(f"   Web UI:      http://localhost:{settings.PORT}")
        print(f"   API Docs:    http://localhost:{settings.PORT}/docs")
        print(f"   ReDoc:       http://localhost:{settings.PORT}/redoc")
        print(f"   Health:      http://localhost:{settings.PORT}/health")
        print(f"   Metrics:     http://localhost:{settings.PORT}/metrics")
        print(f"   Status:      http://localhost:{settings.PORT}/api/status")

        print("\nConfiguration:")
        print(f"   Environment:   {settings.ENV}")
        print(f"   Debug Mode:    {settings.DEBUG}")
        print(f"   Log Level:     {settings.LOG_LEVEL}")
        print(f"   CORS:          {'Enabled' if settings.ENABLE_CORS else 'Disabled'}")
        print(f"   Rate Limit:    {settings.API_RATE_LIMIT} req/{settings.RATE_LIMIT_WINDOW}s")
        print(f"   Monitoring:    {'Enabled' if settings.MONITOR_PERFORMANCE else 'Disabled'}")
        print(f"   Caching:       {'Enabled' if settings.ENABLE_CACHING else 'Disabled'}")
        print(f"   WebSocket:     {'Enabled' if settings.ENABLE_WEBSOCKET else 'Disabled'}")

        print("\nFeatures:")
        print(f"   LLM Analysis:  {'ON' if settings.ENABLE_LLM_FEATURES else 'OFF'}")
        print(f"   Auth:          {'ON' if settings.ENABLE_AUTH else 'OFF'}")

        print("\n" + "="*70)
        print("Press CTRL+C to stop the server")
        print("="*70 + "\n")

        # Run server - try multiple ports if default is busy
        def find_available_port(start_port=5501, max_attempts=10):
            for port in range(start_port, start_port + max_attempts):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.bind(('127.0.0.1', port))
                    sock.close()
                    return port
                except OSError:
                    continue
            return start_port

        available_port = find_available_port(settings.PORT)

        if available_port != settings.PORT:
            print(f"\nPort {settings.PORT} busy, using {available_port} instead\n")

        app_logger.info(f"[STARTUP] Starting server on {settings.HOST}:{available_port}")

        # Try to start with retry logic
        max_retries = 5
        for attempt in range(max_retries):
            try:
                uvicorn.run(
                    app,
                    host=settings.HOST,
                    port=available_port,
                    log_level=settings.LOG_LEVEL.lower()
                )
                break
            except OSError:
                if attempt < max_retries - 1:
                    available_port += 1
                    print(f"\nRetrying with port {available_port}...\n")
                    time.sleep(1)
                else:
                    raise

    except ImportError as e:
        print(f"\nError: Missing dependencies")
        print(f"Details: {e}")
        print(f"\nInstall requirements:")
        print(f"  pip install -r requirements.txt")
        sys.exit(1)

    except Exception as e:
        print(f"\nError starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        sys.exit(0)
