from services.booking_service import BookingService, get_booking_service
from services.tg_user_service import TgUserService, get_tg_user_service
from core.dependencies.authorization import verify_tg_request
from schemas.booking_schema import (
    CreateBookingResponseSchema,
    BookingConfirmNotificationSchema,
    IsVerifiedBookingResponseSchema,
)
from faststream.rabbit import RabbitRouter
from faststream import Depends
from typing import Annotated
from core import settings
from ..broker import broker

booking_router = RabbitRouter()


@booking_router.subscriber(
    "booking.created",
)
async def register_new_booking(
    booking_data: CreateBookingResponseSchema,
    _: Annotated[None, Depends(verify_tg_request)],
    booking_service: Annotated["BookingService", Depends(get_booking_service)],
    tg_user_service: Annotated["TgUserService", Depends(get_tg_user_service)],
):
    booking = await booking_service.add(data=booking_data)

    if booking:
        tg_user = await tg_user_service.get(id=booking.tg_user_id)
        con_data = BookingConfirmNotificationSchema(
            booking_id=booking.id,
            tg_user_id=tg_user.telegram_id,
            text="Підтвердіть бронювання",
            booking_date=booking.booking_date.strftime("%Y/%m/%d"),
            start_time=booking.start_time.strftime("%H:%M"),
        )
        await broker.publish(
            con_data.model_dump(mode="json"),
            # exchange="bot.booking",
            queue="booking.confirm.notification",
            routing_key="booking.confirm.notification",
        )


@booking_router.subscriber(
    "booking.verified",
)
async def confirm_booking_verified(
    booking_data: IsVerifiedBookingResponseSchema,
    _: Annotated[None, Depends(verify_tg_request)],
    booking_service: Annotated["BookingService", Depends(get_booking_service)],
):
    await booking_service.update(
        booking_id=booking_data.booking_id,
        data=booking_data,
    )
