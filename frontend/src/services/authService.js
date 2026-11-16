import api from "./api";
import { currentUser, setCurrentUser } from "./authState";

export async function registerAccount(payload) {
  const response = await api.post("/auth/register", payload);
  return response.data;
}

export async function loginAccount(payload) {
  const response = await api.post("/auth/login", payload);
  sessionStorage.setItem("access_token", response.data.access_token);
  sessionStorage.setItem("auth_user", JSON.stringify(response.data.user));
  setCurrentUser(response.data.user);
  return response.data.user;
}

export async function getCurrentAccount() {
  const token = sessionStorage.getItem("access_token");
  if (!token) {
    setCurrentUser(null);
    return null;
  }

  const response = await api.get("/auth/me");
  sessionStorage.setItem("auth_user", JSON.stringify(response.data));
  setCurrentUser(response.data);
  return response.data;
}

export function logoutAccount() {
  sessionStorage.removeItem("access_token");
  sessionStorage.removeItem("auth_user");
  setCurrentUser(null);
}
