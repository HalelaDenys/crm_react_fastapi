from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository
from infrastructure.db.models.service import Service
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Sequence


class ServiceRepository(SQLAlchemyRepository[Service]):
    def __init__(self, session: AsyncSession):
        super().__init__(Service, session)

    async def find_all_pag(
        self, category_id: int, page: int = 1, limit: int = 10
    ) -> tuple[Sequence[Service], bool]:
        offset = (page - 1) * limit

        res = await self._session.execute(
            select(self._model)
            .where(self._model.category_id == category_id)
            .limit(limit + 1)
            .offset(offset)
            .order_by(self._model.id)
        )
        items = res.scalars().all()
        has_next = len(items) > limit
        return items[:limit], has_next
