from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import main_router
from core import settings

storage = MemoryStorage()

async def create_bot() -> None:
    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=storage)

    dp.include_router(main_router())

    await dp.start_polling(bot)
