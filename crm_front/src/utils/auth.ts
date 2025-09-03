import { jwtDecode } from "jwt-decode";

interface JwtPayload {
  exp: number;
  [key: string]: any;
}

export const isTokenExpired = (token: string): boolean => {
  try {
    const payload = jwtDecode<JwtPayload>(token);
    const currentTime = Math.floor(Date.now() / 1000);
    return payload.exp < currentTime;
  } catch {
    return true;
  }
};

export const getTokenFromLocalStorage = (): string | null => {
  return localStorage.getItem("token");
};

export const currentUserId = (): number => {
  const token = getTokenFromLocalStorage();
  if (token) {
    const payload = jwtDecode<JwtPayload>(token);
    return Number(payload.sub);
  }
  return 0;
}