"""
Caching Module
Optional caching layer for performance
"""

from typing import Any, Optional, Callable
from datetime import datetime, timedelta
import json
from config import settings


class MemoryCache:
    """Simple in-memory cache"""
    
    def __init__(self):
        self.cache = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            item = self.cache[key]
            if datetime.now() < item['expires_at']:
                return item['value']
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        """Set value in cache"""
        ttl = ttl or settings.CACHE_TTL
        self.cache[key] = {
            'value': value,
            'expires_at': datetime.now() + timedelta(seconds=ttl)
        }
    
    def delete(self, key: str):
        """Delete value from cache"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear entire cache"""
        self.cache.clear()
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        return {
            'entries': len(self.cache),
            'memory_usage': sum(
                len(str(item['value'])) 
                for item in self.cache.values()
            )
        }


class RedisCache:
    """Redis-based cache (optional)"""
    
    def __init__(self):
        try:
            import redis
            self.redis_client = redis.from_url(settings.REDIS_URL)
            self.available = True
        except:
            self.available = False
            print("⚠️ Redis not available, falling back to memory cache")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        if not self.available:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
        except:
            return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        """Set value in Redis"""
        if not self.available:
            return
        
        ttl = ttl or settings.CACHE_TTL
        try:
            self.redis_client.setex(
                key,
                ttl,
                json.dumps(value, default=str)
            )
        except:
            pass
    
    def delete(self, key: str):
        """Delete value from Redis"""
        if self.available:
            try:
                self.redis_client.delete(key)
            except:
                pass
    
    def clear(self):
        """Clear Redis cache"""
        if self.available:
            try:
                self.redis_client.flushdb()
            except:
                pass


# Initialize cache
def initialize_cache():
    """Initialize appropriate cache backend"""
    if settings.CACHE_TYPE == 'redis' and settings.ENABLE_CACHING:
        cache = RedisCache()
        if cache.available:
            return cache
    
    return MemoryCache()


cache = initialize_cache()


def cached(ttl: int = None):
    """Decorator for caching function results"""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            if not settings.ENABLE_CACHING:
                return await func(*args, **kwargs)
            
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        
        def sync_wrapper(*args, **kwargs):
            if not settings.ENABLE_CACHING:
                return func(*args, **kwargs)
            
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cached_value = cache.get(cache_key)
            
            if cached_value is not None:
                return cached_value
            
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        
        return async_wrapper if hasattr(func, '__await__') else sync_wrapper
    
    return decorator
