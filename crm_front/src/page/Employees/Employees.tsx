import EmployeeCreateForm from "../../components/Form/EmployeeCreateForm/EmployeeCreateForm";
import type { EmpQueryParams, IEmployeeCreateFormData } from "../../entities/employee.types";
import { useCreateEmployee } from "../../hooks/empHooks/useCreateEmployee";
import ContentItem from "../../components/ContentItem/ContentItem";
import { useUserFilterStore } from "../../store/userFilter.store";
import { useEmployees } from "../../hooks/empHooks/useEmployees";
import ModalWnd from "../../components/Modals/ModalWnd/ModalWnd";
import CustomFilter from "../../components/Filters/CustomFilter";
import { currentUserId } from "../../utils/auth";
import styles from "../Page.module.css";
import { useState } from "react";
import { transformKeysToSnakeCase } from "../../utils/utils";
import ReloadBtn from "../../components/ReloadBtn/ReloadBtn";

function Employees() {
  const userId = currentUserId();
  const filters = useUserFilterStore((state) => state.getUserFilters(userId));
  const setUserFilters = useUserFilterStore((state) => state.setUserFilters);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const params = transformKeysToSnakeCase(filters) as EmpQueryParams;
  const { data: empData = [], isLoading, error } = useEmployees(params);
  const createEmpMutation= useCreateEmployee();

  

  const handleSubmit = (data: IEmployeeCreateFormData) => {
    createEmpMutation.mutate(data);
    setIsModalOpen(false);
  };
  
  if (isLoading) return "Loading...";

  if (error) return "An error has occurred: " + error.message;

  if (empData.length === 0  && filters.search.length === 0) {
        return (
            <ReloadBtn 
            title="Employees found."/>
        )
  }

  return (
    <div>
    <CustomFilter
      filters={filters}
      setFilters={(values) => setUserFilters(userId, values)}
      sortOptions={[
        { label: "Дата створення", value: "created_at" },
        { label: "Ім'я", value: "first_name" },
        { label: "Прізвище", value: "last_name" },
        { label: "Номер телефону", value: "phone_number" },
        { label: "Посада", value: "position_id" },
      ]}
    />
      <div className="flex justify-center">
        <button className={styles["btn"]} onClick={() => setIsModalOpen(true)}>
          Create new employee
        </button>
      </div>
      <div className="flex flex-col gap-2 mt-1">
        {empData.map((emp) => (
          <ContentItem
            key={emp.id}
            id={emp.id}
            title={emp.firstName + " " + emp.lastName}
            endpoint="employees"
            createdAt={emp.createdAt}
          />
        ))}
      </div>
      <ModalWnd
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Create new employee"
        content={<EmployeeCreateForm  onSubmit={handleSubmit}/>}
      />
    </div>
  );
}

export default Employees;
