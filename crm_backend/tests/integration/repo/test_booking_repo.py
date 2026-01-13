import pytest
from schemas.booking_schema import RegisterNewBookingSchema
from datetime import date, time
from infrastructure import BookingRepository, Booking


@pytest.mark.asyncio
class TestBookingRepo:
    async def test_create_booking(
        self, booking_repo: BookingRepository, b_date: date
    ) -> None:
        data = RegisterNewBookingSchema(
            service_id=1,
            booking_date=b_date,
            start_time=time(hour=15, minute=0),
            user_id=1,
            end_time=time(hour=16, minute=0),
        )

        booking = await booking_repo.create(data)

        assert booking is not None

    async def test_find_all_by_booking_date(
        self, booking_repo: BookingRepository, b_date: date
    ) -> None:
        bookings = await booking_repo.find_all_by_booking_date(
            booking_date=date.today()
        )

        assert len(bookings) > 0
        assert bookings[0].booking_date == b_date
        assert bookings[1].booking_date == b_date
        assert isinstance(bookings[0], Booking)

    @pytest.mark.parametrize(
        "s_time, is_answer",
        [
            (time(hour=10, minute=0), True),
            (time(hour=13, minute=0), True),
            (time(hour=16, minute=0), False),
        ],
    )
    async def test_access_check_reservation(
        self,
        booking_repo: BookingRepository,
        b_date: date,
        s_time: time,
        is_answer: bool,
    ) -> None:
        booking = await booking_repo.access_check_reservation(
            booking_date=b_date,
            start_time=s_time,
        )
        if is_answer:
            assert booking is not None
        else:
            assert booking is None

    async def test_find_all_bookings_by_user(
        self, booking_repo: BookingRepository
    ) -> None:
        booking = await booking_repo.find_all_bookings_by_user(user_id=1)

        assert booking is not None
        assert isinstance(booking[0], Booking)

    async def test_delete_booking(self, booking_repo: BookingRepository) -> None:
        await booking_repo.delete(id=1)

        booking = await booking_repo.find_single(id=1)

        assert booking is None
