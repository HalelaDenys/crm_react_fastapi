import ModalWnd from "../../../components/Modals/ModalWnd/ModalWnd";

interface IConfirmDeleteModalProps {
    id: number
    isOpen: boolean;
    onClose: () => void;
    onConfirm: (id: number) => void;
    message?: string;
}

function ConfirmDeleteModal({
    id,
    isOpen,
    onClose,
    onConfirm,
    message = "Ви впевнені, що хочете видалити цей запис?",
}: IConfirmDeleteModalProps) {
    return (
        <ModalWnd
            isOpen={isOpen}
            onClose={onClose}
            title="Підтвердження видалення"
            content={
                <>
                    <p className="mb-6">{message}</p>
                    <div className="flex justify-end gap-4">
                        <button
                            onClick={onClose}
                            className="px-3 py-2 border rounded hover:bg-gray-300 
              transition duration-300 ease-in-out"
                        >
                            Скасувати
                        </button>
                        <button
                            onClick={() => onConfirm?.(id)}
                            className="px-3 py-2 bg-red-600 text-white rounded 
              hover:bg-red-800 transition duration-300 ease-in-out"
                        >
                            Видалити
                        </button>
                    </div>
                </>
            }
        />
    );
}

export default ConfirmDeleteModal;
