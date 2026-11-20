import api from "./api";

const PHASE_ORDER = {
  vegetatif: 0,
  pembungaan: 1,
  pembuahan: 2,
  panen: 3,
  pascapanen: 4
};

function normalizePhaseName(name) {
  return String(name ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]/g, "");
}

export async function getFase() {
  const response = await api.get("/fase/");
  const phases = Array.isArray(response.data) ? response.data : [];

  // Urutkan berdasarkan siklus tanaman, bukan berdasarkan ID database.
  // ID asli tetap dipertahankan untuk dikirim ke endpoint rekomendasi.
  return phases
    .map((phase, index) => ({
      phase,
      index,
      order: PHASE_ORDER[normalizePhaseName(phase?.nama)] ?? Number.MAX_SAFE_INTEGER
    }))
    .sort((a, b) => a.order - b.order || a.index - b.index)
    .map(({ phase }) => phase);
}
