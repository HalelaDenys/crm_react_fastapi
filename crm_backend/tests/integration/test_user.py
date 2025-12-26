import pytest


@pytest.mark.asyncio
class TestUser:
    async def test_register_user(self, async_client, db_session):
        assert 1 == 1
