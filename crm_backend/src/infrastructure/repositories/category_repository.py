from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio.session import AsyncSession
from infrastructure import Category


class CategoryRepository(SQLAlchemyRepository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)
