import ContentItem from "../../components/ContentItem/ContentItem";
import PositionCreateForm from "../../components/Form/PositionForm/PositionCreateForm";
import ModalWnd from "../../components/Modals/ModalWnd/ModalWnd";
import ReloadBtn from "../../components/ReloadBtn/ReloadBtn";
import type { IPositionCreateData } from "../../entities/position.types";
import { useCreatePosition } from "../../hooks/positionHooks/useCreatePosition";
import useDeletePosition from "../../hooks/positionHooks/useDeletePosition";
import { usePositions } from "../../hooks/positionHooks/usePositions";
import styles from "../Page.module.css";
import { useState } from "react";


export default function Positions() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const { data: empData = [], isLoading, error } = usePositions();
    const createPosition = useCreatePosition();
    const { handleDelete } = useDeletePosition();

    if (isLoading) return "Loading...";

    if (error) return "An error has occurred: " + error.message;

    if (empData.length === 0) {
        return (
            <ReloadBtn 
            title="Positions found."/>
        )
    }

    const handleSubmit = (data: IPositionCreateData) => {
        createPosition.mutate(data);
        setIsModalOpen(false);
    };


    return (
        <div>
            <div className="flex justify-center">
                <button className={styles["btn"]} onClick={() => setIsModalOpen(true)}>
                    Create new position
                </button>
            </div>
            <div className="flex flex-col gap-2 mt-1">
                {empData.map((emp) => (
                    <ContentItem
                        key={emp.id}
                        id={emp.id}
                        title={emp.name}
                        createdAt={emp.createdAt}
                        onClick={() => handleDelete(emp.id)}
                    />
                ))}
            </div>
            <ModalWnd
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title="Create new position"
                content={<PositionCreateForm onSubmit={handleSubmit} />}
            />
        </div>
    );
}