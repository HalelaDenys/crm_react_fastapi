from aiogram.fsm.state import State, StatesGroup


class BookingStateForm(StatesGroup):
    category_id = State()
    service_id = State()
    date = State()
    time = State()
    phone_number = State()
