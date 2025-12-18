from schemas.user_schema import UpdatePhoneNumberTgUserSchema
from core.exceptions import NotFoundError, AlreadyExistsError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime, date
from services.base_service import BaseService
from schemas.booking_schema import (
    ReadAvailableDateBookingSchema,
    CreateBookingResponseSchema,
    ReadBookingShema,
    IsVerifiedBookingResponseSchema,
    RegisterNewBookingSchema,
    CreateBookingSchema,
    UpdateIsVerifiedSchema,
    QoeryBookingAllByUserSchema,
)
from typing import AsyncGenerator
from infrastructure import (
    db_helper,
    Booking,
    BookingRepository,
    ServiceRepository,
    Service,
    TgUserRepository,
)
from core import settings


class BookingService(BaseService):
    def __init__(self, session: AsyncSession):
        self._booking_repository = BookingRepository(session)
        self._service_repository = ServiceRepository(session)
        self._tg_user_repository = TgUserRepository(session)

    async def add(self, data: CreateBookingResponseSchema) -> Booking:
        # check service
        if not (
            service := await self._service_repository.find_single(id=data.service_id)
        ):
            raise NotFoundError("Service not found")

        # check if the booking time is available
        if await self._booking_repository.access_check_reservation(
            booking_date=data.booking_date, start_time=data.start_time
        ):
            raise AlreadyExistsError(
                f"Booking with start date {data.start_time} already exists"
            )

        booking_data = CreateBookingSchema(**data.model_dump())
        booking_data.end_time = (
            (
                datetime.combine(datetime.today(), data.start_time)
                + timedelta(minutes=service.duration_minutes)
            )
            + settings.booking.buffer
        ).time()

        new_booking_data = await self.__user_verification(booking_data)

        return await self._booking_repository.create(data=new_booking_data)

    async def update(
        self, booking_id: int, data: IsVerifiedBookingResponseSchema
    ) -> None | Booking:
        await self.get(id=booking_id)

        if not data.is_verified:
            await self.delete(booking_id=booking_id)
            return None

        return await self._booking_repository.update(
            id=booking_id, data=UpdateIsVerifiedSchema(is_verified=data.is_verified)
        )

    async def delete(self, booking_id: int) -> None:
        await self.get(id=booking_id)
        await self._booking_repository.delete(id=booking_id)

    async def get(self, **kwargs) -> Booking:
        if not (booking := await self._booking_repository.find_single(**kwargs)):
            raise NotFoundError("Booking not found")
        return booking

    async def get_all(self, booking_date: str) -> list[ReadBookingShema]:
        bookings = await self._booking_repository.find_all(
            booking_date=date.fromisoformat(booking_date)
        )

        return [ReadBookingShema(**booking.to_dict()) for booking in bookings]

    async def get_available_slots(
        self, service_id: int, booking_date: str
    ) -> list[ReadAvailableDateBookingSchema] | None:
        slots: list[ReadAvailableDateBookingSchema] = []
        booking_dt = datetime.fromisoformat(booking_date).date()
        now = datetime.now()

        service: "Service" = await self._service_repository.find_single(id=service_id)
        duration_service_minutes = timedelta(minutes=service.duration_minutes)
        buffer = settings.booking.buffer

        work_start = datetime.combine(booking_dt, settings.booking.work_start)
        work_end = datetime.combine(booking_dt, settings.booking.work_end)

        if booking_dt == now.date():
            current_time = now.replace(minute=0, second=0, microsecond=0)
            work_start = max(current_time, work_start)  # не раніше 09:00

        bookings = await self._booking_repository.find_all_by_booking_date(
            booking_date=booking_dt
        )

        while (work_start + duration_service_minutes) <= work_end:
            slot_start = work_start
            slot_end = work_start + duration_service_minutes + buffer

            overlap = any(
                slot_start < datetime.combine(booking_dt, b.end_time)
                and slot_end > datetime.combine(booking_dt, b.start_time)
                for b in bookings
            )

            if not overlap:
                slots.append(
                    ReadAvailableDateBookingSchema(
                        start=slot_start.time(),
                        end=slot_end.time(),
                    )
                )

            work_start += duration_service_minutes + settings.booking.buffer

        return slots

    async def __user_verification(
        self, booking_data: CreateBookingSchema
    ) -> RegisterNewBookingSchema:
        if booking_data.user_id is not None:  # якщо дуло створенно менеджером
            booking_data.is_verified = True

        if booking_data.telegram_id is not None:  # якщо дуло створенно через телеграм
            tg_user = await self._tg_user_repository.find_single(
                telegram_id=booking_data.telegram_id
            )

            if tg_user.phone_number is None and booking_data.phone_number is not None:
                await self._tg_user_repository.update(
                    data=UpdatePhoneNumberTgUserSchema(
                        phone_number=booking_data.phone_number
                    ),
                    telegram_id=booking_data.telegram_id,
                )

        return RegisterNewBookingSchema(
            service_id=booking_data.service_id,
            booking_date=booking_data.booking_date,
            start_time=booking_data.start_time,
            end_time=booking_data.end_time,
            user_id=booking_data.user_id,
            tg_user_id=tg_user.id,
            is_verified=booking_data.is_verified,
        )

    async def get_all_bookings_by_user(
        self, q_data: QoeryBookingAllByUserSchema
    ) -> list[ReadBookingShema]:
        bookings = await self._booking_repository.find_all_bookings_by_user(
            telegram_id=q_data.telegram_id, user_id=q_data.user_id
        )
        return [ReadBookingShema(**booking.to_dict()) for booking in bookings]


async def get_booking_service() -> AsyncGenerator["BookingService", None]:
    async with db_helper.get_session() as session:
        yield BookingService(session)
