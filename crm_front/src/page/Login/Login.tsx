import { useState } from "react";
import styles from "./Login.module.css";
import { useNavigate } from "react-router-dom";
import login from "../../api/auth";

function Login() {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);


    try {
      const response = await login(phoneNumber, password);
      const token = response.access_token;
      localStorage.setItem("token", token);
      navigate("/");
    } catch (err) {
      setError("Невірний номер телефону або пароль");
      console.error(err);
    }
  };

  return (
    <div className={styles["wrapper"]}>
      <div className={styles["login-container"]}>
        <h2 className="text-2xl mb-4">Вхід</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full">
          <input
            type="text"
            className={styles["input"]}
            placeholder="+380 67 123 45 67"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            required
          />
          <div className="relative w-full mb-3">
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              className={`!mb-0 ${styles["input"]}`}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2"
            >
              <img
                src={showPassword ? "/eye-slash.svg" : "/eye.svg"}
                alt="toggle password visibility"
                className="w-5 h-5"
              />
            </button>
          </div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <button type="submit" className={styles["btn"]}>
            Увійти
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
