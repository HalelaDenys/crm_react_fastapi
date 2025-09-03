import { useMutation, useQueryClient } from "@tanstack/react-query";
import type { UpdateUserInput } from "../../entities/user.types";
import { updateUserService } from "../../service/userService";

export const useUpdateUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: UpdateUserInput) => updateUserService(id, data),
    onSuccess: (_data, vars) => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
      queryClient.invalidateQueries({ queryKey: ["user", vars.id] });
    },
  });
};
