export interface IEmployee {
    id: number;
    firstName: string;
    lastName: string;
    patronymic: string | null;
    email: string | null;
    phoneNumber: string
    positionId: number;
    isActive: boolean;
    isAdmin: boolean;
    createdAt: string;
}

export interface IEmployeeRaw {
    id: number;
    first_name: string;
    last_name: string;
    phone_number: string;
    patronymic: string | null;
    email: string | null;
    position_id: number;
    is_admin: boolean;
    is_active: boolean;
    created_at: string;
}


export interface IEmployeeWithPosition {
    id: number;
    firstName: string;
    lastName: string;
    patronymic: string | null;
    email: string | null;
    phoneNumber: string
    positionId: number;
    position: string;
    isActive: boolean;
    isAdmin: boolean;
    createdAt: string;
}

export interface IEmployeeCreateFormData {
    firstName: string;
    lastName: string;
    patronymic: string | null;
    phoneNumber: string;
    email: string | null;
    positionId: number;
    password: string;
    isAdmin: boolean;
}

export interface IEmployeeFormProps {
    onSubmit: (data: IEmployeeCreateFormData) => void
}


export interface IUpdateEmployeeInput {
    id: number;
    data: Partial<IEmployee>;
}

export interface EmpQueryParams {
  status: "is_active" | "is_inactive" | "all";
  search?: string;
  date_from?: string;
  date_to?: string;
  sort_by: "created_at" | "first_name" | "last_name" | "phone_number" | "position";
  sort_order: "asc" | "desc";
}