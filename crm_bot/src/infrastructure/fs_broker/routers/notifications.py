from faststream.rabbit import RabbitRouter
from faststream import Context
from typing import Annotated
from aiogram import Bot

from core.keyboards.inline_fabrics import inline_keyboard_builder
from core.entities import BookingConfirmNotificationSchema

notification_router = RabbitRouter()


@notification_router.subscriber(
    queue="booking.confirm.notification",
)
async def booking_confirm_notification(
    notification_date: BookingConfirmNotificationSchema,
    bot: Annotated[Bot, Context("bot")],
):
    await bot.send_message(
        chat_id=notification_date.tg_user_id,
        text=f"Підтвердіть бронювання на {notification_date.booking_date}, {notification_date.start_time}",
        reply_markup=inline_keyboard_builder(
            buttons=[
                {
                    "text": "Підтвердити",
                    "call": f"confirm_booking:{notification_date.booking_id}",
                },
                {
                    "text": "Скасувати",
                    "call": f"cancel_booking:{notification_date.booking_id}",
                },
            ]
        ),
    )
