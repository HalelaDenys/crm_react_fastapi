from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from handlers import main_router
from core import settings
from core.midd import RegisterUserMiddleware

from infrastructure import broker, container

import logging

logger = logging.getLogger(__name__)


async def main_bot():
    await container.start()

    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    storage = RedisStorage(container.redis)
    dp = Dispatcher(storage=storage)
    dp.include_router(main_router())
    dp.message.middleware(RegisterUserMiddleware())

    container.broker.context.set_global("bot", bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await container.stop()
        logger.info("Service connections closed")
