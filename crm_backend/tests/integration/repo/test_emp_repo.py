from infrastructure import EmployeeRepository, Employee
import pytest
from schemas.employee_shemas import CreateEmployeeSchema, UpdateEmployeeSchema


@pytest.mark.asyncio
class TestEmployeeRepository:
    async def test_create_emp(
        self, employee_repo: EmployeeRepository, petro_test_data: CreateEmployeeSchema
    ) -> None:
        emp = await employee_repo.create(data=petro_test_data)

        assert emp is not None
        assert emp.id is not None
        assert emp.email == petro_test_data.email
        assert emp.phone_number == petro_test_data.phone_number

    async def test_get_emp(
        self, employee_repo: EmployeeRepository, emp_ron_data: CreateEmployeeSchema
    ) -> None:
        emp = await employee_repo.find_single(id=2)

        assert emp is not None
        assert emp.id == 2
        assert emp.email == emp_ron_data.email
        assert emp.phone_number == emp_ron_data.phone_number

    async def test_update_emp(
        self, employee_repo: EmployeeRepository, emp_ron_data: CreateEmployeeSchema
    ) -> None:
        new_data = UpdateEmployeeSchema(patronymic="ronison", is_active=False)
        emp = await employee_repo.update(data=new_data, id=2)

        assert emp is not None
        assert emp.id == 2
        assert emp.patronymic != emp_ron_data.patronymic
        assert emp.is_active != True

    async def test_find_all_emp(self, employee_repo: EmployeeRepository) -> None:
        emps = await employee_repo.find_all(
            sort_order="desc",
            sort_by="created_at",
            status="all",
        )

        assert emps is not None
        assert len(emps) > 0
        assert isinstance(emps, list)
        assert isinstance(emps[0], Employee)

    async def test_delete_emp(self, employee_repo: EmployeeRepository) -> None:
        await employee_repo.delete(id=2)
        emp = await employee_repo.find_single(id=2)
        assert emp is None
