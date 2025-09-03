export interface IPosition {
    id: number
    name: string
    createdAt: string;
}

export interface IPositionRaw {
    id: number
    name: string
    created_at: string;
}


export interface IPositionCreateData {
    name: string
}
export interface IPositionFormProps {
    onSubmit: (data: IPositionCreateData) => void
}