import logging
import json
from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def get(self, key: str) -> dict | None:
        try:
            value = await self._redis.get(key)
        except Exception:
            logger.exception("Failed to get cached value")
            return None

        if not value:
            return None

        return json.loads(value)

    async def set(self, key: str, value: dict, ttl: int = 60) -> None:
        try:
            await self._redis.set(
                key,
                json.dumps(value),
                ex=ttl,
            )
        except Exception:
            logger.exception("Failed to set cached value")
