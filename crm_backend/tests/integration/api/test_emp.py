from sqlalchemy.ext.asyncio import AsyncSession
from schemas.employee_shemas import CreateEmployeeSchema, TokenInfo
from infrastructure import Employee
from httpx import AsyncClient
from sqlalchemy import select
import pytest
from tests.data_fixtures.emps import test_emp_1, petro_user


@pytest.mark.asyncio
class TestEmployee:

    async def test_create_emp(
        self,
        async_client: AsyncClient,
        login_admin: TokenInfo,
        petro_test_data: CreateEmployeeSchema,
    ):
        response = await async_client.post(
            "/employees",
            json=petro_test_data.model_dump(),
            headers={"Authorization": f"Bearer {login_admin.access_token}"},
        )
        assert response.status_code == 201
        data = response.json()

        assert data["first_name"] == petro_test_data.first_name
        assert data["phone_number"] == petro_test_data.phone_number
        assert "id" in data

    @pytest.mark.parametrize(
        "data, expected_status, use_auth",
        [
            (test_emp_1, 422, True),
            (test_emp_1, 401, False),
            (petro_user, 409, True),
        ],
    )
    async def test_failed_emp_creation(
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
            "/employees",
            json=data,
            headers=headers,
        )

        data = response.json()

        assert response.status_code == expected_status
        assert len(data) != 0

    @pytest.mark.parametrize(
        "user_id, expected_status, use_auth",
        [
            (2, 200, True),
            (1, 401, False),
            (99, 404, True),
        ],
    )
    async def test_get_emp(
        self,
        async_client: AsyncClient,
        login_admin: TokenInfo,
        user_id: int,
        expected_status: str,
        use_auth: bool,
    ):
        headers = {}
        if use_auth:
            headers["Authorization"] = f"Bearer {login_admin.access_token}"

        response = await async_client.get(
            f"/employees/{user_id}",
            headers=headers,
        )
        assert response.status_code == expected_status

    async def test_update_emp(
        self,
        async_client: AsyncClient,
        login_admin: TokenInfo,
    ):
        response = await async_client.patch(
            f"/employees/{petro_user.get('id')}",
            json={"position_id": 1, "is_admin": True},
            headers={"Authorization": f"Bearer {login_admin.access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["position_id"] == 1
        assert data["is_admin"] == True

    async def test_get_all_emp(
        self,
        async_client: AsyncClient,
        login_admin: TokenInfo,
    ):
        response = await async_client.get(
            "/employees",
            headers={"Authorization": f"Bearer {login_admin.access_token}"},
        )
        assert response.status_code == 200

        data = response.json()

        assert len(data) != 0
        assert isinstance(data, list)

    async def test_delete_emp(
        self,
        async_client: AsyncClient,
        login_admin: TokenInfo,
    ):
        response = await async_client.delete(
            f"/employees/{petro_user.get('id')}",
            headers={"Authorization": f"Bearer {login_admin.access_token}"},
        )
        assert response.status_code == 204
