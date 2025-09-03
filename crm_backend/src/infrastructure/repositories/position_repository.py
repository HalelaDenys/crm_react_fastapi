from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository
from infrastructure.db.models.position import Position
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence


class PositionRepository(SQLAlchemyRepository[Position]):
    def __init__(self, session: AsyncSession):
        super().__init__(Position, session)

    async def find_all(self) -> Sequence[Position]:
        stmt = select(self._model).order_by(self._model.id)
        result = await self._session.execute(stmt)
        return result.scalars().all()
