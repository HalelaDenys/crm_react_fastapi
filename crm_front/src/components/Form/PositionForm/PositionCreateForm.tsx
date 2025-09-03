import { useState } from "react";
import type { IPositionFormProps } from "../../../entities/position.types";
import style from "../Form.module.css";


export default function PositionCreateForm({ onSubmit }: IPositionFormProps) {
    const [name, setName] = useState("");
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        onSubmit({ name });
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Position name"
                className={style["input"]}
            />

            {error && <p className="text-red-500 text-sm">{error}</p>}
            <button type="submit" className={style["btn_submit"]}>
                Create
            </button>
        </form>
    )

}