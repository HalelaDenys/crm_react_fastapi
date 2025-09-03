import type { IUser } from "../../entities/user.types";
import { getChangedFields, transformKeysToSnakeCase } from "../../utils/utils";
import { useUpdateUser } from "./useUpdateUser";

// Hook to control the state of the user form and update the user.
export default function useUpdateUserForm(
  userData: IUser | null,
  newUserData: IUser | null,
  setValidationErrors: React.Dispatch<React.SetStateAction<{ [key: string]: string }>>
) {
  const updateUserMutation = useUpdateUser();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const changedFields = getChangedFields(userData!, newUserData!);
    if (Object.keys(changedFields).length === 0) return;

    const data = transformKeysToSnakeCase(changedFields) as Partial<IUser>;
    updateUserMutation.mutate(
      { id: userData!.id, data },
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
    isUpdating: updateUserMutation.isPending,
  };
}
