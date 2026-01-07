from httpx import AsyncClient

from create_app import create_app
from tests.utils import (
    client_manager,
    ClientManagerType,
    async_session_maker,
    metadata,
    engine_test,
    insert_into_tables,
)
from core import settings
import pytest_asyncio
from schemas.employee_shemas import TokenInfo, LoginSchema


app = create_app()

pytest_plugins = [
    "tests.data_fixtures.users",
    "tests.data_fixtures.emps",
]


@pytest_asyncio.fixture(scope="module", autouse=True)
async def engine():
    assert settings.mode == "TEST"
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)

    await insert_into_tables()
    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)
    await engine_test.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def async_client() -> ClientManagerType:
    async with client_manager(app) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def login_admin(
    async_client: AsyncClient,
    admin_login_data: LoginSchema,
) -> TokenInfo:
    response = await async_client.post(
        "/auth/login", data=admin_login_data.model_dump()
    )

    assert response.status_code == 200

    return TokenInfo.model_validate(response.json())
