from typing import TypeVar, Generic, Type, Union, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from pydantic import BaseModel

from infrastructure import Base


ModelType = TypeVar("ModelType", bound=Base)


class SQLAlchemyRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self._model = model
        self._session = session

    async def create(self, data: BaseModel) -> ModelType:
        obj = self._model(**data.model_dump())
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def update(self, data: BaseModel, **filters) -> Union[ModelType, None]:
        stmt = (
            update(self._model)
            .where(
                *[getattr(self._model, key) == value for key, value in filters.items()]
            )
            .values(**data.model_dump(exclude_unset=True))
            .returning(self._model.id)
        )

        res = await self._session.execute(stmt)
        await self._session.flush()
        updated_id = res.scalar_one_or_none()

        if updated_id is None:
            return None

        return await self.find_single(id=updated_id)

    async def find_single(self, **filters) -> Union[ModelType, None]:
        res = await self._session.execute(select(self._model).filter_by(**filters))
        return res.scalar_one_or_none()

    async def delete(self, **filters) -> None:
        await self._session.execute(delete(self._model).filter_by(**filters))
        await self._session.flush()

    async def find_all(self, **kwargs) -> Sequence[ModelType]:
        res = await self._session.execute(
            select(self._model).filter_by(**kwargs).order_by(self._model.id)
        )
        return res.scalars().all()
