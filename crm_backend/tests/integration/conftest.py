from create_app import create_app
from tests.utils import (
    client_manager,
    ClientManagerType,
    async_session_maker,
    metadata,
    engine_test,
)
import pytest
from core import settings

app = create_app()


@pytest.fixture(scope="session", autouse=True)
async def engine():
    assert settings.mode == "TEST"
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield

    await engine_test.dispose()
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(
    scope="function",
)
async def db_session():
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def async_client() -> ClientManagerType:
    async with client_manager(app) as client:
        yield client
