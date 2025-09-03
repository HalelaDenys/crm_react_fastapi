import { useEffect, useState } from "react";
import { useUser } from "./useUser";
import type { IUser } from "../../entities/user.types";


// Hook to control the state of the user form.
export default function useUserForm(userId: number) {
  const { data: userData, isLoading, error } = useUser(userId);
  const [userForm, setUserForm] = useState<IUser | null>(null);
  const [validationErrors, setValidationErrors] = useState<{
    [key: string]: string;
  }>({});

  useEffect(() => {
    if (userData !== undefined) {
      setUserForm(userData);
    }
  }, [userData]);

  return {
    isLoading,
    error,
    userData,
    userForm,
    setUserForm,
    validationErrors,
    setValidationErrors,
  };
}
