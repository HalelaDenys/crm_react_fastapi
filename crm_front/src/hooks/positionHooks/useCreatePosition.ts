import { createPositionService } from "../../service/positionService";
import { useMutation, useQueryClient } from "@tanstack/react-query";

export const useCreatePosition = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createPositionService,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["positions"] });
    },
  });
};
