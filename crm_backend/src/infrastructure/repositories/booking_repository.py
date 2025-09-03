from typing import Union

from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio.session import AsyncSession
from infrastructure import Booking
from sqlalchemy import select, or_, and_
from datetime import date, time


class BookingRepository(SQLAlchemyRepository[Booking]):
    def __init__(self, session: AsyncSession):
        super().__init__(Booking, session)

    async def find_all(self, booking_date: date):
        stmt = (
            select(self._model)
            .where(self._model.booking_date == booking_date)
            .order_by(self._model.start_date)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
