from unittest.mock import AsyncMock

import pytest_asyncio
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, Chat, Contact, User


# tests/conftest.py
@pytest_asyncio.fixture
def fsm():
    state = AsyncMock(spec=FSMContext)
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()
    state.get_data = AsyncMock(return_value={})
    state.clear = AsyncMock()
    return state


@pytest_asyncio.fixture
def callback_query():
    call = AsyncMock(spec=CallbackQuery)

    call.data = "create_booking"

    call.from_user = User(
        id=123,
        is_bot=False,
        first_name="Test",
        language_code="uk",
    )

    call.message = AsyncMock(spec=Message)
    call.message.chat = Chat(id=123, type="private")
    call.message.edit_text = AsyncMock()
    call.message.answer = AsyncMock()

    call.answer = AsyncMock()

    return call


@pytest_asyncio.fixture
def message_with_contact():
    msg = AsyncMock(spec=Message)

    msg.from_user = User(
        id=123,
        is_bot=False,
        first_name="Test",
    )

    msg.chat = Chat(id=123, type="private")

    msg.contact = Contact(
        phone_number="+380991234567",
        first_name="Test",
        user_id=123,
    )

    msg.answer = AsyncMock()
    msg.delete = AsyncMock()

    return msg
