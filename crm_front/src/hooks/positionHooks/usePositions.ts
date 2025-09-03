import { useQuery } from "@tanstack/react-query";
import type { IPosition } from "../../entities/position.types"
import { getPositionsService } from "../../service/positionService";


export const usePositions = () => {
    return useQuery<IPosition[]>({
        queryKey: ["positions"],
        queryFn: () => getPositionsService(),
        staleTime: 3600000,
        refetchOnWindowFocus: false,
    })
}