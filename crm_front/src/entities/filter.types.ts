
export type FilterType = "status" | "date" | "sortBy" | "sortOrder";

export interface IFilterValues {
  search: string;
  sortBy: "created_at" | "first_name" | "last_name";
  sortOrder: "asc" | "desc";
  status: "is_active" | "is_inactive" | "all";
  dateFrom: string;
  dateTo: string;
}