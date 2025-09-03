from services.booking_service import BookingService, get_booking_service
from core.dependencies.authorization import check_user_is_admin
from fastapi import APIRouter, Query, Depends, status, Path
from schemas.booking_schema import (
    ReadAvailableDateBookingSchema,
    CreateBookingResponseSchema,
    ReadBookingShema,
)
from typing import Annotated
from core import settings

router = APIRouter(prefix=settings.api_prefix.booking, tags=["Booking"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def create_booking(
    booking_data: CreateBookingResponseSchema,
    booking_service: Annotated["BookingService", Depends(get_booking_service)],
) -> ReadBookingShema:
    booking = await booking_service.add(data=booking_data)
    return ReadBookingShema(**booking.to_dict())


@router.get(
    "/services/{service_id}/available-slots",
    status_code=status.HTTP_200_OK,
)
async def get_available_slots(
    service_id: int,
    booking_date: Annotated[str, Query(description="Дата у форматі YYYY-MM-DD")],
    booking_service: Annotated["BookingService", Depends(get_booking_service)],
) -> list[ReadAvailableDateBookingSchema]:
    slot = await booking_service.get_available_slots(
        service_id=service_id,
        booking_date=booking_date,
    )
    return slot


@router.delete("{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking_id: Annotated[int, Path(ge=0)],
    is_admin: Annotated[bool, Depends(check_user_is_admin)],
    booking_service: Annotated["BookingService", Depends(get_booking_service)],
) -> None:
    await booking_service.delete(booking_id=booking_id)
    return
