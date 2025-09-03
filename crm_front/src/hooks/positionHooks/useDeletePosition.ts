import { deletePositionService } from "../../service/positionService";
import { useMutation, useQueryClient } from "@tanstack/react-query";

export default function useDeletePosition() {
  const queryClient = useQueryClient();

  const deletePosMutation = useMutation({
    mutationFn: deletePositionService,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["positions"] });
    },
  });

  const handleDelete = (id: number) => {
    deletePosMutation.mutate(id);
  };

  return { handleDelete, isDeleting: deletePosMutation.isPending };
}
