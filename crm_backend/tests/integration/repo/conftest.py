import pytest_asyncio
from infrastructure import (
    UserRepository,
    EmployeeRepository,
    PositionRepository,
    CategoryRepository,
)
from sqlalchemy.ext.asyncio import AsyncSession


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
