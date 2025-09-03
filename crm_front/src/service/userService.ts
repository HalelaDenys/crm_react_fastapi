import {
  fetchUsers,
  fetchUsersById,
  updateUser,
  deleteUser,
  createUser,
} from "../api/users";
import type { IUser, IUserCreateFormData } from "../entities/user.types";
import {transformKeysToCamelCase } from "../utils/utils";

export const getUsersService = async (
    query: Record<string, string>
): Promise<IUser[]> => {
  const users = await fetchUsers(query);
  return users.map(transformKeysToCamelCase) as IUser[];
};

export const getUserByIdService = async (id: number): Promise<IUser> => {
  const user = await fetchUsersById(id);
  return transformKeysToCamelCase(user) as IUser;
};

export const updateUserService = async (
  id: number,
  userDate: Partial<IUser>
): Promise<IUser> => {
  const user = await updateUser(id, userDate);
  return transformKeysToCamelCase(user) as IUser;
};

export const deleteUserService = async (id: number): Promise<void> => {
  await deleteUser(id);
};

export const createUserService = async (
  data: IUserCreateFormData
): Promise<IUser> => {
  const user = await createUser(data);
  return transformKeysToCamelCase(user) as IUser;
};
