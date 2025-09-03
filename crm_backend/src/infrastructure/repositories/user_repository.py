from core.utils.query_filters import query_filters
from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, asc
from typing import Sequence, Optional
from infrastructure import User
from datetime import date


class UserRepository(SQLAlchemyRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def find_all(
        self,
        sort_order: str,
        sort_by: str,
        status: str,
        search: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> Sequence[User]:
        sort_column = getattr(self._model, sort_by, None)

        stmt = select(self._model).order_by(
            asc(sort_column) if sort_order == "asc" else desc(sort_column)
        )

        stmt = query_filters(
            stmt=stmt,
            model=self._model,
            status=status,
            search=search,
            date_from=date_from,
            date_to=date_to,
        )

        result = await self._session.execute(stmt)
        return result.scalars().all()
