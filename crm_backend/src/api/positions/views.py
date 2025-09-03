from schemas.position_shemas import ReadPositionSchema, CreatePositionSchema
from services.positiion_service import get_position_service, PositionService
from core.dependencies.authorization import check_user_is_admin
from fastapi import APIRouter, Depends, status, Path
from typing import Annotated
from core import settings


router = APIRouter(
    prefix=settings.api_prefix.positions,
    tags=["Positions"],
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_positions(
    position_service: Annotated["PositionService", Depends(get_position_service)],
    is_admin: Annotated[bool, Depends(check_user_is_admin)],
) -> list[ReadPositionSchema]:
    return await position_service.get_all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_position(
    position_data: CreatePositionSchema,
    position_service: Annotated["PositionService", Depends(get_position_service)],
    is_admin: Annotated[bool, Depends(check_user_is_admin)],
):
    position = await position_service.add(position_data)
    return ReadPositionSchema(**position.to_dict())


@router.delete("/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position(
    position_id: Annotated[int, Path(ge=1)],
    position_service: Annotated["PositionService", Depends(get_position_service)],
    is_admin: Annotated[bool, Depends(check_user_is_admin)],
):
    await position_service.delete(position_id=position_id)
    return
