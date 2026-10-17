import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export const getLatestMonitoring = async () => {
    const response = await axios.get(
        `${API_URL}/monitoring/latest`
    );

    return response.data;
};

export const getMonitoringHistory = async () => {
    const response = await axios.get(
        `${API_URL}/monitoring/history`
    );

    return response.data;
};
