<script setup>
import { computed } from "vue";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";
import { Bar, Doughnut } from "vue-chartjs";
import { ChartNoAxesCombined, CircleDot, ClipboardList } from "lucide-vue-next";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend);

const props = defineProps({
  recommendations: { type: Array, default: () => [] }
});

const phaseOrder = [
  { key: "vegetatif", label: "Vegetatif" },
  { key: "pembungaan", label: "Pembungaan" },
  { key: "pembuahan", label: "Pembuahan" },
  { key: "panen", label: "Panen" },
  { key: "pascapanen", label: "Pascapanen" }
];

const fertilizerOrder = [
  { key: "UREA", label: "Urea", color: "#79A991" },
  { key: "SP36", label: "SP 36", color: "#8EA8C8" },
  { key: "KCL", label: "KCL", color: "#D3B477" },
  { key: "NPK", label: "NPK", color: "#A99BC5" }
];
const additionalFertilizerColors = ["#A6B9AD", "#C5AD99", "#9EAFBF"];

const totalRecommendations = computed(() => props.recommendations.length);
const hasRecommendations = computed(() => totalRecommendations.value > 0);
const hasLimitedSample = computed(() => totalRecommendations.value > 0 && totalRecommendations.value < 20);

const normalizeFertilizer = (value) =>
  String(value || "")
    .trim()
    .toUpperCase()
    .replace(/[^A-Z0-9]/g, "");

const fertilizerDistribution = computed(() => {
  const counts = new Map(fertilizerOrder.map((item) => [item.key, 0]));
  const additionalCounts = new Map();

  for (const item of props.recommendations) {
    const rawLabel = String(item.jenis_pupuk || "").trim();
    const key = normalizeFertilizer(rawLabel);

    if (counts.has(key)) {
      counts.set(key, counts.get(key) + 1);
    } else {
      const label = rawLabel || "Tidak diketahui";
      additionalCounts.set(label, (additionalCounts.get(label) || 0) + 1);
    }
  }

  const ordered = fertilizerOrder.map((item) => ({
    key: item.key,
    label: item.label,
    count: counts.get(item.key),
    color: item.color
  }));

  const additional = [...additionalCounts.entries()]
    .sort(([a], [b]) => a.localeCompare(b, "id"))
    .map(([label, count], index) => ({
      key: normalizeFertilizer(label),
      label,
      count,
      color: additionalFertilizerColors[index % additionalFertilizerColors.length]
    }));

  return [...ordered, ...additional];
});

const normalizePhase = (value) =>
  String(value || "")
    .trim()
    .toLocaleLowerCase("id-ID")
    .replace(/[\s_-]+/g, "");

const phaseDistribution = computed(() => {
  const counts = new Map(phaseOrder.map((phase) => [phase.key, 0]));
  let otherCount = 0;

  for (const item of props.recommendations) {
    const key = normalizePhase(item.fase);
    if (counts.has(key)) counts.set(key, counts.get(key) + 1);
    else otherCount += 1;
  }

  const result = phaseOrder.map((phase) => ({
    label: phase.label,
    count: counts.get(phase.key)
  }));
  if (otherCount) result.push({ label: "Lainnya", count: otherCount });
  return result;
});

const doughnutData = computed(() => ({
  labels: fertilizerDistribution.value.map((item) => item.label),
  datasets: [
    {
      data: fertilizerDistribution.value.map((item) => item.count),
      backgroundColor: fertilizerDistribution.value.map((item) => item.color),
      borderColor: "#ffffff",
      borderWidth: 3,
      hoverOffset: 7
    }
  ]
}));

const doughnutCenterPlugin = {
  id: "recommendation-doughnut-center",
  afterDraw(chart) {
    if (!chart.chartArea) return;
    const { ctx, chartArea } = chart;
    const x = (chartArea.left + chartArea.right) / 2;
    const y = (chartArea.top + chartArea.bottom) / 2;
    ctx.save();
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillStyle = "#64748b";
    ctx.font = "600 10px Inter, ui-sans-serif, sans-serif";
    ctx.fillText("TOTAL", x, y - 10);
    ctx.fillStyle = "#0f172a";
    ctx.font = "800 24px Inter, ui-sans-serif, sans-serif";
    ctx.fillText(String(totalRecommendations.value), x, y + 13);
    ctx.restore();
  }
};

