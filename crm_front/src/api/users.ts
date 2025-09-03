import { getTokenFromLocalStorage } from "../utils/auth";
import type {
  IUser,
  IUserCreateFormData,
  IUserRaw,
} from "../entities/user.types";
import api from "./instanceAPI";
import axios from "axios";

const token = getTokenFromLocalStorage();

export const fetchUsers = async (
  query?: Record<string, string>
): Promise<IUserRaw[]> => {
  try {
    const response = await api.get("/users", {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      params: query ,
    });

    return response.data;
  } catch (error: any) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw error;
    }
    throw {
      type: "unknown_error",
      error,
    };
  }
};

export const fetchUsersById = async (id: number): Promise<IUserRaw> => {
  try {
    const response = await api.get(`/users/${id}`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error: any) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw error;
    }
    throw {
      type: "unknown_error",
      error,
    };
  }
};

export const updateUser = async (
  id: number,
  userData: Partial<IUser>
): Promise<IUserRaw> => {
  try {
    const response = await api.patch(`/users/${id}`, userData, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error: any) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw error;
    }
    throw {
      type: "unknown_error",
      error,
    };
  }
};

export const deleteUser = async (id: number): Promise<void> => {
  try {
    await api.delete(`/users/${id}`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    return;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw error;
    }
    throw {
      type: "unknown_error",
      error,
    };
  }
};

export const createUser = async (
  userData: IUserCreateFormData
): Promise<IUserRaw> => {
  const data = {
    first_name: userData.firstName,
    last_name: userData.lastName,
    phone_number: userData.phoneNumber,
  };
  try {
    const response = await api.post(`/users`, data, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data?.detail) {
      throw error;
    }
    throw {
      type: "unknown_error",
      error,
    };
  }
};
