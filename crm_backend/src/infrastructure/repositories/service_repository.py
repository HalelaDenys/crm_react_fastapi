from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository
from infrastructure.db.models.service import Service
from sqlalchemy.ext.asyncio import AsyncSession


class ServiceRepository(SQLAlchemyRepository[Service]):
    def __init__(self, session: AsyncSession):
        super().__init__(Service, session)