const doughnutPercentagePlugin = {
  id: "recommendation-doughnut-percentages",
  afterDatasetsDraw(chart) {
    const values = (chart.data.datasets[0]?.data || []).map((value) => Math.max(0, Number(value) || 0));
    const total = values.reduce((sum, value) => sum + value, 0);
    if (!total) return;

    const arcs = chart.getDatasetMeta(0).data;
    const { ctx } = chart;
    ctx.save();
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "700 10px Inter, ui-sans-serif, sans-serif";

    arcs.forEach((arc, index) => {
      const value = values[index];
      if (!arc || !value) return;

      const startAngle = arc.startAngle;
      const endAngle = arc.endAngle;
      const circumference = Math.abs(endAngle - startAngle);
      if (circumference < 0.28) return;

      const radius = (arc.innerRadius + arc.outerRadius) / 2;
      const angle = (startAngle + endAngle) / 2;
      const x = arc.x + Math.cos(angle) * radius;
      const y = arc.y + Math.sin(angle) * radius;
      const percentage = (value / total) * 100;
      const label = percentage.toFixed(1) + "%";
      const availableWidth = radius * circumference * 0.82;

      // Leave very narrow slices unlabeled; their exact percentage remains in the legend.
      if (ctx.measureText(label).width > availableWidth) return;

      ctx.lineWidth = 2.5;
      ctx.strokeStyle = "rgba(15, 23, 42, 0.18)";
      ctx.strokeText(label, x, y);
      ctx.fillStyle = "#ffffff";
      ctx.fillText(label, x, y);
    });

    ctx.restore();
  }
};

const doughnutLegendGenerator = ChartJS.overrides.doughnut.plugins.legend.labels.generateLabels;

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: "70%",
  animation: { duration: 550, easing: "easeOutQuart" },
  plugins: {
    legend: {
      position: "bottom",
      labels: {
        usePointStyle: true,
        pointStyle: "circle",
        generateLabels(chart) {
          const items = doughnutLegendGenerator(chart);
          const values = chart.data.datasets[0]?.data || [];
          const total = values.reduce((sum, value) => sum + Math.max(0, Number(value) || 0), 0);

          return items.map((item) => {
            const value = Math.max(0, Number(values[item.index]) || 0);
            const percentage = total ? ((value / total) * 100).toFixed(1) : "0.0";
            return { ...item, text: item.text + " · " + percentage + "%" };
          });
        },
        boxWidth: 10,
        boxHeight: 10,
        padding: 16,
        color: "#526579",
        font: { size: 12, weight: "600" }
      }
    },
    tooltip: {
      backgroundColor: "#14392d",
      titleColor: "#f8fafc",
      bodyColor: "#e2e8f0",
      padding: 11,
      cornerRadius: 10,
      callbacks: {
        label: (context) => {
          const value = Number(context.parsed || 0);
          const percentage = totalRecommendations.value
            ? ((value / totalRecommendations.value) * 100).toFixed(1)
            : "0.0";
          return " " + context.label + ": " + value + " (" + percentage + "%)";
        }
      }
    }
  }
};

const phaseData = computed(() => ({
  labels: phaseDistribution.value.map((item) => item.label),
  datasets: [
    {
      label: "Jumlah rekomendasi",
      data: phaseDistribution.value.map((item) => item.count),
      backgroundColor: ["#087f5b", "#16966e", "#36a77c", "#77bd76", "#a8cf72", "#94a3b8"],
      borderRadius: 7,
      borderSkipped: false,
      barThickness: 17,
      maxBarThickness: 20
    }
  ]
}));

const phaseOptions = {
  indexAxis: "y",
  responsive: true,
  maintainAspectRatio: false,
  animation: { duration: 550, easing: "easeOutQuart" },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: "#14392d",
      titleColor: "#f8fafc",
      bodyColor: "#e2e8f0",
      padding: 11,
      cornerRadius: 10,
      callbacks: {
        label: (context) => " " + context.parsed.x + " rekomendasi"
      }
    }
  },
  scales: {
    x: {
      beginAtZero: true,
      border: { display: false },
      grid: { color: "rgba(148,163,184,.16)", drawTicks: false },
      ticks: {
        color: "#94a3b8",
        precision: 0,
        stepSize: 1,
        font: { size: 10 }
      }
    },
    y: {
      border: { display: false },
      grid: { display: false },
      ticks: {
        color: "#64748b",
        font: { size: 11, weight: "600" }
      }
    }
  }
};
</script>

