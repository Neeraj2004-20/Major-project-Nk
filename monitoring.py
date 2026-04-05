"""
Logging & Monitoring Module
Structured logging with performance tracking
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from collections import defaultdict
from config import settings


# Create logs directory
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)


class PerformanceMonitor:
    """Track request/response performance metrics"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.status_codes = defaultdict(int)
        self.errors = []
        
    def record_request(self, endpoint: str, method: str, duration: float, 
                      status_code: int, error: Optional[str] = None):
        """Record request metrics"""
        self.metrics[endpoint].append({
            'method': method,
            'duration': duration,
            'timestamp': datetime.now().isoformat(),
            'status': status_code
        })
        self.status_codes[status_code] += 1
        
        if error:
            self.errors.append({
                'endpoint': endpoint,
                'error': error,
                'timestamp': datetime.now().isoformat()
            })
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        if not self.metrics:
            return {"message": "No metrics recorded yet"}
        
        stats = {
            'total_requests': sum(len(v) for v in self.metrics.values()),
            'endpoints': {},
            'status_codes': dict(self.status_codes),
            'errors_count': len(self.errors)
        }
        
        for endpoint, records in self.metrics.items():
            durations = [r['duration'] for r in records]
            stats['endpoints'][endpoint] = {
                'count': len(records),
                'avg_duration': sum(durations) / len(durations),
                'min_duration': min(durations),
                'max_duration': max(durations)
            }
        
        return stats
    
    def clear(self):
        """Clear metrics"""
        self.metrics.clear()
        self.status_codes.clear()
        self.errors.clear()


# Configure logging
def setup_logging():
    """Setup structured logging"""
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # File handler
    fh = logging.FileHandler(logs_dir / f'app_{datetime.now().strftime("%Y%m%d")}.log')
    fh.setLevel(getattr(logging, settings.LOG_LEVEL))
    fh.setFormatter(logging.Formatter(log_format))
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, settings.LOG_LEVEL))
    ch.setFormatter(logging.Formatter(log_format))
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    root_logger.addHandler(fh)
    root_logger.addHandler(ch)
    
    return root_logger


# Initialize
logger = setup_logging()
performance_monitor = PerformanceMonitor()


def log_request(endpoint: str, method: str, params: Dict = None):
    """Log incoming request"""
    if settings.LOG_REQUESTS:
        logger.info(f"[REQUEST] {method} {endpoint} - Params: {params or 'None'}")


def log_response(endpoint: str, status_code: int, duration: float):
    """Log outgoing response"""
    if settings.LOG_REQUESTS:
        logger.info(f"[RESPONSE] {endpoint} - Status: {status_code} - Duration: {duration:.3f}s")


def log_error(error: Exception, endpoint: str = "Unknown"):
    """Log error"""
    logger.error(f"[ERROR] Error at {endpoint}: {str(error)}", exc_info=True)
