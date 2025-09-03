import type { IEmployee, IEmployeeCreateFormData, IEmployeeRaw } from "../entities/employee.types";
import { getTokenFromLocalStorage } from "../utils/auth";
import api from "./instanceAPI";
import axios from "axios";

const token = getTokenFromLocalStorage();

export const fetchEmployees = async (
    query?: Record<string, string>
): Promise<IEmployeeRaw[]> => {
  try {
    const response = await api.get("/employees", {
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

export const fetchEmployeeById = async (id: number): Promise<IEmployeeRaw> => {
  try {
    const response = await api.get(`/employees/${id}`, {
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

export const createEmployee = async (
  empData: Partial<IEmployeeCreateFormData>
): Promise<IEmployeeRaw> => {
  try {
    const response = await api.post("/employees", empData, {
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

export const updateEmployee = async (
  id: number,
  empData: Partial<IEmployee>
): Promise<IEmployeeRaw> => {
  try {
    const response = await api.patch(`/employees/${id}`, empData, {
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

export const deleteEmployee = async (id: number): Promise<void> => {
  try {
    await api.delete(`/employees/${id}`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
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
