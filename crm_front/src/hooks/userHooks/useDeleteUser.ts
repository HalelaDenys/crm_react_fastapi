import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deleteUserService } from "../../service/userService";

export const useDeleteUser = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: deleteUserService,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["users"] });
        },
    })
};