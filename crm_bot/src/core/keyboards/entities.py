from pydantic import BaseModel
from datetime import datetime, time


class CreateBookingSchema(BaseModel):
    service_id: int
    booking_date: datetime
    start_time: time
    phone_number: str
    telegram_id: int
