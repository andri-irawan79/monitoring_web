<script setup>
import { computed } from "vue";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from "chart.js";
import { Line } from "vue-chartjs";
import { Activity, CalendarDays } from "lucide-vue-next";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const props = defineProps({
  data: { type: Array, default: () => [] }
});

// Endpoint monitoring mengirim data terbaru lebih dulu.
// Balik urutan agar grafik dibaca dari data lama ke data terbaru.
const latestData = computed(() => [...props.data].reverse().slice(-30));
const validValues = computed(() =>
  latestData.value
    .map((row) => (row.ph === null || row.ph === "" ? null : Number(row.ph)))
    .filter((value) => Number.isFinite(value))
);

const formatDate = (value) => {
  if (!value) return "-";
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? String(value)
    : date.toLocaleDateString("id-ID", { day: "2-digit", month: "short" });
};

const chartData = computed(() => ({
  labels: latestData.value.map((row) =>
    formatDate(row.simulation_date || row.created_at)
  ),
  datasets: [
    {
      label: "pH tanah",
      data: latestData.value.map((row) => {
        if (row.ph === null || row.ph === "") return null;
        const value = Number(row.ph);
        return Number.isFinite(value) ? value : null;
      }),
      borderColor: "#0f8a61",
      backgroundColor: "rgba(16, 185, 129, 0.12)",
      borderWidth: 2.5,
      pointRadius: 2.5,
      pointHoverRadius: 5,
      pointBackgroundColor: "#0f8a61",
      pointBorderColor: "#ffffff",
      pointBorderWidth: 2,
      tension: 0.32,
      fill: true,
      spanGaps: false
    }
  ]
}));

const chartOptions = computed(() => {
  const values = validValues.value;
  const observedMin = values.length ? Math.min(...values) : 0;
  const observedMax = values.length ? Math.max(...values) : 14;
  const axisMin = Math.max(0, Math.floor(observedMin - 0.5));
  const axisMax = Math.min(14, Math.ceil(observedMax + 0.5));

  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 550, easing: "easeOutQuart" },
    interaction: { mode: "index", intersect: false },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: "#14392d",
        titleColor: "#f8fafc",
        bodyColor: "#e2e8f0",
        borderColor: "rgba(255,255,255,.12)",
        borderWidth: 1,
        padding: 11,
        cornerRadius: 10,
        displayColors: false,
        callbacks: {
          label: (context) => " pH: " + Number(context.parsed.y).toFixed(2)
        }
      }
    },
    scales: {
      x: {
        border: { display: false },
        grid: { display: false },
        ticks: {
          color: "#94a3b8",
          autoSkip: true,
          maxTicksLimit: 9,
          maxRotation: 0,
          font: { size: 10 }
        }
      },
      y: {
        min: axisMin,
        max: axisMax > axisMin ? axisMax : Math.min(14, axisMin + 1),
        border: { display: false, dash: [3, 4] },
        grid: { color: "rgba(148,163,184,.16)", drawTicks: false },
        ticks: {
          color: "#94a3b8",
          padding: 9,
          maxTicksLimit: 6,
          font: { size: 10 },
          callback: (value) => Number(value).toFixed(1)
        }
      }
    }
  };
});

const recordCount = computed(() => latestData.value.length);
</script>

<template>
  <section class="overflow-hidden rounded-2xl border border-emerald-100/80 bg-white p-4 shadow-[0_3px_18px_-12px_rgba(15,65,48,.24)] sm:p-5">
    <div class="mb-4 flex flex-wrap items-start justify-between gap-3">
      <div class="flex min-w-0 items-start gap-3">
        <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700">
          <Activity class="h-5 w-5" />
        </div>
        <div class="min-w-0">
          <h2 class="text-lg font-bold tracking-tight text-slate-900">Tren pH Tanah</h2>
          <p class="mt-1 text-xs leading-5 text-slate-500 sm:text-sm">
            Perubahan tingkat keasaman tanah berdasarkan data simulasi
          </p>
        </div>
      </div>
      <span class="inline-flex shrink-0 items-center gap-1.5 rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700">
        <CalendarDays class="h-3.5 w-3.5" />
        {{ recordCount }} data terakhir
      </span>
    </div>

    <div v-if="!recordCount" class="flex min-h-[260px] flex-col items-center justify-center rounded-xl bg-emerald-50/50 px-4 text-center">
      <Activity class="h-8 w-8 text-emerald-300" />
      <p class="mt-3 text-sm font-semibold text-slate-700">Belum ada data pH</p>
      <p class="mt-1 text-xs text-slate-500">Grafik akan tampil setelah data simulasi tersedia.</p>
    </div>
    <div v-else class="h-[260px] min-w-0 sm:h-[290px]">
      <Line :data="chartData" :options="chartOptions" />
    </div>

    <p class="mt-3 border-t border-slate-100 pt-3 text-[11px] leading-5 text-slate-400">
      Grafik menggunakan catatan simulasi terbaru. Skala vertikal menyesuaikan rentang nilai agar perubahan pH lebih mudah diamati.
    </p>
  </section>
</template>
