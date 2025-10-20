from core.dependencies.authorization import check_user_is_admin
from infrastructure.fs_broker.broker import broker
from fastapi import Depends, APIRouter, status
from schemas.user_schema import TgUserSchema
from fastapi.responses import ORJSONResponse
from typing import Annotated
from core import settings


router = APIRouter(prefix=settings.api_prefix.tg_users, tags=["Tg Users"])


@router.post("", status_code=200)
async def create_tg_users(
    user_data: TgUserSchema,
    is_admin: Annotated[bool, Depends(check_user_is_admin)],
):
    """
    Created for testing purposes
    """
    await broker.publish(
        user_data,
        queue="tg_users.created",
        headers={"authorization": f"Bearer {settings.jwt.tg_api_secret}"},
    )
    return ORJSONResponse(
        status_code=status.HTTP_201_CREATED, content={"success": True}
    )
