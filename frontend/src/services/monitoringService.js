import api from "./api";

export const getLatestMonitoring = async () => {
  const response = await api.get("/monitoring/latest");
  return response.data;
};

export const getMonitoringHistory = async () => {
  const response = await api.get("/monitoring/history");
  return response.data;
};

export const getSimulatorStatus = async () => {
  const response = await api.get("/monitoring/simulator-status");
  return response.data;
};
