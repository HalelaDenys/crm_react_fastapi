from services.tg_user_service import get_tg_user_service, TgUserService
from core.dependencies.authorization import verify_tg_request
from schemas.user_schema import TgUserSchema
from faststream.rabbit import RabbitRouter
from faststream import Depends
from typing import Annotated


tg_user_router = RabbitRouter()


@tg_user_router.subscriber("tg_users.created")
async def create_tg_user(
    user_data: TgUserSchema,
    _: Annotated[None, Depends(verify_tg_request)],
    tg_user_service: Annotated["TgUserService", Depends(get_tg_user_service)],
):
    await tg_user_service.add(data=user_data)
