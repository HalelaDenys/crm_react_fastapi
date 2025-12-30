from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport
from contextlib import asynccontextmanager
from asgi_lifespan import LifespanManager
from typing import AsyncGenerator
from sqlalchemy import NullPool
from infrastructure import Base, Employee, Position, User
from core import settings, Security


ClientManagerType = AsyncGenerator[AsyncClient, None]
AsyncSessionGenerator = AsyncGenerator[AsyncSession, None]

metadata = Base.metadata
DATABASE_URL = settings.db.database_url

engine_test = create_async_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)
async_session_maker = async_sessionmaker(
    bind=engine_test,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@asynccontextmanager
async def client_manager(
    app, base_url: str = "http://test" + settings.api_prefix.api_v1, **kwargs
) -> ClientManagerType:
    app.state.testing = True
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url=base_url, **kwargs
        ) as client:
            yield client


async def insert_into_tables() -> None:
    async with async_session_maker() as session:
        test_data(session)
        await session.commit()


def test_data(session: AsyncSession) -> None:
    admin_position = Position(
        name="admin",
    )

    session.add(admin_position)

    admin_emp = Employee(
        first_name="admin",
        last_name="superuser",
        email="admin@example.com",
        phone_number="+1 555 555 555",
        is_admin=True,
        position=admin_position,
        password=Security.hash_password("admin_password"),
    )

    session.add(admin_emp)

    liza_user = User(
        first_name="liza",
        last_name="simson",
        phone_number="+1 004 552 842",
    )

    session.add(liza_user)
