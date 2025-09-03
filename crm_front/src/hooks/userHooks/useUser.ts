import { useQuery } from "@tanstack/react-query";
import type { IUser } from "../../entities/user.types";
import { getUserByIdService } from "../../service/userService";

export const useUser = (id?: number) => {
  return useQuery<IUser> (
    {
      queryKey: ["user", id],
      queryFn: () => {
        if (!id) throw new Error("User id is undefined");
        return getUserByIdService(Number(id));
      },
      enabled: !!id
    }
  )
};
