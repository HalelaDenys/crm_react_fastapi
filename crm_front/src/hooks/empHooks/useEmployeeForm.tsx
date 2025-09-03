import { useEffect, useState } from "react";
import { useEmployee } from "./useEmployee";
import type { IEmployeeWithPosition } from "../../entities/employee.types";

export default function useEmployeeForm(empId: number) {
  const { data: empData, isLoading, error } = useEmployee(empId);
  const [empForm, setEmpForm] = useState<IEmployeeWithPosition | null>(null);
  const [validationErrors, setValidationErrors] = useState<{
    [key: string]: string;
  }>({});

  useEffect(() => {
    if (empData !== undefined) {
      setEmpForm(empData);
    }
  }, [empData]);

  return {
    isLoading,
    error,
    empData,
    empForm,
    setEmpForm,
    validationErrors,
    setValidationErrors,
  };
}
