import { getChangedFields, transformKeysToSnakeCase } from "../../utils/utils";
import { updateEmployeeService } from "../../service/employeeService";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import type {
  IUpdateEmployeeInput,
  IEmployee,
} from "../../entities/employee.types";

// Hook to manage the state and submission of the employee update form.
export default function useUpdateEmployeeForm(
  empData: IEmployee,
  newEmpData: IEmployee,
  setValidationErrors: React.Dispatch<
    React.SetStateAction<{ [key: string]: string }>
  >
) {
  const queryClient = useQueryClient();

  // create mutation
  const updateEmpMutation = useMutation({
    mutationFn: ({ id, data }: IUpdateEmployeeInput) =>
      updateEmployeeService(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["employees"] });
      queryClient.invalidateQueries({ queryKey: ["employee", empData.id] });
    },
  });

  // Processes data forms to update employee information.
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const changerFields = getChangedFields(empData, newEmpData);
    if (Object.keys(changerFields).length === 0) return;

    const data = transformKeysToSnakeCase(changerFields) as Partial<IEmployee>;

    updateEmpMutation.mutate(
      { id: empData.id, data },
      {
        onError: (error: any) => {
          if (error?.response?.data?.detail) {
            const err: { [key: string]: string } = {};
            error.response.data.detail.forEach((e: any) => {
              const field = e.loc[1];
              if (field) {
                err[field] = e.msg;
              }
            });
            setValidationErrors(err);
          }
        },
        onSuccess: () => {
          setValidationErrors({});
        },
      }
    );
  };

  return {
    handleSubmit,
    isUpdating: updateEmpMutation.isPending,
  };
}
