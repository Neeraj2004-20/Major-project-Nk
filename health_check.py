"""
Health Check & System Status
Monitor system health and availability
"""

from datetime import datetime
from typing import Dict, Any
import sys

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class HealthCheck:
    """System health monitoring"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.last_check = datetime.now()
    
    def get_health(self) -> Dict[str, Any]:
        """Get system health status"""
        
        now = datetime.now()
        uptime = (now - self.start_time).total_seconds()
        
        # CPU and Memory
        if PSUTIL_AVAILABLE:
            try:
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                memory_available_mb = memory.available / (1024 * 1024)
            except Exception:
                cpu_percent = 0
                memory_percent = 0
                memory_available_mb = 0
            
            # Disk
            try:
                disk = psutil.disk_usage('/')
                disk_percent = disk.percent
            except Exception:
                disk_percent = 0
        else:
            cpu_percent = 0
            memory_percent = 0
            memory_available_mb = 0
            disk_percent = 0
        
        # Status determination
        status = "healthy"
        if cpu_percent > 80 or memory_percent > 90 or disk_percent > 95:
            status = "degraded"
        if cpu_percent > 95 or memory_percent > 98 or disk_percent > 99:
            status = "critical"
        
        from config import settings
        from monitoring import performance_monitor
        
        health = {
            "status": status,
            "timestamp": now.isoformat(),
            "uptime_seconds": uptime,
            "uptime_formatted": self._format_uptime(uptime),
            "system": {
                "cpu_percent": round(cpu_percent, 2),
                "memory_percent": round(memory_percent, 2),
                "memory_available_mb": round(memory_available_mb, 2),
                "disk_percent": round(disk_percent, 2),
                "python_version": sys.version.split()[0]
            },
            "server": {
                "host": settings.HOST,
                "port": settings.PORT,
                "environment": settings.ENV,
                "debug": settings.DEBUG,
                "log_level": settings.LOG_LEVEL
            },
            "api": {
                "requests_total": len(performance_monitor.metrics),
                "rate_limit": f"{settings.API_RATE_LIMIT} per {settings.RATE_LIMIT_WINDOW}s",
                "cors_enabled": settings.ENABLE_CORS
            },
            "features": {
                "websocket": settings.ENABLE_WEBSOCKET,
                "caching": settings.ENABLE_CACHING,
                "auth": settings.ENABLE_AUTH,
                "monitoring": settings.ENABLE_MONITORING,
                "llm": settings.ENABLE_LLM_FEATURES
            }
        }
        
        return health
    
    @staticmethod
    def _format_uptime(seconds: float) -> str:
        """Format uptime in human readable form"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        parts.append(f"{secs}s")
        
        return " ".join(parts)
    
    def get_detailed_metrics(self) -> Dict[str, Any]:
        """Get detailed performance metrics"""
        from monitoring import performance_monitor
        return {
            "performance": performance_monitor.get_stats(),
            "health": self.get_health()
        }


# Global health check instance
health_check = HealthCheck()
