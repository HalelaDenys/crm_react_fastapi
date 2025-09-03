import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createEmployeeService } from "../../service/employeeService";


export const useCreateEmployee = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createEmployeeService,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["employees"] });
    },
  });
};