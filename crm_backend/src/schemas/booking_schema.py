from pydantic import Field, field_serializer, field_validator
from schemas.base_schema import BaseSchema
from datetime import date, time, datetime
from typing import Annotated, Optional
import re


class CreateBookingResponseSchema(BaseSchema):
    service_id: Annotated[int, Field(ge=0)]
    booking_date: Annotated[
        date, Field(description="The date the booking was created.")
    ]
    start_time: Annotated[
        time, Field(description="The date the booking was started. Format: HH:MM")
    ]
    user_id: Annotated[Optional[int], Field(ge=0)] = None
    telegram_id: Annotated[Optional[int], Field(ge=0)] = None

    phone_number: Annotated[
        Optional[str], Field(min_length=5, max_length=20, description="Phone number")
    ] = None

    @field_validator("phone_number")
    def validate_phone_number(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value  # дозволяємо не передавати номер

        if not value.startswith("+"):
            value = value.strip().replace(" ", "")
            value = f"+{value}"

        if not re.match(r"^\+\d{5,15}$", value):
            raise ValueError("Phone number must be entered in the format: +999999999")

        return value


class CreateBookingSchema(CreateBookingResponseSchema):
    end_time: Annotated[
        Optional[time], Field(description="The date the booking was end.")
    ] = None
    is_verified: Annotated[
        Optional[bool], Field(description="Booking confirmation")
    ] = False


class ReadBookingShema(CreateBookingSchema):
    id: int
    end_time: time
    created_at: datetime
    updated_at: datetime

    @field_serializer("start_time", "end_time")
    def serialize_time(self, value: time) -> str:
        return value.strftime("%H:%M")


class ReadAvailableDateBookingSchema(BaseSchema):
    start: time
    end: time

    @field_serializer("start", "end")
    def serialize_time(self, value: time) -> str:
        return value.strftime("%H:%M")


class RegisterNewBookingSchema(BaseSchema):
    service_id: int
    booking_date: date
    start_time: time
    user_id: Optional[int] = None
    tg_user_id: Optional[int] = None
    end_time: Optional[time | None] = None
    is_verified: Annotated[
        Optional[bool], Field(description="Booking confirmation")
    ] = False


class BookingConfirmNotificationSchema(BaseSchema):
    booking_id: int
    tg_user_id: int
    text: str
    booking_date: str
    start_time: str


class IsVerifiedBookingResponseSchema(BaseSchema):
    booking_id: int
    is_verified: bool


class UpdateIsVerifiedSchema(BaseSchema):
    is_verified: bool


class QoeryBookingAllByUserSchema(BaseSchema):
    user_id: Annotated[Optional[int], Field(ge=0, description="Сгккуте user ID")] = None
    telegram_id: Annotated[
        Optional[int], Field(ge=0, description="Telegram user ID")
    ] = None