<template>
  <section class="space-y-4">
    <div class="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.18em] text-emerald-700">Analisis keluaran sistem</p>
        <h2 class="mt-1 text-xl font-bold tracking-tight text-slate-900 sm:text-2xl">Analisis Hasil Rekomendasi</h2>
        <p class="mt-1 text-sm text-slate-500">Komposisi jenis pupuk dan sebaran rekomendasi pada fase pertumbuhan.</p>
      </div>
      <span class="inline-flex w-fit items-center gap-1.5 rounded-full border border-emerald-100 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700">
        <ClipboardList class="h-3.5 w-3.5" />
        {{ totalRecommendations }} rekomendasi dianalisis
      </span>
    </div>

    <div class="grid grid-cols-1 items-stretch gap-5 2xl:grid-cols-2">
      <article class="flex min-h-[390px] flex-col rounded-2xl border border-slate-200/80 bg-white p-4 shadow-[0_3px_18px_-12px_rgba(15,23,42,.22)] sm:p-5">
        <div class="mb-3 flex items-center gap-3">
          <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700">
            <CircleDot class="h-5 w-5" />
          </span>
          <div>
            <h3 class="text-base font-bold tracking-tight text-slate-900">Distribusi Jenis Pupuk</h3>
            <p class="mt-0.5 text-xs text-slate-500">Proporsi jenis pupuk dari hasil rekomendasi.</p>
          </div>
        </div>

        <div v-if="hasRecommendations" class="flex flex-1 items-center justify-center">
          <div class="h-[285px] w-full max-w-[440px]">
            <Doughnut :data="doughnutData" :options="doughnutOptions" :plugins="[doughnutCenterPlugin, doughnutPercentagePlugin]" />
          </div>
        </div>
        <div v-else class="flex flex-1 flex-col items-center justify-center rounded-xl bg-emerald-50/40 px-4 text-center">
          <CircleDot class="h-8 w-8 text-emerald-300" />
          <p class="mt-3 text-sm font-semibold text-slate-700">Belum ada data rekomendasi</p>
          <p class="mt-1 text-xs text-slate-500">Distribusi pupuk akan tampil setelah rekomendasi dibuat.</p>
        </div>
      </article>

      <article class="flex min-h-[390px] flex-col rounded-2xl border border-slate-200/80 bg-white p-4 shadow-[0_3px_18px_-12px_rgba(15,23,42,.22)] sm:p-5">
        <div class="mb-3 flex items-center gap-3">
          <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-lime-50 text-lime-700">
            <ChartNoAxesCombined class="h-5 w-5" />
          </span>
          <div>
            <h3 class="text-base font-bold tracking-tight text-slate-900">Rekomendasi per Fase</h3>
            <p class="mt-0.5 text-xs text-slate-500">Jumlah rekomendasi pada setiap fase pertumbuhan.</p>
          </div>
        </div>

        <div v-if="hasRecommendations" class="flex flex-1 items-center">
          <div class="h-[285px] w-full">
            <Bar :data="phaseData" :options="phaseOptions" />
          </div>
        </div>
        <div v-else class="flex flex-1 flex-col items-center justify-center rounded-xl bg-lime-50/40 px-4 text-center">
          <ChartNoAxesCombined class="h-8 w-8 text-lime-400" />
          <p class="mt-3 text-sm font-semibold text-slate-700">Belum ada data fase</p>
          <p class="mt-1 text-xs text-slate-500">Distribusi fase akan tampil setelah rekomendasi dibuat.</p>
        </div>
      </article>
    </div>

    <p v-if="hasLimitedSample" class="rounded-xl border border-amber-100 bg-amber-50/70 px-3.5 py-2.5 text-xs leading-5 text-amber-800">
      Catatan: distribusi dihitung dari {{ totalRecommendations }} rekomendasi tersimpan. Jumlah per fase mencerminkan frekuensi rekomendasi yang dibuat pada fase tersebut, bukan ukuran kebutuhan pupuk atau keberhasilan agronomis.
    </p>
    <p v-else-if="hasRecommendations" class="text-[11px] leading-5 text-slate-400">
      Distribusi menunjukkan frekuensi keluaran sistem, bukan jumlah pupuk yang diaplikasikan atau tingkat kebutuhan setiap fase.
    </p>
  </section>
</template>
