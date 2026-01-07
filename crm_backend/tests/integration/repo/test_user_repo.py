import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure import UserRepository, User
from schemas.user_schema import UserSchema, UpdateUserSchema


@pytest.mark.asyncio
class TestUserRepository:

    async def test_create_user(
        self,
        user_repo: UserRepository,
        homer_test_data: UserSchema,
    ) -> None:
        user = await user_repo.create(data=homer_test_data)

        assert user is not None
        assert user.id is not None
        assert user.phone_number == homer_test_data.phone_number

    async def test_get_user(
        self,
        user_repo: UserRepository,
        liza_test_data: UserSchema,
    ) -> None:
        user = await user_repo.find_single(id=1)

        assert user is not None
        assert user.id == 1
        assert user.phone_number == liza_test_data.phone_number

    async def test_update_user(
        self, user_repo: UserRepository, liza_test_data: UserSchema
    ) -> None:
        new_data = UpdateUserSchema(phone_number="+48032105401")
        user = await user_repo.update(data=new_data, id=1)

        assert user is not None
        assert user.phone_number != liza_test_data.phone_number

    async def test_find_all_users(self, user_repo: UserRepository) -> None:
        users = await user_repo.find_all(
            sort_order="desc",
            sort_by="created_at",
            status="all",
        )
        assert users is not None
        assert len(users) > 0
        assert isinstance(users, list)
        assert isinstance(users[0], User)

    async def test_delete_user(self, user_repo: UserRepository) -> None:
        await user_repo.delete(id=1)
        user = await user_repo.find_single(id=1)
        assert user is None
