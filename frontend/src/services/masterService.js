import api from "./api";

export async function getFase() {
  const response = await api.get("/fase/");
  return response.data;
}
