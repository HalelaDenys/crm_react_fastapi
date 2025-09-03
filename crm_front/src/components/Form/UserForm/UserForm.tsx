import { useState } from "react";
import type { IUserFormProps } from "../../../entities/user.types";
import style from "../Form.module.css";

export default function UserForm({ onSubmit }: IUserFormProps) {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
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
    onSubmit({ firstName, lastName, phoneNumber });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="First Name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          className={style["input"]}
        />
        <input
          type="text"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          placeholder="Last Name"
          className={style["input"]}
        />
      </div>
      <input
        type="text"
        placeholder="+380 XX XXX XXXX"
        value={phoneNumber}
        onChange={(e) => setPhoneNumber(e.target.value)}
        className={style["input"]}
      />
      {error && <p className="text-red-500 text-sm">{error}</p>}
      <button type="submit" className={style["btn_submit"]}>
        Create
      </button>
    </form>
  );
}
