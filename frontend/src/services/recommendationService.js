import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export const getLatestRecommendation = async () => {
  const response = await axios.get(
    `${API_URL}/recommendation/latest`
  );

  return response.data;
};

export const getRecommendationHistory = async () => {
  const response = await axios.get(
    `${API_URL}/recommendation/history`
  );

  return response.data;
};

export const generateRecommendation = async (
  monitoringId,
  faseId
) => {
  const response = await axios.post(
    `${API_URL}/recommendation/generate`,
    {
      monitoring_id: monitoringId,
      fase_id: faseId
    }
  );

  return response.data;
};

export const exportRecommendationCSV = () => {
  window.open(
    `${API_URL}/recommendation/export`,
    "_blank"
  );
};
