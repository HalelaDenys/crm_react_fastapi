import pytest
from schemas.user_schema import TgUserSchema
from infrastructure import TgUserRepository
import asyncio


@pytest.mark.asyncio
class TestTgUserBroker:

    async def test_create_tg_user(
        self, test_broker, tg_user_repo: TgUserRepository, tg_secret_key: dict
    ):
        user_data = TgUserSchema(
            telegram_id=1234567,
            first_name="Test",
            last_name="User",
            username="test_user",
        )

        await test_broker.publish(
            user_data.model_dump(),
            queue="tg_users.created",
            headers=tg_secret_key,
        )
        # Чекаємо поки повідомлення обробиться
        await asyncio.sleep(1.5)

        user = await tg_user_repo.find_single(telegram_id=1234567)

        assert user is not None
        assert user.telegram_id == 1234567
