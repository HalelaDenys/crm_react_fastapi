from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository
from infrastructure.db.models.employee import Employee
from core.utils.query_filters import query_filters
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, desc
from sqlalchemy.orm import joinedload
from typing import Sequence, Optional
from datetime import date


class EmployeeRepository(SQLAlchemyRepository[Employee]):
    def __init__(self, session: AsyncSession):
        super().__init__(Employee, session)

    async def find_all(
        self,
        sort_order: str,
        sort_by: str,
        status: str,
        search: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> Sequence[Employee]:
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

    async def find_single(self, **filters) -> Employee:
        stmt = (
            select(self._model)
            .options(joinedload(self._model.position))
            .filter_by(**filters)
            .order_by(self._model.id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
