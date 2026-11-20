import api from "./api";

export const getLatestRecommendation = async () => {
  const response = await api.get("/recommendation/latest");
  return response.data;
};

export const getRecommendationHistory = async () => {
  const response = await api.get("/recommendation/history");
  return response.data;
};

export const deleteRecommendation = async (recommendationId) => {
  const response = await api.delete(`/recommendation/${recommendationId}`);
  return response.data;
};

export const generateRecommendation = async (monitoringId, faseId) => {
  const response = await api.post("/recommendation/generate", {
    monitoring_id: monitoringId,
    fase_id: faseId
  });
  return response.data;
};

export const exportRecommendationCSV = async () => {
  const response = await api.get("/recommendation/export", {
    responseType: "blob"
  });
  const objectUrl = URL.createObjectURL(response.data);
  const link = document.createElement("a");
  link.href = objectUrl;
  link.download = "riwayat_rekomendasi.csv";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(objectUrl);
};
