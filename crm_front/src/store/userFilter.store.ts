import { create } from "zustand";
import type { IFilterValues } from "../entities/filter.types";


interface IUserFilterValues extends IFilterValues {};

interface IUserFilterStore {
  filters: Record<string, IUserFilterValues>;
  setUserFilters: (userId: number, values: Partial<IUserFilterValues>) => void;
  getUserFilters: (userId: number) => IUserFilterValues;
  resetUserFilters: (userId: number) => void;
}

const defaultFilter: IFilterValues = {
  sortBy: "created_at",
  sortOrder: "desc",
  status: "all",
  search: "",
  dateFrom: "",
  dateTo: "",
};

export const useUserFilterStore = create<IUserFilterStore>((set, get) => ({
  filters: {},

  setUserFilters: (userId, values) => {
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
  getUserFilters: (userId) => {
    return get().filters[userId] || defaultFilter;
  },

  resetUserFilters: (userId) => {
    set({
      filters: {
        ...get().filters,
        [userId]: defaultFilter,
      },
    });
  },
}));
