from typing import Any, Optional
from datetime import datetime, timedelta
import threading
from functools import lru_cache


class CacheManager:
    def __init__(self, ttl_seconds: int = 300):  # 5 minutes default TTL
        self._cache = {}
        self._ttl = ttl_seconds
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if datetime.utcnow() - timestamp < timedelta(seconds=self._ttl):
                    return value
                else:
                    del self._cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache with timestamp"""
        with self._lock:
            self._cache[key] = (value, datetime.utcnow())

    def invalidate(self, key: str) -> None:
        """Remove key from cache"""
        with self._lock:
            self._cache.pop(key, None)


# Create global cache instances for different components
problem_cache = CacheManager(ttl_seconds=600)  # 10 minutes for problems
progress_cache = CacheManager(ttl_seconds=60)   # 1 minute for progress
stats_cache = CacheManager(ttl_seconds=300)     # 5 minutes for statistics


@lru_cache(maxsize=128)
def get_problem_template(topic: str, difficulty: int) -> dict:
    """Cache frequently used problem templates"""
    from .repository import ProblemRepository
    repo = ProblemRepository()
    return repo.create_problem(topic, difficulty).to_dict()
