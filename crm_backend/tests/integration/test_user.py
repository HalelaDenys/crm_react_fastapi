from tests.data_fixtures.users import test_user_1, homer_user
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.employee_shemas import TokenInfo
from schemas.user_schema import UserSchema
from infrastructure import User
from httpx import AsyncClient
from sqlalchemy import select
import pytest


@pytest.mark.asyncio
class TestUser:
    async def test_create_user(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        login_admin: TokenInfo,
        homer_test_data: UserSchema,
    ):
        response = await async_client.post(
            "/users",
            json=homer_test_data.model_dump(),
            headers={"Authorization": f"Bearer {login_admin.access_token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["first_name"] == homer_test_data.first_name
        assert data["last_name"] == homer_test_data.last_name
        assert data["phone_number"] == homer_test_data.phone_number

        stmt = select(User).where(User.id == data["id"])
        result = await db_session.execute(stmt)
        user = result.scalar_one_or_none()

        assert user is not None

    @pytest.mark.parametrize(
        "data, expected_status, use_auth",
        [
            (test_user_1, 422, True),
            (test_user_1, 401, False),
            (homer_user, 409, True),
        ],
    )
    async def test_failed_user_creation(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        login_admin: TokenInfo,
        data: dict,
        expected_status: int,
        use_auth: bool,
    ):
        headers = {}
        if use_auth:
            headers["Authorization"] = f"Bearer {login_admin.access_token}"

        response = await async_client.post(
            "/users",
            json=data,
            headers=headers,
        )

        data = response.json()

        assert response.status_code == expected_status
        assert len(data) != 0

    @pytest.mark.parametrize(
        "user_id, expected_status, use_auth, exists",
        [
            (2, 200, True, True),
            (1, 401, False, True),
            (3, 404, True, False),
            (0, 422, True, False),
        ],
    )
    async def test_get_user(
        self,
        async_client: AsyncClient,
        login_admin: TokenInfo,
        db_session: AsyncSession,
        user_id: int,
        expected_status: int,
        use_auth: bool,
        exists: bool,
    ):
        headers = {}
        if use_auth:
            headers["Authorization"] = f"Bearer {login_admin.access_token}"

        response = await async_client.get(
            f"/users/{user_id}",
            headers=headers,
        )

        assert response.status_code == expected_status

        stmt = select(User).where(User.id == user_id)
        result = await db_session.execute(stmt)
        user = result.scalar_one_or_none()

        if exists:
            assert user is not None
        else:
            assert user is None

        if expected_status == 200:
            data = response.json()
            assert data["id"] == user.id

    @pytest.mark.parametrize(
        "user_id, expected_status, update_data, exists",
        [
            (homer_user.get("id", 2), 200, {"is_active": False}, True),
            (99, 404, {"is_active": True}, False),
        ],
    )
    async def test_update_user(
        self,
        async_client: AsyncClient,
        login_admin: TokenInfo,
        db_session: AsyncSession,
        user_id: int,
        update_data: dict,
        expected_status: int,
        exists: bool,
    ):

        response = await async_client.patch(
            f"/users/{user_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {login_admin.access_token}"},
        )

        assert response.status_code == expected_status

        stmt = select(User).where(User.id == user_id)
        result = await db_session.execute(stmt)
        user = result.scalar_one_or_none()

        if exists:
            assert user is not None
            assert user_id == user.id
            for k, v in update_data.items():
                assert getattr(user, k) == v
        else:
            assert user is None

    async def test_get_all_users(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        login_admin: TokenInfo,
    ):
        response = await async_client.get(
            "/users",
            params={"sort_order": "asc"},
            headers={"Authorization": f"Bearer {login_admin.access_token}"},
        )

        data = response.json()
        assert response.status_code == 200
        assert len(data) != 0
        assert isinstance(data, list)

        assert data[0]["id"] == 1
        assert data[0]["first_name"] == "liza"
        assert data[0]["last_name"] == "simson"

    async def test_delete_user(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        login_admin: TokenInfo,
    ):
        response = await async_client.delete(
            f"/users/1",
            headers={"Authorization": f"Bearer {login_admin.access_token}"},
        )

        assert response.status_code == 204
        stmt = select(User).where(User.id == 1)
        result = await db_session.execute(stmt)
        user = result.scalar_one_or_none()
        assert user is None
