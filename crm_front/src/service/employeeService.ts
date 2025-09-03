import type { IEmployee, IEmployeeWithPosition, IEmployeeCreateFormData } from "../entities/employee.types";
import { cleanedFilters, transformKeysToCamelCase, transformKeysToSnakeCase } from "../utils/utils";
import {
  fetchEmployees,
  fetchEmployeeById,
  updateEmployee,
  deleteEmployee,
  createEmployee,
} from "../api/employees";

export const getEmployeesService = async (
    query: Record<string, string>
): Promise<IEmployee[]> => {
  const employees = await fetchEmployees(query);
  return employees.map(transformKeysToCamelCase) as IEmployee[];
};

export const getEmployeeByIdService = async (
  id: number
): Promise<IEmployeeWithPosition> => {
  const employee = await fetchEmployeeById(id);
  return transformKeysToCamelCase(employee) as IEmployeeWithPosition;
};

export const updateEmployeeService = async (
  id: number,
  empData: Partial<IEmployee>
) => {
  const employee = await updateEmployee(id, empData);
  return transformKeysToCamelCase(employee) as IEmployee;
};

export const createEmployeeService = async (empData: IEmployeeCreateFormData) => {
  const data = transformKeysToSnakeCase(cleanedFilters(empData)) as Partial<IEmployeeCreateFormData>;
  const employee = await createEmployee(data);
  return transformKeysToCamelCase(employee) as IEmployee;
};

export const deleteEmployeeService = async (id: number) => {
  await deleteEmployee(id);
};
