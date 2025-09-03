import { useNavigate, useParams } from "react-router-dom";
import BackBtn from "../../../components/BackBtn/BackBtn";
import useEmployeeForm from "../../../hooks/empHooks/useEmployeeForm";
import { formatDateString } from "../../../utils/utils";
import ValidatedInput from "../../../components/ValidatedInput/ValidatedInput";
import styles from "../Card.module.css";
import CustomSelect from "../../../components/CustomSelect/CustomSelect";
import { usePositions } from "../../../hooks/positionHooks/usePositions";
import useDeleteEmployee from "../../../hooks/empHooks/useDeleteEmployee";
import ConfirmDeleteModal from "../../../components/Modals/ConfirmDeleteModal/ConfirmDeleteModal";
import { useState } from "react";
import useUpdateEmployeeForm from "../../../hooks/empHooks/useUpdateEmpForm";

function EmployeeCard() {
  const { id } = useParams<{ id?: string }>();
  const navigate = useNavigate();
  const userId = Number(id);
  const {
    isLoading,
    error,
    empData,
    empForm,
    setEmpForm,
    validationErrors,
    setValidationErrors,
  } = useEmployeeForm(userId);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { data: positionsData = [] } = usePositions();
  const { handleSubmit, isUpdating } = useUpdateEmployeeForm(
    empData!,
    empForm!,
    setValidationErrors
  ); const { handleDelete, isDeleting } = useDeleteEmployee(() => {
    navigate("/employees");
  })

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Помилка: {(error as Error).message}</p>;
  if (!empForm) return <p>Немає даних користувача</p>;

  const isChanged = JSON.stringify(empData) !== JSON.stringify(empForm);
  const formattedDate = formatDateString(empData!.createdAt!);


  return (
    <div>
      <BackBtn endpoint="employees" />

      <h1 className="text-xl my-3">Користувач ID: {id}</h1>
      <form onSubmit={handleSubmit}>
        <div className="flex flex-col border border-black p-4">
          <div>
            <ValidatedInput
              label="Ім'я: "
              name="first_name"
              value={empForm.firstName}
              onChange={(value) => {
                setEmpForm({ ...empForm, firstName: value }),
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
              value={empForm.lastName}
              onChange={(value) => {
                setEmpForm({ ...empForm, lastName: value }),
                  setValidationErrors((prev) => ({ ...prev, last_name: "" }));
              }}
              error={validationErrors.last_name}
            />
          </div>
          {empData?.patronymic && (
            <div>
              <ValidatedInput
                label="По-батькові: "
                name="patronymic"
                value={empForm?.patronymic || ""}
                onChange={(value) => {
                  setEmpForm({ ...empForm, patronymic: value }),
                    setValidationErrors((prev) => ({
                      ...prev,
                      patronymic: "",
                    }));
                }}
                error={validationErrors.patronymic}
              />
            </div>
          )}
          {empForm?.email && (
            <div>
              <ValidatedInput
                label="Електрона пошта: "
                name="email"
                value={empData?.email || ""}
                onChange={(value) => {
                  setEmpForm({ ...empForm, email: value }),
                    setValidationErrors((prev) => ({ ...prev, email: "" }));
                }}
                error={validationErrors.email}
              />
            </div>
          )}
          <div>
            <ValidatedInput
              label="Телефон: "
              name="phone_number"
              value={empData?.phoneNumber}
              onChange={(value) => {
                setEmpForm({ ...empForm, phoneNumber: value }),
                  setValidationErrors((prev) => ({
                    ...prev,
                    phone_number: "",
                  }));
              }}
            />
          </div>
          <div>
            <ValidatedInput
              label="Активний: "
              name="is_active"
              type="checkbox"
              checked={empForm.isActive}
              onChange={(val) =>
                setEmpForm({ ...empForm, isActive: val === "true" })
              }
              error={validationErrors.is_active}
            />
          </div>
          <div>
            <ValidatedInput
              label="Права адміністратора: "
              name="is_admin"
              type="checkbox"
              checked={empForm.isAdmin}
              onChange={(val) =>
                setEmpForm({ ...empForm, isAdmin: val === "true" })
              }
              error={validationErrors.is_admin}
            />
          </div>
          <CustomSelect
            label="Посада: "
            selectedValue={empForm.positionId}
            options={positionsData.map((position) => ({
              value: position.name,
              id: position.id,
            }))}
            onChange={(option) => {
              setEmpForm({
                ...empForm,
                position: option.value,
                positionId: option.id,
              });
            }}
          />
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
            type="button"
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

export default EmployeeCard;
``;
