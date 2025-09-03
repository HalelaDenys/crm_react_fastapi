from schemas.user_schema import (
    UserSchema,
    UpdateUserSchema,
    ReadUserSchema,
    FilterParamsSchema,
)
from core.exceptions import NotFoundError, AlreadyExistsError
from infrastructure import UserRepository, User, db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from services.base_service import BaseService
from typing import AsyncGenerator


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        self._user_repository = UserRepository(session)

    async def add(self, data: UserSchema) -> User:
        await self.check_phone_number(phone_number=data.phone_number)
        return await self._user_repository.create(data)

    async def update(self, user_id: int, data: UpdateUserSchema) -> User:
        await self.check_phone_number(phone_number=data.phone_number)
        await self.get(id=user_id)
        return await self._user_repository.update(id=user_id, data=data)

    async def delete(self, user_id: int) -> None:
        await self.get(id=user_id)
        await self._user_repository.delete(id=user_id)

    async def get(self, **kwargs) -> User:
        if not (user := await self._user_repository.find_single(**kwargs)):
            raise NotFoundError("User not found")
        return user

    async def get_all(self, filter_params: FilterParamsSchema) -> list[ReadUserSchema]:
        users = await self._user_repository.find_all(
            sort_by=filter_params.sort_by,
            sort_order=filter_params.sort_order,
            status=filter_params.status,
            search=filter_params.search,
            date_from=filter_params.date_from,
            date_to=filter_params.date_to,
        )
        return [ReadUserSchema(**user.to_dict()) for user in users]

    async def check_phone_number(self, phone_number: str) -> None:
        if await self._user_repository.find_single(phone_number=phone_number):
            raise AlreadyExistsError("User already exists")


async def get_user_service() -> AsyncGenerator[UserService, None]:
    async with db_helper.get_session() as session:
        yield UserService(session=session)
