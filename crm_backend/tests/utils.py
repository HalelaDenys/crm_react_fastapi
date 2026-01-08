from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport
from contextlib import asynccontextmanager
from asgi_lifespan import LifespanManager
from typing import AsyncGenerator
from sqlalchemy import NullPool
from infrastructure import Base, Employee, Position, User, Category
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

    from tests.data_fixtures.users import liza_user
    from tests.data_fixtures.emps import ron_emp
    from tests.data_fixtures.category import quick_works, diagnostics

    admin_position = Position(
        name="admin",
    )

    manager_position = Position(
        name="manager",
    )
    session.add_all([admin_position, manager_position])

    admin_emp = Employee(
        first_name="admin",
        last_name="superuser",
        email="admin@example.com",
        phone_number="+1 555 555 555",
        is_admin=True,
        position=admin_position,
        password=Security.hash_password("admin_password"),
    )

    ron_emp = Employee(
        first_name=ron_emp["first_name"],
        last_name=ron_emp["last_name"],
        email=ron_emp["email"],
        phone_number=ron_emp["phone_number"],
        is_admin=False,
        position=manager_position,
        password=Security.hash_password(ron_emp["password"]),
    )

    session.add_all([admin_emp, ron_emp])

    test_liza_user = User(
        first_name=liza_user["first_name"],
        last_name=liza_user["last_name"],
        phone_number=liza_user["phone_number"],
    )

    session.add(test_liza_user)

    data_quick_works = Category(name=quick_works["name"])
    data_diagnostics = Category(name=diagnostics["name"])

    session.add_all([data_quick_works, data_diagnostics])
