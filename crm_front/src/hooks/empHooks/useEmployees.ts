import type { EmpQueryParams, IEmployee } from "../../entities/employee.types";
import { getEmployeesService } from "../../service/employeeService";
import { useQuery } from "@tanstack/react-query";
import { cleanedFilters } from "../../utils/utils";

export const useEmployees = (params: EmpQueryParams) => {
  const cleaned_params = cleanedFilters(params);
  return useQuery<IEmployee[]>({
    queryKey: ["employees", cleaned_params],
    queryFn: () => getEmployeesService(cleaned_params),
    placeholderData: (prev) => prev,
    staleTime: 3600000, // 1 hour
    refetchOnWindowFocus: false, // не робити запит при фокусі вікна
  });
};