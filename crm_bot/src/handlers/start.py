from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from core import inline_keyboard_builder

router = Router()


async def send_main_menu(target: CallbackQuery | Message):
    await target.answer(
        "Menu",
        reply_markup=inline_keyboard_builder(
            [
                {"text": "Бронювання", "call": "create_booking"},
                {"text": "Час роботи ", "call": "work_time"},
            ]
        ),
    )


@router.message(CommandStart())
async def start_from_message(message: Message):
    await send_main_menu(message)


@router.callback_query(F.data == "start")
async def start_from_callback(callback: CallbackQuery):
    await callback.message.delete()
    await send_main_menu(callback.message)
