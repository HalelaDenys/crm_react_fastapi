from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from handlers import main_router
from core import settings, api
from core.midd import RegisterUserMiddleware

from infrastructure import broker, redis_client

import logging

logger = logging.getLogger(__name__)


async def main_bot():
    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await redis_client.connect()
    await api.connect()

    storage = RedisStorage(redis_client.client)
    dp = Dispatcher(storage=storage)

    dp.include_router(main_router())
    dp.message.middleware(RegisterUserMiddleware())

    broker.context.set_global("bot", bot)

    await broker.start()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await api.close()
        await broker.stop()
        await redis_client.disconnect()
        logger.info("Service connections closed")
