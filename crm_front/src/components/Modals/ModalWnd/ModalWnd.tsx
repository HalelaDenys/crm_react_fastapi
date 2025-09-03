interface IModalWndProps {
  isOpen: boolean;
  onClose: () => void;
  title: string
  content?: React.ReactNode;
}

function ModalWnd({ isOpen, onClose, title, content }: IModalWndProps) {
    if (!isOpen) return null;

    const handleBackgroundClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

    return (
        <div
            className="modal fixed inset-0 bg-gray-900 opacity-90 flex items-center justify-center z-50"
            onClick={handleBackgroundClick}
        >
            <div className="bg-zinc-400 p-6 rounded-lg shadow-lg w-full max-w-md relative">
                <h2 className="text-xl font-bold mb-4">{title}</h2>
                <i
                    onClick={onClose}
                    className="absolute top-3 right-3 cursor-pointer hover:opacity-50"
                >
                    ❌
                </i>

                {content}

            </div>
        </div>
    );
}

export default ModalWnd;
