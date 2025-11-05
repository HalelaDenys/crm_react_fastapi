from services.booking_service import BookingService, get_booking_service
from core.dependencies.authorization import verify_tg_request
from schemas.booking_schema import CreateBookingResponseSchema
from faststream.rabbit import RabbitRouter
from faststream import Depends
from typing import Annotated


booking_router = RabbitRouter()


@booking_router.subscriber(
    "booking.created",
    exchange="booking.created",
)
async def register_new_booking(
    booking_data: CreateBookingResponseSchema,
    _: Annotated[None, Depends(verify_tg_request)],
    booking_service: Annotated["BookingService", Depends(get_booking_service)],
):
    await booking_service.add(data=booking_data)
