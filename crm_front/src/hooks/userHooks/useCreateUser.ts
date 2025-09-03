import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createUserService } from "../../service/userService";

export const useCreateUser = () => {
    const queryClient = useQueryClient();

    return useMutation({
    mutationFn: createUserService,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
};