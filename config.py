"""
Configuration Management
Loads settings from .env file with fallbacks to defaults
"""

import os
import json
from typing import Optional, List
from pathlib import Path

# Force load .env file
try:
    from dotenv import load_dotenv, find_dotenv
    # Find and load .env file
    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        load_dotenv(dotenv_path, override=True)
    else:
        # Try explicit path
        env_file = Path(__file__).parent / '.env'
        if env_file.exists():
            load_dotenv(env_file, override=True)
except ImportError:
    pass


class Settings:
    """Application Settings"""
    
    # Server
    DEBUG: bool = os.getenv('DEBUG', 'true').lower() == 'true'
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8000'))
    ENV: str = os.getenv('ENV', 'development')
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_REQUESTS: bool = os.getenv('LOG_REQUESTS', 'true').lower() == 'true'
    LOG_RESPONSES: bool = os.getenv('LOG_RESPONSES', 'false').lower() == 'true'
    
    # Security
    API_KEY_ENABLED: bool = os.getenv('API_KEY_ENABLED', 'false').lower() == 'true'
    API_KEY: str = os.getenv('API_KEY', 'change-me-in-production')
    API_RATE_LIMIT: int = int(os.getenv('API_RATE_LIMIT', '100'))
    RATE_LIMIT_WINDOW: int = int(os.getenv('RATE_LIMIT_WINDOW', '60'))
    
    # Database
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./market_predictor.db')
    DATABASE_ECHO: bool = os.getenv('DATABASE_ECHO', 'false').lower() == 'true'
    
    # Cache
    CACHE_TYPE: str = os.getenv('CACHE_TYPE', 'memory')
    REDIS_URL: str = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TTL: int = int(os.getenv('CACHE_TTL', '3600'))
    
    # LLM
    ENABLE_LLM_FEATURES: bool = os.getenv('ENABLE_LLM_FEATURES', 'true').lower() == 'true'
    LLM_MODEL_NAME: str = os.getenv('LLM_MODEL_NAME', 'auto')
    LLM_MAX_TOKENS: int = int(os.getenv('LLM_MAX_TOKENS', '2048'))
    LLM_TEMPERATURE: float = float(os.getenv('LLM_TEMPERATURE', '0.7'))
    
    # Features
    ENABLE_WEBSOCKET: bool = os.getenv('ENABLE_WEBSOCKET', 'true').lower() == 'true'
    ENABLE_CACHING: bool = os.getenv('ENABLE_CACHING', 'true').lower() == 'true'
    ENABLE_AUTH: bool = os.getenv('ENABLE_AUTH', 'false').lower() == 'true'
    ENABLE_MONITORING: bool = os.getenv('ENABLE_MONITORING', 'true').lower() == 'true'
    ENABLE_CORS: bool = os.getenv('ENABLE_CORS', 'true').lower() == 'true'
    
    # Monitoring
    MONITOR_PERFORMANCE: bool = os.getenv('MONITOR_PERFORMANCE', 'true').lower() == 'true'
    RETENTION_DAYS: int = int(os.getenv('RETENTION_DAYS', '30'))
    
    # CORS Origins
    CORS_ORIGINS: List[str] = json.loads(os.getenv('CORS_ORIGINS', '["http://localhost:3000", "http://localhost:5501", "http://localhost:8000"]'))
    
    # API Documentation
    ENABLE_DOCS: bool = os.getenv('ENABLE_DOCS', 'true').lower() == 'true'
    ENABLE_REDOC: bool = os.getenv('ENABLE_REDOC', 'true').lower() == 'true'
    DOCS_URL: str = os.getenv('DOCS_URL', '/docs')
    REDOC_URL: str = os.getenv('REDOC_URL', '/redoc')
    OPENAPI_URL: str = os.getenv('OPENAPI_URL', '/openapi.json')
    
    # Security - Session & Token
    SESSION_TIMEOUT: int = int(os.getenv('SESSION_TIMEOUT', '1800'))  # 30 minutes
    TOKEN_EXPIRY: int = int(os.getenv('TOKEN_EXPIRY', '86400'))  # 24 hours
    JWT_SECRET: str = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    
    # File Upload & Request Limits
    MAX_FILE_SIZE: int = int(os.getenv('MAX_FILE_SIZE', '10485760'))  # 10MB
    MAX_REQUEST_SIZE: int = int(os.getenv('MAX_REQUEST_SIZE', '5242880'))  # 5MB
    MAX_PREDICTIONS_BATCH: int = int(os.getenv('MAX_PREDICTIONS_BATCH', '100'))
    
    # Storage Paths
    OUTPUT_DIR: str = os.getenv('OUTPUT_DIR', './outputs')
    LOGS_DIR: str = os.getenv('LOGS_DIR', './logs')
    DATA_DIR: str = os.getenv('DATA_DIR', './data')
    MODELS_DIR: str = os.getenv('MODELS_DIR', './models')
    
    # Prediction Thresholds
    CONFIDENCE_THRESHOLD: float = float(os.getenv('CONFIDENCE_THRESHOLD', '0.6'))
    BUY_SIGNAL_THRESHOLD: float = float(os.getenv('BUY_SIGNAL_THRESHOLD', '0.7'))
    SELL_SIGNAL_THRESHOLD: float = float(os.getenv('SELL_SIGNAL_THRESHOLD', '0.3'))
    HOLD_RANGE: tuple = (0.3, 0.7)  # Hold between 30% and 70%
    
    # External APIs
    STOCK_API_KEY: str = os.getenv('STOCK_API_KEY', '')
    STOCK_API_URL: str = os.getenv('STOCK_API_URL', 'https://api.example.com')
    SENTIMENT_API_KEY: str = os.getenv('SENTIMENT_API_KEY', '')
    SENTIMENT_API_URL: str = os.getenv('SENTIMENT_API_URL', '')
    NEWS_API_KEY: str = os.getenv('NEWS_API_KEY', '')
    
    # Version & Metadata
    API_VERSION: str = "2.0.0"
    APP_NAME: str = "AI Market Predictor"
    APP_DESCRIPTION: str = "Advanced AI-powered market analysis and prediction system"
    TIMEZONE: str = os.getenv('TIMEZONE', 'UTC')
    API_PREFIX: str = os.getenv('API_PREFIX', '/api')
    
    # Advanced Features
    ENABLE_BACKTEST: bool = os.getenv('ENABLE_BACKTEST', 'true').lower() == 'true'
    ENABLE_ALERTS: bool = os.getenv('ENABLE_ALERTS', 'true').lower() == 'true'
    ENABLE_EXPORT: bool = os.getenv('ENABLE_EXPORT', 'true').lower() == 'true'
    ENABLE_HISTORY: bool = os.getenv('ENABLE_HISTORY', 'true').lower() == 'true'
    
    # Performance Tuning
    WORKER_THREADS: int = int(os.getenv('WORKER_THREADS', '4'))
    CACHE_WARMUP: bool = os.getenv('CACHE_WARMUP', 'true').lower() == 'true'
    BATCH_PROCESSING: bool = os.getenv('BATCH_PROCESSING', 'true').lower() == 'true'
    
    # Email & Notifications
    SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT: int = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME: str = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD', '')
    EMAIL_FROM: str = os.getenv('EMAIL_FROM', 'noreply@marketpredictor.com')
    ENABLE_EMAIL_ALERTS: bool = os.getenv('ENABLE_EMAIL_ALERTS', 'false').lower() == 'true'


settings = Settings()
