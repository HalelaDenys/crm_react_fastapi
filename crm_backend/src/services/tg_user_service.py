from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import AlreadyExistsError, NotFoundError
from infrastructure import TgUserRepository, TgUser, db_helper
from schemas.user_schema import TgUserSchema
from services.base_service import BaseService


class TgUserService(BaseService):
    def __init__(self, session: AsyncSession):
        self._tg_user_repository = TgUserRepository(session)

    async def add(self, data: TgUserSchema) -> TgUser:
        if await self._tg_user_repository.find_single(telegram_id=data.telegram_id):
            raise AlreadyExistsError("User already exists")
        return await self._tg_user_repository.create(data)

    async def update(self, tg_user_id: int, data):
        pass

    async def delete(self, tg_user_id: int) -> None:
        await self.get(id=tg_user_id)
        await self._tg_user_repository.delete(id=tg_user_id)

    async def get(self, **kwargs) -> TgUser:
        if not (user := await self._tg_user_repository.find_single(**kwargs)):
            raise NotFoundError("User not found")
        return user

    async def get_all(self, **kwargs):
        pass


async def get_tg_user_service() -> AsyncGenerator["TgUserService", None]:
    async with db_helper.get_session() as session:
        yield TgUserService(session=session)
