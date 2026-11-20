import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
  timeout: 15000,
});

api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;
    const hasToken = Boolean(sessionStorage.getItem("access_token"));
    const isAuthRequest = error.config?.url?.startsWith("/auth/");

    if (status === 401 && hasToken && !isAuthRequest) {
      sessionStorage.removeItem("access_token");
      sessionStorage.removeItem("auth_user");
      if (window.location.pathname !== "/login") {
        window.location.replace("/login?expired=1");
      }
    }

    return Promise.reject(error);
  }
);

export default api;
