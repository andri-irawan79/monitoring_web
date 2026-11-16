<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { getLatestMonitoring, getMonitoringHistory } from "../services/monitoringService";
import { getDashboardSummary } from "../services/dashboardService";
import DashboardStatGrid from "../components/dashboard/DashboardStatGrid.vue";
import MonitoringChartCard from "../components/dashboard/MonitoringChartCard.vue";
import NutrientStatusCard from "../components/dashboard/NutrientStatusCard.vue";
import MonitoringTableCard from "../components/dashboard/MonitoringTableCard.vue";
import DashboardHero from "../components/dashboard/DashboardHero.vue";
import MonitoringInsight from "../components/dashboard/MonitoringInsight.vue";

const monitoring = ref(null);
const history = ref([]);
const summary = ref({});
const lastMonitoringId = ref(null);
const lastUpdate = ref("");
let refreshInterval = null;

const updateTimestamp = () => {
  lastUpdate.value = new Date().toLocaleTimeString("id-ID");
};

const loadAllData = async () => {
  try {
    const [latest, records, totals] = await Promise.all([
      getLatestMonitoring(),
      getMonitoringHistory(),
      getDashboardSummary()
    ]);
    monitoring.value = latest;
    history.value = Array.isArray(records) ? records : [];
    summary.value = totals || {};
    lastMonitoringId.value = latest?.id ?? null;
    updateTimestamp();
  } catch (error) {
    console.error("Gagal memuat dashboard:", error);
  }
};

const checkLatestMonitoring = async () => {
  try {
    const latest = await getLatestMonitoring();
    if (!latest || latest.id === lastMonitoringId.value) return;
    const [records, totals] = await Promise.all([
      getMonitoringHistory(),
      getDashboardSummary()
    ]);
    monitoring.value = latest;
    history.value = Array.isArray(records) ? records : [];
    summary.value = totals || {};
    lastMonitoringId.value = latest.id;
    updateTimestamp();
  } catch (error) {
    console.error("Auto refresh gagal:", error);
  }
};

onMounted(async () => {
  await loadAllData();
  refreshInterval = setInterval(checkLatestMonitoring, 2000);
});

onBeforeUnmount(() => {
  if (refreshInterval) clearInterval(refreshInterval);
});
</script>

<template>
  <div class="dashboard-page space-y-7 sm:space-y-8">
    <DashboardHero :summary="summary" :last-update="lastUpdate" />

    <section v-if="monitoring" aria-labelledby="monitoring-metrics-title">
      <div class="mb-4 flex flex-wrap items-end justify-between gap-3">
        <div>
          <p class="text-xs font-bold uppercase tracking-[0.18em] text-emerald-700">Ringkasan kondisi tanah</p>
          <h2 id="monitoring-metrics-title" class="mt-1 text-xl font-bold tracking-tight text-slate-900 sm:text-2xl">Parameter Monitoring</h2>
          <p class="mt-1 text-sm text-slate-500">Nilai pengukuran dari data simulasi terakhir</p>
        </div>
        <span class="inline-flex items-center gap-2 rounded-full border border-emerald-100 bg-white px-3 py-1.5 text-xs font-semibold text-emerald-700 shadow-sm">
          <span class="h-2 w-2 rounded-full bg-emerald-500"></span>
          Data simulasi
        </span>
      </div>
      <DashboardStatGrid :monitoring="monitoring" />
    </section>

    <section class="grid grid-cols-1 items-start gap-5 2xl:grid-cols-[minmax(0,1.7fr)_minmax(300px,0.8fr)]">
      <div class="min-w-0">
        <MonitoringChartCard :data="history" />
      </div>
      <aside v-if="monitoring" class="grid min-w-0 gap-5 sm:grid-cols-2 2xl:grid-cols-1">
        <NutrientStatusCard :monitoring="monitoring" />
        <MonitoringInsight :monitoring="monitoring" :summary="summary" />
      </aside>
    </section>

    <section class="min-w-0">
      <MonitoringTableCard :data="history" />
    </section>
  </div>
</template>

<style scoped>
.dashboard-page {
  animation: dashboard-enter 420ms ease both;
}
@keyframes dashboard-enter {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .dashboard-page { animation: none; }
}
</style>