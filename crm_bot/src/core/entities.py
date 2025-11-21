from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional


class CreateBookingSchema(BaseModel):
    service_id: int
    booking_date: datetime
    start_time: time
    phone_number: str
    telegram_id: int


class RegisterUserSchema(BaseModel):
    telegram_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None

    # model_config = ConfigDict(from_attributes=True)


class BookingConfirmNotificationSchema(BaseModel):
    tg_user_id: int
    text: str
    booking_date: str
    start_time: str
