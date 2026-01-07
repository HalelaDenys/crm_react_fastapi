import pytest_asyncio
from infrastructure.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture
async def user_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)
