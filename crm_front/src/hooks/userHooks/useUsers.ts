import type { IUser, UserQueryParams } from "../../entities/user.types";
import { getUsersService } from "../../service/userService";
import { cleanedFilters } from "../../utils/utils";
import { useQuery } from "@tanstack/react-query";

export const useUsers = (params: UserQueryParams) => {
  const cleaned = cleanedFilters(params);
  return useQuery<IUser[]>({
    queryKey: ["users", cleaned],
    queryFn: () => getUsersService(cleaned),
    placeholderData: (prev) => prev, // залишає попередні дані у кеші під час зміни queryKey
    staleTime: 3600000,
    refetchOnWindowFocus: false, // не робити запит при фокусі вікна
  });
};