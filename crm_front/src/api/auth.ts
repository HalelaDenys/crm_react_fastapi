import api from "./instanceAPI";

interface ILoginResponse {
    access_token: string;
    refresh_token: string;
    type: string;
}


const login = async (phoneNumber: string, password: string): Promise<ILoginResponse> => {
    const formData = new URLSearchParams();
    formData.append("phone_number", phoneNumber);
    formData.append("password", password);

    try {
        const response = await api.post("/auth/login", formData, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });

        return response.data;
    } catch (error: any) {
        console.error("Login error:", error);
        throw error;
    }
};

export default login;
