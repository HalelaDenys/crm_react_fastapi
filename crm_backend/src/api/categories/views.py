from schemas.category_schema import ReadCategorySchema, CreateCategorySchema
from services.category_service import get_category_service, CategoryService
from fastapi import Depends, APIRouter, status, Path
from core.dependencies.authorization import check_user_is_admin
from core.config import settings
from typing import Annotated

router = APIRouter(prefix=settings.api_prefix.categories, tags=["Categories"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CreateCategorySchema,
    category_service: Annotated["CategoryService", Depends(get_category_service)],
    current_user: Annotated[bool, Depends(check_user_is_admin)],
) -> ReadCategorySchema:
    category = await category_service.add(data=category_data)
    return ReadCategorySchema(**category.to_dict())


@router.get("", status_code=status.HTTP_200_OK)
async def get_categories(
    category_service: Annotated["CategoryService", Depends(get_category_service)],
) -> list[ReadCategorySchema]:
    return await category_service.get_all()


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: Annotated[int, Path(ge=1)],
    category_service: Annotated["CategoryService", Depends(get_category_service)],
    current_user: Annotated[bool, Depends(check_user_is_admin)],
) -> None:
    await category_service.delete(category_id=category_id)
    return
