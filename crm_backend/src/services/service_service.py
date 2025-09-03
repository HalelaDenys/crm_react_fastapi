from infrastructure import db_helper, CategoryRepository, Service
from core.exceptions import NotFoundError, AlreadyExistsError
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories.service_repository import ServiceRepository
from schemas.service_shemas import CreateServiceSchema, ReadServiceSchema
from services.base_service import BaseService
from typing import AsyncGenerator


class ServiceService(BaseService):
    def __init__(self, session: AsyncSession):
        self._service_repository = ServiceRepository(session)

    async def add(self, data: CreateServiceSchema) -> Service:
        if await self._service_repository.find_single(name=data.name):
            raise AlreadyExistsError("Service already exists")
        service = await self._service_repository.create(data)
        return service

    async def update(self, data) -> Service:
        pass

    async def delete(self, service_id) -> None:
        await self.get(id=service_id)
        await self._service_repository.delete(id=service_id)

    async def get(self, **kwargs):
        if not (service := await self._service_repository.find_single(**kwargs)):
            raise NotFoundError("Service not found")
        return service

    async def get_all(self, category_id) -> list[ReadServiceSchema]:
        services = await self._service_repository.find_all(category_id=category_id)
        return [ReadServiceSchema(**service.to_dict()) for service in services]


async def get_service() -> AsyncGenerator["ServiceService", None]:
    async with db_helper.get_session() as session:
        yield ServiceService(session)
