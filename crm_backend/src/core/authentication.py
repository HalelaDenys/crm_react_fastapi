from services.employee_service import EmployeeService, get_employee_service
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core import Security, UNAUTHORIZED_EXC_INVALID_TOKEN
from fastapi import Depends, HTTPException
from infrastructure import Employee
from typing import Annotated
from jose import JWTError


http_bearer = HTTPBearer(auto_error=False)


def get_current_token_payload(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> dict:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = credentials.credentials
    try:
        payload = Security.decode_token(
            token=token,
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return payload


def validate_token(payload: dict, token_type: str) -> bool | Exception:
    current_token_type = payload.get("type")
    if current_token_type == token_type:
        return True
    return HTTPException(
        status_code=401,
        detail=f"Invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub(
    payload: dict,
    employee_service: "EmployeeService",
):
    sub: str | None = payload.get("sub")
    if user := await employee_service.get(id=int(sub)):
        return user
    raise UNAUTHORIZED_EXC_INVALID_TOKEN


def get_auth_user_from_token_of_type(token_type: str):

    async def get_auth_user_from_token(
        employee_service: Annotated["EmployeeService", Depends(get_employee_service)],
        payload: dict = Depends(get_current_token_payload),
    ) -> "Employee":
        validate_token(payload, token_type)
        return await get_user_by_token_sub(payload, employee_service)

    return get_auth_user_from_token
