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

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

const props = defineProps({ data: { type: Array, default: () => [] } });

const latestData = computed(() => [...props.data].reverse().slice(-30));
const chartData = computed(() => ({
  labels: latestData.value.map(row => {
    const raw = row.simulation_date || row.created_at || "";
    if (!raw) return "-";
    const date = new Date(raw);
    return Number.isNaN(date.getTime()) ? String(raw) : date.toLocaleDateString("id-ID", { day: "2-digit", month: "short" });
  }),
  datasets: [
    {
      label: "Nitrogen",
      data: latestData.value.map(row => Number(row.nitrogen)),
      borderColor: "#15966a",
      backgroundColor: "rgba(21,150,106,0.08)",
      borderWidth: 2.5,
      pointRadius: 0,
      pointHoverRadius: 5,
      pointHitRadius: 12,
      pointHoverBackgroundColor: "#15966a",
      pointHoverBorderColor: "#ffffff",
      pointHoverBorderWidth: 2,
      tension: 0.34,
      fill: false
    },
    {
      label: "Fosfor",
      data: latestData.value.map(row => Number(row.phosphorus)),
      borderColor: "#4f78d1",
      backgroundColor: "rgba(79,120,209,0.06)",
      borderWidth: 2.5,
      pointRadius: 0,
      pointHoverRadius: 5,
      pointHitRadius: 12,
      pointHoverBackgroundColor: "#4f78d1",
      pointHoverBorderColor: "#ffffff",
      pointHoverBorderWidth: 2,
      tension: 0.34,
      fill: false
    },
    {
      label: "Kalium",
      data: latestData.value.map(row => Number(row.potassium)),
      borderColor: "#d99a35",
      backgroundColor: "rgba(217,154,53,0.06)",
      borderWidth: 2.5,
      pointRadius: 0,
      pointHoverRadius: 5,
      pointHitRadius: 12,
      pointHoverBackgroundColor: "#d99a35",
      pointHoverBorderColor: "#ffffff",
      pointHoverBorderWidth: 2,
      tension: 0.34,
      fill: false
    }
  ]
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: { duration: 650, easing: "easeOutQuart" },
  interaction: { mode: "index", intersect: false },
  layout: { padding: { top: 8, right: 8, bottom: 0, left: 0 } },
  plugins: {
    legend: {
      position: "top",
      align: "start",
      labels: {
        usePointStyle: true,
        pointStyle: "circle",
        boxWidth: 7,
        boxHeight: 7,
        padding: 20,
        color: "#64748b",
        font: { size: 12, weight: "600" }
      }
    },
    tooltip: {
      backgroundColor: "#142b24",
      titleColor: "#f8fafc",
      bodyColor: "#e2e8f0",
      borderColor: "rgba(255,255,255,.12)",
      borderWidth: 1,
      padding: 12,
      cornerRadius: 10,
      displayColors: true,
      usePointStyle: true,
      callbacks: {
        label: context => ` ${context.dataset.label}: ${Number(context.parsed.y).toFixed(2)} mg/kg`
      }
    }
  },
  scales: {
    x: {
      border: { display: false },
      grid: { display: false },
      ticks: { color: "#94a3b8", autoSkip: true, maxTicksLimit: 8, maxRotation: 0, font: { size: 10 } }
    },
    y: {
      beginAtZero: true,
      border: { display: false, dash: [3, 4] },
      grid: { color: "rgba(148,163,184,.16)", drawTicks: false },
      ticks: { color: "#94a3b8", padding: 10, font: { size: 10 }, maxTicksLimit: 6 }
    }
  }
};
</script>

<template>
  <div class="chart-shell">
    <div v-if="!latestData.length" class="flex h-[300px] flex-col items-center justify-center rounded-xl bg-slate-50/80 text-center">
      <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-white text-slate-400 shadow-sm">
        <svg viewBox="0 0 24 24" class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 3v18h18M7 14l4-4 3 3 6-7"/></svg>
      </div>
      <p class="mt-3 text-sm font-semibold text-slate-700">Belum ada data grafik</p>
      <p class="mt-1 text-xs text-slate-400">Data simulasi akan ditampilkan setelah dikirim ke sistem.</p>
    </div>
    <div v-else class="h-[300px] sm:h-[350px]">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<style scoped>
.chart-shell { min-width: 0; width: 100%; }
</style>