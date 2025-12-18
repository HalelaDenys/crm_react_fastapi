from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import Union, Sequence
from infrastructure import Booking, TgUser
from datetime import date, time
from sqlalchemy import select


class BookingRepository(SQLAlchemyRepository[Booking]):
    def __init__(self, session: AsyncSession):
        super().__init__(Booking, session)

    async def find_all_by_booking_date(self, booking_date: date) -> Sequence[Booking]:
        stmt = (
            select(self._model)
            .where(self._model.booking_date == booking_date)
            .order_by(self._model.start_time)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def access_check_reservation(
        self, booking_date: date, start_time: time
    ) -> Union[Booking, None]:
        stmt = select(self._model).where(
            self._model.booking_date == booking_date,
            self._model.start_time == start_time,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all_bookings_by_user(
        self,
        *,
        telegram_id: Union[int, None] = None,
        user_id: Union[int, None] = None,
    ) -> Sequence[Booking]:
        if telegram_id is None and user_id is None:
            raise ValueError("Потрібно передати telegram_id або user_id")

        stmt = select(self._model)

        if telegram_id is not None:
            stmt = stmt.join(TgUser, TgUser.id == self._model.tg_user_id).where(
                TgUser.telegram_id == telegram_id
            )

        if user_id is not None:
            stmt = stmt.where(self._model.user_id == user_id)

        stmt = stmt.order_by(self._model.created_at)

        res = await self._session.execute(stmt)
        return res.scalars().all()
