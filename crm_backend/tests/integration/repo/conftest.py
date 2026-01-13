import pytest_asyncio
from infrastructure import (
    UserRepository,
    EmployeeRepository,
    PositionRepository,
    CategoryRepository,
    ServiceRepository,
    BookingRepository,
)
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date


@pytest_asyncio.fixture
async def user_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


@pytest_asyncio.fixture
async def employee_repo(db_session: AsyncSession) -> EmployeeRepository:
    return EmployeeRepository(db_session)


@pytest_asyncio.fixture
async def pos_repo(db_session: AsyncSession) -> PositionRepository:
    return PositionRepository(db_session)


@pytest_asyncio.fixture
async def category_repo(db_session: AsyncSession) -> CategoryRepository:
    return CategoryRepository(db_session)


@pytest_asyncio.fixture
async def service_repo(db_session: AsyncSession) -> ServiceRepository:
    return ServiceRepository(db_session)


@pytest_asyncio.fixture
async def booking_repo(db_session: AsyncSession) -> BookingRepository:
    return BookingRepository(db_session)


@pytest_asyncio.fixture
def b_date() -> date:
    """
    Returns a random date for testing.
    """
    return date.today()
