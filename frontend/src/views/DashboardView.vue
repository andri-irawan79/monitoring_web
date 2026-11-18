<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from "vue";
import { useRoute } from "vue-router";
import { getLatestMonitoring, getMonitoringHistory } from "../services/monitoringService";
import { getDashboardSummary } from "../services/dashboardService";
import DashboardStatGrid from "../components/dashboard/DashboardStatGrid.vue";
import MonitoringChartCard from "../components/dashboard/MonitoringChartCard.vue";
import NutrientStatusCard from "../components/dashboard/NutrientStatusCard.vue";
import DashboardHero from "../components/dashboard/DashboardHero.vue";
import MonitoringInsight from "../components/dashboard/MonitoringInsight.vue";
import PHTrendCard from "../components/dashboard/PHTrendCard.vue";
import RecommendationAnalytics from "../components/dashboard/RecommendationAnalytics.vue";
import { getRecommendationHistory } from "../services/recommendationService";

const route = useRoute();
const monitoring = ref(null);
const history = ref([]);
const recommendations = ref([]);
const recommendationLoading = ref(false);
const summary = ref({});
const lastMonitoringId = ref(null);
const lastUpdate = ref("");
let refreshInterval = null;
let recommendationRefreshInterval = null;

const updateTimestamp = () => { lastUpdate.value = new Date().toLocaleTimeString("id-ID"); };

const loadAllData = async () => {
  try {
    const [latest, records, totals] = await Promise.all([
      getLatestMonitoring(), getMonitoringHistory(), getDashboardSummary()
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

const loadRecommendationData = async () => {
  if (recommendationLoading.value) return;
  recommendationLoading.value = true;
  try {
    const records = await getRecommendationHistory();
    recommendations.value = Array.isArray(records) ? records : [];
  } catch (error) {
    console.error("Gagal memperbarui analisis rekomendasi:", error);
  } finally {
    recommendationLoading.value = false;
  }
};

const checkLatestMonitoring = async () => {
  try {
    const latest = await getLatestMonitoring();
    if (!latest || latest.id === lastMonitoringId.value) return;
    const [records, totals] = await Promise.all([getMonitoringHistory(), getDashboardSummary()]);
    monitoring.value = latest;
    history.value = Array.isArray(records) ? records : [];
    summary.value = totals || {};
    lastMonitoringId.value = latest.id;
    updateTimestamp();
  } catch (error) {
    console.error("Auto refresh gagal:", error);
  }
};

const scrollToRequestedSection = async () => {
  if (!route.hash) return;
  await nextTick();
  window.setTimeout(() => document.querySelector(route.hash)?.scrollIntoView({ behavior: "smooth", block: "start" }), 100);
};

onMounted(async () => {
  await loadAllData();
  await loadRecommendationData();
  await scrollToRequestedSection();
  refreshInterval = setInterval(checkLatestMonitoring, 2000);
  recommendationRefreshInterval = setInterval(loadRecommendationData, 5000);
});
onBeforeUnmount(() => {
  if (refreshInterval) clearInterval(refreshInterval);
  if (recommendationRefreshInterval) clearInterval(recommendationRefreshInterval);
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
        <span class="inline-flex items-center gap-2 rounded-full border border-emerald-100 bg-white px-3 py-1.5 text-xs font-semibold text-emerald-700 shadow-sm"><span class="h-2 w-2 rounded-full bg-emerald-500"></span>Data simulasi</span>
      </div>
      <DashboardStatGrid :monitoring="monitoring" />
    </section>

    <section class="grid grid-cols-1 items-stretch gap-5 2xl:grid-cols-[minmax(0,1.7fr)_minmax(300px,0.8fr)]">
      <div class="min-w-0 h-full"><MonitoringChartCard :data="history" /></div>
      <div v-if="monitoring" class="min-w-0 h-full"><NutrientStatusCard :monitoring="monitoring" /></div>
    </section>

    <section v-if="history.length" class="min-w-0">
      <PHTrendCard :data="history" />
    </section>

    <section v-if="monitoring" class="min-w-0">
      <MonitoringInsight :monitoring="monitoring" :summary="summary" />
    </section>

    <RecommendationAnalytics :recommendations="recommendations" />

  </div>
</template>

<style scoped>
.dashboard-page { animation: dashboard-enter 420ms ease both; }
@keyframes dashboard-enter { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
@media (prefers-reduced-motion: reduce) { .dashboard-page { animation: none; } }
</style>