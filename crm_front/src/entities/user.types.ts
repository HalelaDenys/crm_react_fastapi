
export interface IUser {
    id: number;
    firstName: string;
    lastName: string;
    phoneNumber: string;
    isActive: boolean;
    createdAt: string;
}

export interface IUserRaw {
  id: number;
  first_name: string;
  last_name: string;
  phone_number: string;
  is_active: boolean;
  created_at: string;
}

export interface IUserCreateFormData {
    firstName: string;
    lastName: string;
    phoneNumber: string;
}

export interface IUserFormProps {
    onSubmit: (data: IUserCreateFormData) => void
}

export interface UpdateUserInput {
  id: number;
  data: Partial<IUser>;
}

export interface UserQueryParams {
  status: "is_active" | "is_inactive" | "all";
  search?: string;
  date_from?: string;
  date_to?: string;
  sort_by: "created_at" | "first_name" | "last_name";
  sort_order: "asc" | "desc";
}