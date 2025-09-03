from services.employee_service import get_employee_service, EmployeeService
from core.dependencies.authorization import check_user_is_admin
from core.authentication import http_bearer
from fastapi import APIRouter, Depends, status, Path, Query
from schemas.employee_shemas import (
    ReadEmployeeSchemaWithPosition,
    EmpFilterParamsSchema,
    CreateEmployeeSchema,
    UpdateEmployeeSchema,
    ReadEmployeeSchema,
)
from typing import Annotated
from core import settings

router = APIRouter(
    prefix=settings.api_prefix.employees,
    tags=["Employees"],
    dependencies=[Depends(http_bearer)],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee_data: CreateEmployeeSchema,
    employee_service: Annotated["EmployeeService", Depends(get_employee_service)],
    is_admin: Annotated[bool, Depends(check_user_is_admin)],
) -> ReadEmployeeSchema:
    employee = await employee_service.add(data=employee_data)
    return ReadEmployeeSchema(**employee.to_dict())


@router.get("/{employee_id}", status_code=status.HTTP_200_OK)
async def get_employee_by_id(
    employee_id: Annotated[int, Path(ge=1)],
    employee_service: Annotated["EmployeeService", Depends(get_employee_service)],
    is_admin: Annotated[bool, Depends(check_user_is_admin)],
) -> ReadEmployeeSchemaWithPosition:
    emp = await employee_service.get_by_employee_id(employee_id=employee_id)
    return emp


@router.get("", status_code=status.HTTP_200_OK)
async def get_employees(
    employee_service: Annotated["EmployeeService", Depends(get_employee_service)],
    is_admin: Annotated[bool, Depends(check_user_is_admin)],
    filter_params: Annotated[EmpFilterParamsSchema, Query()],
) -> list[ReadEmployeeSchema]:
    return await employee_service.get_all(filter_params=filter_params)


@router.patch("/{employee_id}", status_code=status.HTTP_200_OK)
async def update_employee(
    employee_id: Annotated[int, Path(ge=1)],
    employee_data: UpdateEmployeeSchema,
    employee_service: Annotated["EmployeeService", Depends(get_employee_service)],
    is_admin: Annotated[bool, Depends(check_user_is_admin)],
) -> ReadEmployeeSchema:
    employee = await employee_service.update(
        employee_id=employee_id, data=employee_data
    )
    return ReadEmployeeSchema(**employee.to_dict())


@router.delete("/{employee_id}", status_code=status.HTTP_200_OK)
async def delete_employee(
    employee_id: Annotated[int, Path(ge=1)],
    employee_service: Annotated["EmployeeService", Depends(get_employee_service)],
    is_admin: Annotated[bool, Depends(check_user_is_admin)],
):
    await employee_service.delete(employee_id=employee_id)
    return
