from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from infrastructure import (
    Base,
    Employee,
    Position,
    User,
    Category,
    Service,
    Booking,
    TgUser,
)
from httpx import AsyncClient, ASGITransport
from contextlib import asynccontextmanager
from asgi_lifespan import LifespanManager
from typing import AsyncGenerator
from sqlalchemy import NullPool
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
        await test_data(session)
        await session.commit()


async def test_data(session: AsyncSession) -> None:
    from datetime import date, time
    from tests.data_fixtures.users import liza_user
    from tests.data_fixtures.emps import ron_emp
    from tests.data_fixtures.category import quick_works, diagnostics
    from tests.data_fixtures.service import oil_filter_replacement, brake_diagnostics

    # ---- Positions
    admin_position = Position(name="admin")
    manager_position = Position(name="manager")
    session.add_all([admin_position, manager_position])
    await session.flush()

    # ---- Employees
    admin_emp = Employee(
        first_name="admin",
        last_name="superuser",
        email="admin@example.com",
        phone_number="+1 555 555 555",
        is_admin=True,
        position=admin_position,
        password=Security.hash_password("admin_password"),
    )

    ron_emp_data = ron_emp  # з fixture
    ron_emp_obj = Employee(
        first_name=ron_emp_data["first_name"],
        last_name=ron_emp_data["last_name"],
        email=ron_emp_data["email"],
        phone_number=ron_emp_data["phone_number"],
        is_admin=False,
        position=manager_position,
        password=Security.hash_password(ron_emp_data["password"]),
    )

    session.add_all([admin_emp, ron_emp_obj])
    await session.flush()

    # ---- User
    test_liza_user = User(
        first_name=liza_user["first_name"],
        last_name=liza_user["last_name"],
        phone_number=liza_user["phone_number"],
    )
    session.add(test_liza_user)
    await session.flush()

    # ---- Categories
    data_quick_works = Category(name=quick_works["name"])
    data_diagnostics = Category(name=diagnostics["name"])
    session.add_all([data_quick_works, data_diagnostics])
    await session.flush()

    # ---- Services
    data_oil_filter_replacement = Service(
        name=oil_filter_replacement["name"],
        duration_minutes=oil_filter_replacement["duration_minutes"],
        price=oil_filter_replacement["price"],
        category=data_quick_works,
    )

    data_brake_diagnostics = Service(
        name=brake_diagnostics["name"],
        duration_minutes=brake_diagnostics["duration_minutes"],
        price=brake_diagnostics["price"],
        category=data_diagnostics,
    )

    session.add_all([data_oil_filter_replacement, data_brake_diagnostics])
    await session.flush()

    # ---- Bookings
    first_booking = Booking(
        service=data_oil_filter_replacement,
        booking_date=date.today(),
        start_time=time(hour=10, minute=0),
        end_time=time(hour=11, minute=0),
        user_id=test_liza_user.id,
    )

    second_booking = Booking(
        service=data_brake_diagnostics,
        booking_date=date.today(),
        start_time=time(hour=13, minute=0),
        end_time=time(hour=14, minute=0),
        user_id=test_liza_user.id,
    )

    session.add_all([first_booking, second_booking])

    # ---- Tg User
    first_tg_user = TgUser(
        telegram_id=123123123,
        phone_number="",
        first_name="homer_tg_user",
        last_name="homer_tg_user",
        username="homer_tg_user",
    )

    session.add(first_tg_user)
