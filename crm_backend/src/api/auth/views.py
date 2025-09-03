from fastapi import Depends, APIRouter, status
from typing import Annotated
from core import settings, Security
from core.dependencies.authorization import (
    get_current_auth_user_for_refresh,
    authenticate_user,
)
from infrastructure import Employee
from schemas.employee_shemas import TokenInfo

router = APIRouter(prefix=settings.api_prefix.auth, tags=["Auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    employee_data: Annotated["Employee", Depends(authenticate_user)],
) -> TokenInfo:
    access_token = Security.create_access_token(employee_data)
    refresh_token = Security.create_refresh_token(employee_data)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_none=True,
    summary="refresh user",
    status_code=status.HTTP_200_OK,
)
async def create_new_access_token(
    current_user: Annotated[Employee, Depends(get_current_auth_user_for_refresh)],
):
    access_token = Security.create_access_token(current_user)
    return TokenInfo(
        access_token=access_token,
    )
