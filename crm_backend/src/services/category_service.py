from infrastructure import db_helper, CategoryRepository, Category
from core.exceptions import NotFoundError, AlreadyExistsError
from sqlalchemy.ext.asyncio import AsyncSession
from services.base_service import BaseService
from typing import AsyncGenerator
from schemas.category_schema import CreateCategorySchema, ReadCategorySchema


class CategoryService(BaseService):
    def __init__(self, session: AsyncSession):
        self._category_repository = CategoryRepository(session)

    async def add(self, data: CreateCategorySchema) -> Category:
        if await self._category_repository.find_single(name=data.name):
            raise AlreadyExistsError("Category already exists")
        category = await self._category_repository.create(data)
        return category

    async def update(self, category_id: int, data):
        pass

    async def delete(self, category_id: int) -> None:
        await self.get(id=category_id)
        await self._category_repository.delete(id=category_id)

    async def get(self, **kwargs) -> Category:
        if not (category := await self._category_repository.find_single(**kwargs)):
            raise NotFoundError("Category not found")
        return category

    async def get_all(self) -> list[ReadCategorySchema]:
        categories = await self._category_repository.find_all()
        return [ReadCategorySchema(**category.to_dict()) for category in categories]


async def get_category_service() -> AsyncGenerator["CategoryService", None]:
    async with db_helper.get_session() as session:
        yield CategoryService(session)
