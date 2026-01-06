from tests.data_fixtures.users import test_user_1, homer_user
from schemas.employee_shemas import TokenInfo
from schemas.employee_shemas import CreateEmployeeSchema
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
class TestUser:
    async def test_create_user(
        self,
        async_client: AsyncClient,
        login_admin: TokenInfo,
        homer_test_data: CreateEmployeeSchema,
    ):
        response = await async_client.post(
            "/users",
            json=homer_test_data.model_dump(),
            headers={"Authorization": f"Bearer {login_admin.access_token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["phone_number"] == homer_test_data.phone_number
        assert "id" in data

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
        "user_id, expected_status, use_auth,",
        [
            (2, 200, True),
            (1, 401, False),
            (3, 404, True),
            (0, 422, True),
        ],
    )
    async def test_get_user(
        self,
        async_client: AsyncClient,
        login_admin: TokenInfo,
        user_id: int,
        expected_status: int,
        use_auth: bool,
    ):
        headers = {}
        if use_auth:
            headers["Authorization"] = f"Bearer {login_admin.access_token}"

        response = await async_client.get(
            f"/users/{user_id}",
            headers=headers,
        )

        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_id, expected_status, update_data",
        [
            (homer_user.get("id", 2), 200, {"is_active": False}),
            (99, 404, {"is_active": True}),
        ],
    )
    async def test_update_user(
        self,
        async_client: AsyncClient,
        login_admin: TokenInfo,
        user_id: int,
        update_data: dict,
        expected_status: int,
    ):

        response = await async_client.patch(
            f"/users/{user_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {login_admin.access_token}"},
        )

        assert response.status_code == expected_status

    async def test_get_all_users(
        self,
        async_client: AsyncClient,
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

    async def test_delete_user(
        self,
        async_client: AsyncClient,
        login_admin: TokenInfo,
    ):
        response = await async_client.delete(
            f"/users/1",
            headers={"Authorization": f"Bearer {login_admin.access_token}"},
        )

        assert response.status_code == 204
