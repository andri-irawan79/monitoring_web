import api from "./api";

export async function getVarietas() {
  const response = await api.get("/varietas/");
  return response.data;
}

export async function getFase() {
  const response = await api.get("/fase/");
  return response.data;
}
