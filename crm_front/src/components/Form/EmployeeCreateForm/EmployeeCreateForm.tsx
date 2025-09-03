import { useState } from "react";
import style from "../Form.module.css";
import { usePositions } from "../../../hooks/positionHooks/usePositions";
import CustomSelect from "../../CustomSelect/CustomSelect";
import type { IEmployeeFormProps } from "../../../entities/employee.types";

export default function EmployeeCreateForm({ onSubmit }: IEmployeeFormProps) {
    const [error, setError] = useState<string | null>(null);
    const { data: positionsData = [] } = usePositions();

    const [showPassword, setShowPassword] = useState(false);
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [patronymic, setPatronymic] = useState("");
    const [phoneNumber, setPhoneNumber] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [IsAdmin, setIsAdmin] = useState(false);
    const [positionId, setPositionId] = useState<number>(1);


    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault(); setError(null);
        if (!phoneNumber.startsWith("+380")) {
            setError("Номер телефону повинен починатися з +380");
            return;
        }

        if (phoneNumber.length !== 13) {
            setError("Номер телефону повинен містити рівно 13 символів");
            return;
        }

        if (!/^\+380\d{9}$/.test(phoneNumber)) {
            setError("Номер повинен містити лише цифри після +380");
            return;
        }
        onSubmit({
            firstName,
            lastName,
            patronymic: patronymic || null,
            phoneNumber,
            email: email || null,
            positionId: positionId as number,
            password,
            isAdmin: IsAdmin,
        });
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="flex gap-4">
                <input
                    type="text"
                    placeholder="Ім'я"
                    className={style["input"]}
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    required
                />
                <input
                    type="text"
                    placeholder="Прізвище"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    className={style["input"]}
                    required
                />
            </div>
            <div className="flex gap-4">
                <input type="text"
                    placeholder="По-батькові"
                    value={patronymic}
                    onChange={(e) => setPatronymic(e.target.value)}
                    className={style["input"]} />
                <input
                    type="text"
                    placeholder="+380 XX XXX XXXX"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                    className={style["input"]}
                    required
                />
            </div>
            <div className="flex gap-4">
                <input
                    type="text"
                    placeholder="Пошта"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className={`${style["input"]}`}
                />

                <div className="flex gap-2 p-2.5 items-center pt-1">
                    <label className="text-lg">Admin: </label>
                    <input type="checkbox" onChange={(e) => setIsAdmin(e.target.checked)} />
                </div>
            </div>
            <div className="relative w-full mb-3">
                <input
                    type={showPassword ? "text" : "password"}
                    placeholder="Password"
                    className={`!mb-0 ${style["input"]}`}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button>
                    <img
                        src={showPassword ? "/eye-slash.svg" : "/eye.svg"}
                        alt=""
                        className="w-5 h-5 absolute right-3 top-1/2 -translate-y-1/2 text-gray-500"
                        onClick={() => setShowPassword(!showPassword)}
                    />
                </button>
            </div>
            <div className="flex justify-center w-full">
            <CustomSelect
                label="Виберіть посаду: "
                selectedValue={positionId}
                options={positionsData.map((p) => ({
                value: p.name,
                id: p.id,
                }))}
                onChange={(opt) => {
                setPositionId(opt.id);
                }}
            />
            </div>

            {error && <p className="text-red-500 text-sm">{error}</p>}
            <button type="submit" className={`mt-4 ${style["btn_submit"]}`}>
                Create
            </button>
        </form>
    );
}
