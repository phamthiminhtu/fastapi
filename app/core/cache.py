"""Redis cache utilities for user authentication"""

import json
from typing import Optional
from redis import Redis
from redis.exceptions import RedisError
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Redis client (initialized lazily)
_redis_client: Optional[Redis] = None


def get_redis_client() -> Optional[Redis]:
    """
    Get Redis client instance

    Returns:
        Redis client or None if cache is disabled or connection fails
    """
    global _redis_client

    if not settings.cache_enabled:
        return None

    if _redis_client is None:
        try:
            _redis_client = Redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2
            )
            # Test connection
            _redis_client.ping()
            logger.info("Redis cache connected successfully")
        except RedisError as e:
            logger.warning(f"Redis connection failed: {e}. Cache disabled.")
            _redis_client = None

    return _redis_client


def cache_user(username: str, user_data: dict) -> bool:
    """
    Cache user data in Redis

    Args:
        username: Username to use as cache key
        user_data: User data dictionary to cache

    Returns:
        True if cached successfully, False otherwise
    """
    client = get_redis_client()
    if not client:
        return False

    try:
        cache_key = f"user:{username}"
        user_json = json.dumps(user_data)
        client.setex(cache_key, settings.cache_ttl_seconds, user_json)
        logger.debug(f"Cached user: {username}")
        return True
    except (RedisError, json.JSONDecodeError) as e:
        logger.warning(f"Failed to cache user {username}: {e}")
        return False


def get_cached_user(username: str) -> Optional[dict]:
    """
    Get cached user data from Redis

    Args:
        username: Username to look up

    Returns:
        User data dictionary or None if not found/cache miss
    """
    client = get_redis_client()
    if not client:
        return None

    try:
        cache_key = f"user:{username}"
        cached_data = client.get(cache_key)

        if cached_data:
            logger.debug(f"Cache hit for user: {username}")
            return json.loads(cached_data)

        logger.debug(f"Cache miss for user: {username}")
        return None
    except (RedisError, json.JSONDecodeError) as e:
        logger.warning(f"Failed to get cached user {username}: {e}")
        return None


def invalidate_user_cache(username: str) -> bool:
    """
    Invalidate (delete) cached user data

    Args:
        username: Username to invalidate

    Returns:
        True if invalidated successfully, False otherwise
    """
    client = get_redis_client()
    if not client:
        return False

    try:
        cache_key = f"user:{username}"
        deleted = client.delete(cache_key)
        if deleted:
            logger.debug(f"Invalidated cache for user: {username}")
        return bool(deleted)
    except RedisError as e:
        logger.warning(f"Failed to invalidate cache for {username}: {e}")
        return False


def clear_all_user_cache() -> bool:
    """
    Clear all user cache entries

    Returns:
        True if cleared successfully, False otherwise
    """
    client = get_redis_client()
    if not client:
        return False

    try:
        # Find all user cache keys
        keys = client.keys("user:*")
        if keys:
            client.delete(*keys)
            logger.info(f"Cleared {len(keys)} user cache entries")
        return True
    except RedisError as e:
        logger.warning(f"Failed to clear user cache: {e}")
        return False


def get_cache_stats() -> dict:
    """
    Get cache statistics

    Returns:
        Dictionary with cache stats
    """
    client = get_redis_client()
    if not client:
        return {"enabled": False, "status": "disabled"}

    try:
        info = client.info()
        user_keys = len(client.keys("user:*"))

        return {
            "enabled": True,
            "status": "connected",
            "total_keys": info.get("db0", {}).get("keys", 0),
            "user_cache_keys": user_keys,
            "memory_used": info.get("used_memory_human", "unknown"),
            "connected_clients": info.get("connected_clients", 0)
        }
    except RedisError as e:
        return {"enabled": True, "status": f"error: {e}"}
