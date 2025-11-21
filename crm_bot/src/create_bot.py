from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import main_router
from core import settings
from core.midd import RegisterUserMiddleware

from infrastructure.fs_broker.broker import broker

import logging

logger = logging.getLogger(__name__)

storage = MemoryStorage()


async def main_bot():
    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=storage)
    dp.include_router(main_router())
    dp.message.middleware(RegisterUserMiddleware())

    broker.context.set_global("bot", bot)

    await broker.start()
    logging.info("🐇 Broker started")
    try:
        await dp.start_polling(bot)
    finally:
        await broker.stop()
        logging.info("🛑 Broker stopped")
