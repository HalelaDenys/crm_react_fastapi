from schemas.service_shemas import CreateServiceSchema, ReadServiceSchema
from services.service_service import ServiceService, get_service
from fastapi import Depends, APIRouter, status, Path
from core.dependencies.authorization import check_user_is_admin
from core.config import settings
from typing import Annotated

router = APIRouter(prefix=settings.api_prefix.services, tags=["Services"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: CreateServiceSchema,
    service_service: Annotated["ServiceService", Depends(get_service)],
    is_admin: Annotated[bool, Depends(check_user_is_admin)],
) -> ReadServiceSchema:
    service = await service_service.add(data=service_data)
    return ReadServiceSchema(**service.to_dict())


@router.get("/categories/{category_id}", status_code=status.HTTP_200_OK)
async def get_services(
    category_id: Annotated[int, Path(ge=1)],
    service_service: Annotated["ServiceService", Depends(get_service)],
) -> list[ReadServiceSchema]:
    services = await service_service.get_all(category_id)
    return services


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_id: Annotated[int, Path(ge=1)],
    service_service: Annotated["ServiceService", Depends(get_service)],
    is_admin: Annotated[bool, Depends(check_user_is_admin)],
):
    await service_service.delete(service_id)
    return
