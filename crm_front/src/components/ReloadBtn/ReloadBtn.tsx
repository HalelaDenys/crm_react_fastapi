import styles from "../../page/Page.module.css";

interface ReloadBtnProps {
    title: string;
    titleBtn?: string;
}

export default function ReloadBtn({
    title,
    titleBtn = "Update window",
}: ReloadBtnProps) {
    return (
        <div className="flex flex-col gap-2 mt-1">
            <div className="text-center">{title}</div>
            <button onClick={() => window.location.reload()} className={styles["btn"]}>
                {titleBtn}
            </button>
        </div>
    );
}
