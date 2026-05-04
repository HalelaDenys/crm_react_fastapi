from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from core.keyboards.keyboard_btns import phone_number_kb
from aiogram.filters.callback_data import CallbackData
from faststream.exceptions import FastStreamException
from core.entities import CreateBookingSchema, IsVerifiedBookingSchema
from aiogram.fsm.context import FSMContext
from infrastructure import container
from core import (
    inline_keyboard_builder_with_pagination,
    inline_keyboard_builder,
    inline_back_button,
    inline_menu_button,
    BookingStateForm,
    settings,
)
from aiogram import Router, F
from aiogram_calendar import (
    SimpleCalendar,
    SimpleCalendarCallback,
    get_user_locale,
)
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "create_booking")
async def create_booking(call: CallbackQuery, state: FSMContext):
    """
    Починає процес створення замовлення
    """
    await state.set_state(BookingStateForm.category_id)
    categories_list = await container.api.get_category()
    await call.message.edit_text(
        "Виберіть категорію",
        reply_markup=inline_keyboard_builder(categories_list, back_cb="start"),
    )


# category:{category_id}:{page}
@router.callback_query(F.data.startswith("category:"), BookingStateForm.category_id)
async def get_category(call: CallbackQuery, state: FSMContext):
    """
    приймає катерогія та поверає послуги за категоріею
    """
    _, category_id, page = call.data.split(":")

    await state.update_data(category_id=category_id)
    await state.set_state(BookingStateForm.service_id)

    services_list, hes_next = await container.api.get_service_by_category(
        category_id=category_id,
        page=int(page),
        limit=settings.pag.limit_service,
    )

    try:
        await call.message.edit_text(
            text="Виберіть послугу",
            reply_markup=inline_keyboard_builder_with_pagination(
                buttons=services_list,
                back_cb="create_booking",
                pg_coll_prefix=f"category:{category_id}",
                page=int(page),
                hes_next=hes_next,
            ),
        )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


@router.callback_query(F.data.startswith("service:"), BookingStateForm.service_id)
async def get_service(call: CallbackQuery, state: FSMContext):
    """
    приймає послугу та поертає календер
    """
    service_id = int(call.data.split(":")[1])
    await state.update_data(service_id=service_id)
    await state.set_state(BookingStateForm.booking_date)
    state_data = await state.get_data()

    calendar_kb = await SimpleCalendar(
        locale=await get_user_locale(call.from_user)
    ).start_calendar()

    call_back_data = f"category:{state_data.get('category_id')}:1"
    calendar_kb.inline_keyboard.append(
        [
            inline_back_button(back_cb=call_back_data),
        ]
    )

    await call.message.edit_text(
        "Виберіть дату, на яку хочете записатися:",
        reply_markup=calendar_kb,
    )


@router.callback_query(SimpleCalendarCallback.filter(), BookingStateForm.booking_date)
async def get_the_date_from_the_calendar(
    call: CallbackQuery, callback_data: CallbackData, state: FSMContext
):
    """
    оброблає календар та вопертає доспутний час на вказаний день
    """
    calendar = SimpleCalendar(
        locale=await get_user_locale(call.from_user), show_alerts=True
    )
    selected, date = await calendar.process_selection(call, callback_data)
    if selected:
        await state.update_data(booking_date=date.strftime("%Y-%m-%d"))
        await state.set_state(BookingStateForm.start_time)
        state_data = await state.get_data()
        service_id = int(state_data.get("service_id"))

        available_slots = await container.api.get_available_slots(
            service_id=service_id,
            booking_date=date.strftime("%Y-%m-%d"),
        )
        await call.message.edit_text(
            f'На цею дету {date.strftime("%Y-%m-%d")}, доступен такий час: ',
            reply_markup=inline_keyboard_builder(
                available_slots, sizes=3, back_cb=f"service:{service_id}"
            ),
        )


@router.callback_query(
    F.data.startswith("recording_time:"), BookingStateForm.start_time
)
async def get_recording_time(call: CallbackQuery, state: FSMContext):
    """
    приймає час та відправляю кнопку для номера телефону
    """
    start_time = call.data.split(":")[1]
    await state.update_data(start_time=start_time.replace("-", ":"))
    await state.set_state(BookingStateForm.phone_number)

    await call.message.edit_text("Будь ласка, поділіться номером телефону 👇")

    await call.message.answer(
        "Натисніть кнопку нижче, щоб поділитися номером",
        reply_markup=phone_number_kb,
    )


@router.message(F.contact, BookingStateForm.phone_number)
async def save_contact(message: Message, state: FSMContext):
    """
    оброблає номер телефону та завершаю бронювання
    """
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)

    thank_msg = await message.answer("Дякую!", reply_markup=ReplyKeyboardRemove())

    await message.delete()
    state_data = await state.get_data()
    await state.clear()

    booking_data = CreateBookingSchema(
        service_id=state_data.get("service_id"),
        booking_date=state_data.get("booking_date"),
        start_time=state_data.get("start_time"),
        phone_number=state_data.get("phone_number"),
        telegram_id=message.from_user.id,
    )

    try:
        logging.info("Publishing booking_data")
        await container.broker.publish(
            booking_data.model_dump(mode="json"),
            queue="booking.created",
            headers={"authorization": f"Bearer {settings.fs.tg_api_secret}"},
        )
        logging.info("Published successfully")
    except FastStreamException as e:
        logging.error("Failed to publish message: %s", e)

    await message.answer(
        "Ваше бронювання обробляється. Для підтвердження бот надішле вам повідомлення",
        reply_markup=inline_menu_button(),
    )

    await thank_msg.delete()


@router.callback_query(F.data.regexp(r"^(confirm_booking|cancel_booking)"))
async def confirm_booking(call: CallbackQuery):
    data = call.data.split(":")
    is_verified = data[0] == "confirm_booking"

    booking_date = IsVerifiedBookingSchema(
        booking_id=int(data[1]),
        is_verified=is_verified,
    )
    try:
        await container.broker.publish(
            booking_date.model_dump(mode="json"),
            queue="booking.verified",
            headers={"authorization": f"Bearer {settings.fs.tg_api_secret}"},
        )
        logging.info("Published successfully")

    except FastStreamException as e:
        logging.error("Failed to publish message: %s", e)

    text = (
        "Підтвердження бронювання в обробці."
        if is_verified
        else "Відмінна бронювання в обробці."
    )

    await call.message.edit_text(
        f"{text}",
    )
