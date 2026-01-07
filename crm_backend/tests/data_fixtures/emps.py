import pytest

from infrastructure.db.models import employee
from schemas.employee_shemas import CreateEmployeeSchema


@pytest.fixture
def petro_test_data() -> CreateEmployeeSchema:
    return CreateEmployeeSchema(
        first_name=petro_user["first_name"],
        last_name=petro_user["last_name"],
        phone_number=petro_user["phone_number"],
        email=petro_user["email"],
        position_id=petro_user["position_id"],
        is_admin=petro_user["is_admin"],
        password=petro_user["password"],
    )


@pytest.fixture
async def emp_ron_data() -> CreateEmployeeSchema:
    return CreateEmployeeSchema(
        first_name=ron_emp["first_name"],
        last_name=ron_emp["last_name"],
        phone_number=ron_emp["phone_number"],
        email=ron_emp["email"],
        position_id=ron_emp["position_id"],
        is_admin=False,
        password=ron_emp["password"],
    )


petro_user = {
    "id": 2,
    "first_name": "Petro",
    "last_name": "Zara",
    "phone_number": "+1 821 343 001",
    "patronymic": "petrovich",
    "email": "petro13@example.com",
    "position_id": 2,
    "is_active": True,
    "is_admin": False,
    "password": "petro_password",
}


test_emp_1 = {
    "first_name": "test_emp_1",
    "last_name": "test_emp_1",
    "patronymic": "test_emp_1",
    "position_id": 2,
    "is_active": True,
    "is_admin": False,
    "password": "test_password",
}

ron_emp = {
    "first_name": "Roni",
    "last_name": "Ronin",
    "phone_number": "+1 231 004 199",
    "email": "ron11@example.com",
    "position_id": 2,
    "is_active": True,
    "is_admin": False,
    "password": "ron_0012dsa",
}
