from infrastructure.fs_broker import broker
from faststream.rabbit import TestRabbitBroker
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure import TgUserRepository
from core import settings


@pytest_asyncio.fixture
async def test_broker():
    async with TestRabbitBroker(broker, with_real=True) as br:
        yield br


@pytest_asyncio.fixture
async def tg_user_repo(db_session: AsyncSession):
    return TgUserRepository(session=db_session)


@pytest_asyncio.fixture
async def tg_secret_key() -> dict:
    return {"authorization": f"Bearer {settings.fs.tg_api_secret}"}
