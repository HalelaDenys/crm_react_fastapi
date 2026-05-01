from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository
from infrastructure.db.models.tg_users import TgUser
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel


class TgUserRepository(SQLAlchemyRepository[TgUser]):
    def __init__(self, session: AsyncSession):
        super().__init__(TgUser, session)

    async def create(self, data: BaseModel):
        stmt = insert(self._model).values(**data.model_dump())

        stmt = stmt.on_conflict_do_nothing(
            index_elements=["telegram_id"],
        ).returning(TgUser)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
