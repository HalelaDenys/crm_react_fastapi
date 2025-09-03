from services.employee_service import get_employee_service, EmployeeService
from core.authentication import get_auth_user_from_token_of_type
from schemas.employee_shemas import LoginSchema
from fastapi import Depends, Form
from infrastructure import Employee
from typing import Annotated
from core import (
    FORBIDDEN_EXC_NOT_ENOUGH_RIGHTS,
    UNAUTHORIZED_EXC_INCORRECT,
    FORBIDDEN_EXC_INACTIVE,
    ACCESS_TOKEN,
    REFRESH_TOKEN,
    Security,
)


async def authenticate_user(
    employee_data: Annotated[LoginSchema, Form()],
    employee_service: Annotated["EmployeeService", Depends(get_employee_service)],
) -> Employee:
    if not (
        employee := await employee_service.get(phone_number=employee_data.phone_number)
    ):
        raise UNAUTHORIZED_EXC_INCORRECT

    if not Security.verify_password(
        password=employee_data.password,
        hashed_password=str(employee.password),
    ):
        raise UNAUTHORIZED_EXC_INCORRECT

    if not employee.is_active:
        raise FORBIDDEN_EXC_INACTIVE

    return employee


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN)
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN)


def check_user_is_active(
    employee: Annotated[Employee, Depends(get_current_auth_user)],
) -> bool:
    if not employee.is_active:
        raise FORBIDDEN_EXC_INACTIVE
    return True


def check_user_is_admin(
    employee: Annotated[Employee, Depends(get_current_auth_user)],
) -> bool:
    if not employee.is_admin:
        raise FORBIDDEN_EXC_NOT_ENOUGH_RIGHTS
    return True
