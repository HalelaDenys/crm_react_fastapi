from core import (
    inline_keyboard_builder,
    BookingStateForm,
    api,
    inline_back_button,
    inline_menu_button,
)
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram_calendar import (
    SimpleCalendar,
    SimpleCalendarCallback,
    get_user_locale,
)

from core.keyboards.keyboard_btns import phone_number_kb

router = Router()


@router.callback_query(F.data == "create_booking")
async def create_booking(call: CallbackQuery, state: FSMContext):
    await state.set_state(BookingStateForm.category_id)
    categories_list = await api.get_category()
    print(call.from_user.id)
    await call.message.edit_text(
        "Виберіть категорію",
        reply_markup=inline_keyboard_builder(categories_list, back_cb="start"),
    )

@router.callback_query(F.data.startswith("category:"))
async def get_category(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    await state.update_data(category_id=category_id)
    await state.set_state(BookingStateForm.service_id)
    services_list = await api.get_service_by_category(category_id=category_id)

    await call.message.edit_text(
        "Виберіть послугу",
        reply_markup=inline_keyboard_builder(services_list, back_cb="create_booking"),
    )


@router.callback_query(F.data.startswith("service:"))
async def get_service(call: CallbackQuery, state: FSMContext):
    service_id = int(call.data.split(":")[1])
    await state.update_data(service_id=service_id)
    await state.set_state(BookingStateForm.date)
    state_data = await state.get_data()

    calendar_kb = await SimpleCalendar(
        locale=await get_user_locale(call.from_user)
    ).start_calendar()

    calendar_kb.inline_keyboard.append(
        [
            inline_back_button(back_cb=f"category:{state_data.get('category_id')}"),
        ]
    )

    await call.message.edit_text(
        "Виберіть дату, на яку хочете записатися:",
        reply_markup=calendar_kb,
    )


@router.callback_query(SimpleCalendarCallback.filter())
async def get_the_date_from_the_calendar(
    call: CallbackQuery, callback_data: CallbackData, state: FSMContext
):
    calendar = SimpleCalendar(
        locale=await get_user_locale(call.from_user), show_alerts=True
    )
    selected, date = await calendar.process_selection(call, callback_data)

    if selected:
        await state.update_data(date=date.strftime("%Y-%m-%d"))
        await state.set_state(BookingStateForm.time)
        state_data = await state.get_data()
        service_id = int(state_data.get("service_id"))

        available_slots = await api.get_available_slots(
            service_id=service_id,
            booking_date=date.strftime("%Y-%m-%d"),
        )
        await call.message.edit_text(
            f'На цей дету {date.strftime("%Y-%m-%d")}, доступен такий час: ',
            reply_markup=inline_keyboard_builder(
                available_slots, sizes=3, back_cb=f"service:{service_id}"
            ),
        )


@router.callback_query(F.data.startswith("recording_time:"))
async def get_recording_time(call: CallbackQuery, state: FSMContext):
    start_time = call.data.split(":")[1]
    await state.update_data(time=start_time.replace("-", ":"))
    await state.set_state(BookingStateForm.phone_number)

    await call.message.edit_text("Будь ласка, поділіться номером телефону 👇")

    await call.message.answer(
        "Натисніть кнопку нижче, щоб поділитися номером",
        reply_markup=phone_number_kb,
    )


@router.message(F.contact)
async def save_contact(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)

    thank_msg = await message.answer("Дякую!", reply_markup=ReplyKeyboardRemove())

    await message.delete()

    await message.answer(
        "Ваше бронювання обробляється. Для підтвердження бот надішле вам повідомлення",
        reply_markup=inline_menu_button(),
    )

    await thank_msg.delete()
