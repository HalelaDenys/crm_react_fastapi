import ConfirmDeleteModal from "../../../components/Modals/ConfirmDeleteModal/ConfirmDeleteModal";
import useDeleteUserHandler from "../../../hooks/userHooks/useDeleteUserHandler";
import ValidatedInput from "../../../components/ValidatedInput/ValidatedInput";
import useUpdateUserForm from "../../../hooks/userHooks/useUpdateUserForm";
import useUserForm from "../../../hooks/userHooks/useUserForm";
import { useNavigate, useParams } from "react-router-dom";
import { useState } from "react";
import BackBtn from "../../../components/BackBtn/BackBtn";
import { formatDateString } from "../../../utils/utils";
import styles from "../Card.module.css";

function UsersCard() {
  const { id } = useParams<{ id?: string }>();
  const navigate = useNavigate();
  const userId = Number(id);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const { userForm, setUserForm, validationErrors, setValidationErrors, isLoading, error, userData } = useUserForm(userId);
  const { handleSubmit, isUpdating } = useUpdateUserForm(userData ?? null, userForm, setValidationErrors);
  const { handleDelete, isDeleting } = useDeleteUserHandler(() => {
    setIsModalOpen(false);
    navigate("/users");
  });

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Помилка: {(error as Error).message}</p>;
  if (!userForm) return <p>Немає даних користувача</p>;

  const isChanged = JSON.stringify(userData) !== JSON.stringify(userForm);
  const formattedDate = formatDateString(userData!.createdAt!);


  return (
    <div>
      <BackBtn endpoint="users" />

      <h1 className="text-xl my-3">Користувач ID: {id}</h1>
      <form onSubmit={handleSubmit}>
        <div className="flex flex-col border border-black p-4">
          <div>
            <ValidatedInput
              label="Ім'я: "
              name="first_name"
              value={userForm.firstName}
              onChange={(value) => {
                setUserForm({ ...userForm, firstName: value }),
                  setValidationErrors((prev) => ({ ...prev, first_name: "" }));
              }}
              error={validationErrors.first_name}
              type="text"
            />
          </div>
          <div>
            <ValidatedInput
              label="Прізвище: "
              name="last_name"
              value={userForm.lastName}
              onChange={(value) => {
                setUserForm({ ...userForm, lastName: value }),
                  setValidationErrors((prev) => ({ ...prev, last_name: "" }));
              }}
              error={validationErrors.last_name}
              type="text"
            />
          </div>
          <div>

            <ValidatedInput
              label="Телефон: "
              name="phone_number"
              value={userForm.phoneNumber}
              error={validationErrors.phone_number}
              onChange={(val) => {
                setUserForm({ ...userForm, phoneNumber: val });
                setValidationErrors((prev) => ({ ...prev, phone_number: "" }));
              }}
            />

          </div>
          <div>
            <ValidatedInput
              label="Активний: "
              name="is_active"
              type="checkbox"
              checked={userForm.isActive}
              onChange={(val) =>
                setUserForm({ ...userForm, isActive: val === "true" })
              }
            />
          </div>
          <div className="mt-2">
            <span className="text-lg italic">Створено: {formattedDate}</span>
          </div>
        </div>
        <div className="flex justify-end mt-2">
          {isChanged && (
            <button
              type="submit"
              disabled={isUpdating}
              className={styles["update-btn"]}
            >
              Оновити
            </button>
          )}
          <button
            onClick={() => setIsModalOpen(true)}
            disabled={isDeleting}
            className={styles["delete-btn"]}
          >
            Видалити
          </button>
        </div>
      </form>
      <ConfirmDeleteModal
        id={userId}
        isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onConfirm={handleDelete}
      />
    </div>
  );
}

export default UsersCard;
