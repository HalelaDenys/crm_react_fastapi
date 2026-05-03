from core import settings
from infrastructure.fs_broker.broker import broker
from infrastructure.redis_client.client import RedisClient
from services.cache_service import CacheService
from services.service_api import ServiceAPI


class Container:
    def __init__(
        self,
    ) -> None:
        self.redis_c = RedisClient(url=settings.redis.dsh)
        self.api = ServiceAPI(base_url=settings.api.base_url)
        self.broker = broker

        self.redis = None
        self.cache = None

    async def start(self) -> None:
        await self.redis_c.connect()

        self.redis = self.redis_c.client
        self.cache = CacheService(self.redis)

        await self.api.connect()
        await self.broker.start()

    async def stop(self) -> None:
        await self.api.close()
        await self.broker.stop()
        await self.redis_c.disconnect()


container = Container()
