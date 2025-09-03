from infrastructure import PositionRepository, Position, db_helper
from schemas.position_shemas import ReadPositionSchema, CreatePositionSchema
from sqlalchemy.ext.asyncio import AsyncSession
from services.base_service import BaseService
from core.exceptions import NotFoundError, AlreadyExistsError
from typing import AsyncGenerator


class PositionService(BaseService):
    def __init__(self, session: AsyncSession):
        self._position_repository = PositionRepository(session)

    async def add(self, data: CreatePositionSchema) -> Position:
        if await self._position_repository.find_single(name=data.name):
            raise AlreadyExistsError("Position already exists")
        return await self._position_repository.create(data)

    async def update(self, **kwargs):
        pass

    async def delete(self, position_id):
        await self.get(id=position_id)
        return await self._position_repository.delete(id=position_id)

    async def get(self, **kwargs) -> Position:
        if not (position := await self._position_repository.find_single(**kwargs)):
            raise NotFoundError("Position not found")
        return position

    async def get_all(self) -> list[ReadPositionSchema]:
        positions = await self._position_repository.find_all()
        return [ReadPositionSchema(**position.to_dict()) for position in positions]


async def get_position_service() -> AsyncGenerator[PositionService, None]:
    async with db_helper.get_session() as session:
        yield PositionService(session)
