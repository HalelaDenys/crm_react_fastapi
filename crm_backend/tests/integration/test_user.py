import pytest


@pytest.mark.asyncio
class TestUser:
    async def test_register_user(
        self, async_client, db_session, login_admin, homer_test_data
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
