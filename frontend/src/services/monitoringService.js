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

export const getSimulationSessionStatus = async () => {
  const response = await api.get("/monitoring/sessions/status");
  return response.data;
};

export const startWebsiteSimulation = async () => {
  const response = await api.post("/monitoring/sessions/start");
  return response.data;
};

export const stopWebsiteSimulation = async (sessionId) => {
  const response = await api.post(
    "/monitoring/sessions/" + encodeURIComponent(sessionId) + "/stop"
  );
  return response.data;
};

export const deleteAllMonitoringHistory = async () => {
  const response = await api.delete("/monitoring/history");
  return response.data;
};
