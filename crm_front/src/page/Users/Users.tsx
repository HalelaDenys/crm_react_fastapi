import type { IUserCreateFormData, UserQueryParams } from "../../entities/user.types";
import { useCreateUser } from "../../hooks/userHooks/useCreateUser";
import ContentItem from "../../components/ContentItem/ContentItem";
import { useUserFilterStore } from "../../store/userFilter.store";
import ModalWnd from "../../components/Modals/ModalWnd/ModalWnd";
import CustomFilter from "../../components/Filters/CustomFilter";
import UserForm from "../../components/Form/UserForm/UserForm";
import { transformKeysToSnakeCase } from "../../utils/utils";
import { useUsers } from "../../hooks/userHooks/useUsers";
import { currentUserId } from "../../utils/auth";
import styles from "../Page.module.css";
import { useState } from "react";
import ReloadBtn from "../../components/ReloadBtn/ReloadBtn";

function Users() {
  const userId = currentUserId();
  const filters = useUserFilterStore((state) => state.getUserFilters(userId));
  const [isModalOpen, setIsModalOpen] = useState(false);
  const params = transformKeysToSnakeCase(filters) as UserQueryParams;
  const { data: userData = [], isLoading, error } = useUsers(params);
  const createUserMutation = useCreateUser();

  const setUserFilters = useUserFilterStore((state) => state.setUserFilters);

  const handleSubmit = (data: IUserCreateFormData) => {
    createUserMutation.mutate(data);
    setIsModalOpen(false);
  };

  if (isLoading) return "Loading...";

  if (error) return "An error has occurred: " + error.message;

  if (userData.length === 0 && filters.search.length === 0) {
    return (
        <ReloadBtn
            title="No users found."
            titleBtn="Back"
        />
    );    
  }

  return (
    <div>
      < CustomFilter filters={filters} setFilters={(values) => setUserFilters(userId, values)} />
      {/* <UserFilter /> */}
      <div className="flex justify-center">
        <button className={styles["btn"]} onClick={() => setIsModalOpen(true)}>
          Create New User
        </button>
      </div>
      <div className="flex flex-col gap-2 mt-1">
        {userData.map((user) => (
          <ContentItem
            key={user.id}
            id={user.id}
            title={user.firstName + " " + user.lastName}
            endpoint="users"
            createdAt={user.createdAt}
          />
        ))}
      </div>
      <ModalWnd
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Create New User"
        content={<UserForm onSubmit={handleSubmit} />}
      />
    </div>
  );
}

export default Users;
