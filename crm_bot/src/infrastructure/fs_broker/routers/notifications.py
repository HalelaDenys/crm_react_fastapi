from faststream.rabbit import RabbitRouter
from faststream import Context
from typing import Annotated
from aiogram import Bot

from core.entities import BookingConfirmNotificationSchema

notification_router = RabbitRouter()


@notification_router.subscriber(
    queue="booking.confirm.notification",
    # exchange="bot.booking",
)
async def booking_confirm_notification(
    notification_date: BookingConfirmNotificationSchema,
    bot: Annotated[Bot, Context("bot")],
):
    await bot.send_message(
        chat_id=notification_date.tg_user_id, text=notification_date.text
    )
