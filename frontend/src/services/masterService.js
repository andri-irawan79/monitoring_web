import axios from "axios";

const API = "http://127.0.0.1:8000";

export async function getVarietas() {

    const res = await axios.get(
        `${API}/varietas/`
    );

    return res.data;
}

export async function getFase() {

    const res = await axios.get(
        `${API}/fase/`
    );

    return res.data;
}
