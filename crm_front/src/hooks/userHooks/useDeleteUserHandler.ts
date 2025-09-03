import { useDeleteUser } from "./useDeleteUser";

// Hook to delete a user and handle the loading state.
export default function useDeleteUserHandler(onSuccessCallback: () => void) {
  const deleteUserMutation = useDeleteUser();

  const handleDelete = (id: number) => {
    deleteUserMutation.mutate(id, {
      onSuccess: onSuccessCallback,
    });
  };

  return { handleDelete, isDeleting: deleteUserMutation.isPending };
}
