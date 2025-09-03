from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


phone_number_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📱 Поділитися номер телефлну", request_contact=True),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True,
)
