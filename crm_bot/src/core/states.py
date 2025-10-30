from aiogram.fsm.state import State, StatesGroup


class BookingStateForm(StatesGroup):
    category_id = State()
    service_id = State()
    booking_date = State()
    start_time = State()
    phone_number = State()
