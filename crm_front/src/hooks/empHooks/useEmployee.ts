import type { IEmployee, IEmployeeWithPosition } from "../../entities/employee.types";
import { getEmployeeByIdService } from "../../service/employeeService";
import { useQuery } from "@tanstack/react-query";


export const useEmployee = (id?: number) => {
    return useQuery<IEmployeeWithPosition> (
        {
            queryKey: ["employee", id],
            queryFn: () => {
                if (!id) throw new Error("User id is undefined");
                return getEmployeeByIdService(Number(id));
            },
            enabled: !!id
        }
    )
}