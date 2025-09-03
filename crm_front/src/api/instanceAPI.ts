import axios from "axios";
import { isTokenExpired, getTokenFromLocalStorage} from "../utils/auth";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use(
    (config) => {
        const token = getTokenFromLocalStorage();

        if (token && isTokenExpired(token)) {
            localStorage.removeItem("token");
            window.location.href = "/login";
            return Promise.reject("Token expired");
        }

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

export default api;