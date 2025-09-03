from infrastructure import Employee, db_helper, EmployeeRepository
from core.exceptions import NotFoundError, AlreadyExistsError
from schemas.employee_shemas import (
    ReadEmployeeSchemaWithPosition,
    employee_to_read_schema,
    EmpFilterParamsSchema,
    CreateEmployeeSchema,
    UpdateEmployeeSchema,
    ReadEmployeeSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession
from services.base_service import BaseService
from typing import AsyncGenerator
from core import Security


class EmployeeService(BaseService):
    def __init__(self, session: AsyncSession):
        self._employee_repository = EmployeeRepository(session)

    async def add(self, data: CreateEmployeeSchema) -> Employee:
        if await self._employee_repository.find_single(phone_number=data.phone_number):
            raise AlreadyExistsError("Employee already exists")
        data.password = Security.hash_password(data.password)
        return await self._employee_repository.create(data)

    async def update(self, employee_id: int, data: UpdateEmployeeSchema) -> Employee:
        await self.get(id=employee_id)
        return await self._employee_repository.update(id=employee_id, data=data)

    async def delete(self, employee_id: int):
        await self.get(id=employee_id)
        await self._employee_repository.delete(id=employee_id)

    async def get(self, **kwargs) -> Employee:
        if not (employee := await self._employee_repository.find_single(**kwargs)):
            raise NotFoundError("Employee not found")
        return employee

    async def get_all(
        self, filter_params: EmpFilterParamsSchema
    ) -> list[ReadEmployeeSchema]:
        employees = await self._employee_repository.find_all(
            sort_by=filter_params.sort_by,
            sort_order=filter_params.sort_order,
            status=filter_params.status,
            search=filter_params.search,
            date_from=filter_params.date_from,
            date_to=filter_params.date_to,
        )
        return [ReadEmployeeSchema(**employee.to_dict()) for employee in employees]

    async def get_by_employee_id(
        self, employee_id: int
    ) -> ReadEmployeeSchemaWithPosition:
        employee = await self.get(id=employee_id)
        return employee_to_read_schema(employee)


async def get_employee_service() -> AsyncGenerator[EmployeeService, None]:
    async with db_helper.get_session() as session:
        yield EmployeeService(session)
