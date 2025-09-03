import { deleteEmployeeService } from "../../service/employeeService";
import { useMutation, useQueryClient } from "@tanstack/react-query";


export default function useDeleteEmployee(onSuccessCallback?: () => void) {
  const queryClient = useQueryClient();

  const deleteEmpMutation = useMutation({
    mutationFn: deleteEmployeeService,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["employees"] });
      onSuccessCallback?.();
    },
  });

  const handleDelete = (id: number) => {
    deleteEmpMutation.mutate(id);
  };

  return { handleDelete, isDeleting: deleteEmpMutation.isPending };
}