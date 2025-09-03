import { create } from "zustand";
import type { IFilterValues } from "../entities/filter.types";

interface IEmpFilterValues extends IFilterValues {}

interface IUserFilterStore {
  filters: Record<string, IEmpFilterValues>;
  setEmpFilters: (userId: number, values: Partial<IEmpFilterValues>) => void;
  getEmpFilters: (userId: number) => IEmpFilterValues;
  resetEmpFilters: (userId: number) => void;
}

const defaultFilter: IFilterValues = {
  sortBy: "created_at",
  sortOrder: "desc",
  status: "all",
  search: "",
  dateFrom: "",
  dateTo: "",
};

export const useEmpFilterStore = create<IUserFilterStore>((set, get) => ({
  filters: {},

  setEmpFilters: (userId, values) => {
    const current = get().filters[userId] || defaultFilter;
    set({
      filters: {
        ...get().filters,
        [userId]: {
          ...current,
          ...values,
        },
      },
    });
  },

  getEmpFilters: (userId) => {
    return get().filters[userId] || defaultFilter;
  },

  resetEmpFilters: (userId) => {
    set({
      filters: {
        ...get().filters,
        [userId]: defaultFilter,
      },
    });
  },
}));
