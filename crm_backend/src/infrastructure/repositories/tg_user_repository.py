from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository
from infrastructure.db.models.tg_user import TgUser
from sqlalchemy.ext.asyncio import AsyncSession


class TgUserRepository(SQLAlchemyRepository[TgUser]):
    def __init__(self, session: AsyncSession):
        super().__init__(TgUser, session)
