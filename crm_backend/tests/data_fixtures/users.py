import pytest
from schemas.employee_shemas import LoginSchema
from schemas.user_schema import UserSchema


@pytest.fixture
def admin_login_data() -> LoginSchema:
    return LoginSchema(
        phone_number="+1555555555",
        password="admin_password",
    )


@pytest.fixture
def homer_test_data() -> UserSchema:
    return UserSchema(
        first_name=homer_user["first_name"],
        last_name=homer_user["last_name"],
        phone_number=homer_user["phone_number"],
    )


test_user_1 = {
    "first_name": "test_user_1",
    "last_name": "test_user_1",
}

homer_user = {
    "id": 2,
    "first_name": "Homer",
    "last_name": "Simson",
    "phone_number": "+1 923 021 339",
}
