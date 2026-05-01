from unittest.mock import AsyncMock

from aiogram.exceptions import TelegramBadRequest

from core import BookingStateForm
from handlers.booking import create_booking, get_category
import pytest


# tests/test_booking.py
@pytest.mark.asyncio
async def test_create_booking(callback_query, fsm, mocker):
    # который используется в handlers.booking
    mocker.patch(
        "handlers.booking.api.get_category",
        new_callable=AsyncMock,
        return_value=[
            {"text": "Test category", "call": "category:1:1"},
        ],
    )

    # вызываем handler
    await create_booking(callback_query, fsm)

    # ✅ проверяем FSM
    fsm.set_state.assert_called_once_with(BookingStateForm.category_id)

    # ✅ проверяем, что бот отредактировал сообщение
    callback_query.message.edit_text.assert_called_once()

    # (опционально) проверка текста
    args, kwargs = callback_query.message.edit_text.call_args
    assert args[0] == "Виберіть категорію"
    assert "reply_markup" in kwargs


@pytest.mark.asyncio
async def test_get_category_telegram_badrequest(callback_query, fsm, mocker):
    callback_query.data = "category:5:1"

    mocker.patch(
        "handlers.booking.api.get_service_by_category",
        new_callable=AsyncMock,
        return_value=([], False),
    )

    # Симуляция TelegramBadRequest с "message is not modified"
    callback_query.message.edit_text.side_effect = TelegramBadRequest(
        method="editMessageText",  # метод Telegram, который вызвал ошибку
        message="message is not modified",
    )

    # Хендлер должен обработать и не падать
    await get_category(callback_query, fsm)
