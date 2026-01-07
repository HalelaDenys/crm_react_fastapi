import pytest_asyncio
from infrastructure import UserRepository, EmployeeRepository
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture
async def user_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


@pytest_asyncio.fixture
async def employee_repo(db_session: AsyncSession) -> EmployeeRepository:
    return EmployeeRepository(db_session)
