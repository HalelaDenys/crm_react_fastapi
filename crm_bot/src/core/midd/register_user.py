from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Callable, Dict, Awaitable
from infrastructure import broker
from core.entities import RegisterUserSchema
from core import settings
from faststream.exceptions import FastStreamException

import logging

logger = logging.getLogger(__name__)


class RegisterUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ):
        if event.text == "/start":
            pass
        user_data = RegisterUserSchema(
            telegram_id=event.from_user.id,
            first_name=event.from_user.first_name,
            last_name=event.from_user.last_name,
            username=event.from_user.username,
        )

        try:
            logging.info(f"Publishing %s", user_data)
            await broker.publish(
                user_data.model_dump(),
                queue="tg_users.created",
                headers={"authorization": f"Bearer {settings.fs.tg_api_secret}"},
            )
            logging.info("Published successfully")
        except FastStreamException as e:
            logging.error("Failed to publish message: %s", e)

        return await handler(event, data)
