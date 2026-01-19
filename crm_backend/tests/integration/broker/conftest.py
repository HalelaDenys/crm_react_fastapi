from unittest.mock import AsyncMock

from infrastructure.fs_broker import broker
from faststream.rabbit import TestRabbitBroker
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure import TgUserRepository, BookingRepository
from core import settings


# tests/integration/broker/conftest.
@pytest_asyncio.fixture(scope="function")
async def test_broker(mock_booking_service, mock_tg_user_service):
    async with TestRabbitBroker(broker, with_real=settings.fs.with_real) as br:
        yield br


@pytest_asyncio.fixture
async def tg_secret_key() -> dict:
    return {"authorization": f"Bearer {settings.fs.tg_api_secret}"}
