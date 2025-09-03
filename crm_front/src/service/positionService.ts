import { transformKeysToCamelCase } from "../utils/utils";
import type { IPosition, IPositionCreateData } from "../entities/position.types"
import { createPosition, deletePosition, fetchPositions } from "../api/positions";


export const getPositionsService = async (): Promise<IPosition[]> => {
    const positions = await fetchPositions();
    return positions.map(transformKeysToCamelCase) as IPosition[];
}


export const createPositionService = async (data: IPositionCreateData): Promise<IPosition> => {
    const position = await createPosition(data);
    return transformKeysToCamelCase(position) as IPosition
}

export const deletePositionService = async (id: number): Promise<void> => {
    await deletePosition(id);
}