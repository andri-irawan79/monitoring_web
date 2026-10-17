<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

import {
  getLatestMonitoring,
  getMonitoringHistory,
} from "../services/monitoringService";

import DashboardStatGrid from "../components/dashboard/DashboardStatGrid.vue";
import MonitoringChartCard from "../components/dashboard/MonitoringChartCard.vue";
import NutrientStatusCard from "../components/dashboard/NutrientStatusCard.vue";
import MonitoringTableCard from "../components/dashboard/MonitoringTableCard.vue";
import DashboardHero from "../components/dashboard/DashboardHero.vue";
import MonitoringInsight from "../components/dashboard/MonitoringInsight.vue";

import { getDashboardSummary } from "../services/dashboardService";

const monitoring = ref(null);
const history = ref([]);
const summary = ref({});

// Menyimpan ID monitoring terakhir
const lastMonitoringId = ref(null);

// Menyimpan waktu update terakhir
const lastUpdate = ref("");

let refreshInterval = null;

// Format waktu Indonesia
const updateTimestamp = () => {
  lastUpdate.value = new Date().toLocaleTimeString("id-ID");
};

// Load seluruh data dashboard
const loadAllData = async () => {
  try {
    monitoring.value = await getLatestMonitoring();
    history.value = await getMonitoringHistory();
    summary.value = await getDashboardSummary();

    lastMonitoringId.value = monitoring.value?.id ?? null;

    updateTimestamp();
  } catch (error) {
    console.error("Gagal memuat dashboard:", error);
  }
};

// Mengecek apakah ada data baru
const checkLatestMonitoring = async () => {
  try {
    const latest = await getLatestMonitoring();

    if (!latest) return;

    if (latest.id !== lastMonitoringId.value) {
      console.log("📥 Data monitoring baru ditemukan");

      monitoring.value = latest;
      history.value = await getMonitoringHistory();
      summary.value = await getDashboardSummary();

      lastMonitoringId.value = latest.id;

      updateTimestamp();
    }
  } catch (error) {
    console.error("Auto refresh gagal:", error);
  }
};

onMounted(async () => {
  await loadAllData();

  refreshInterval = setInterval(() => {
    checkLatestMonitoring();
  }, 500);
});

onBeforeUnmount(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval);
  }
});
</script>

<template>
<div>

    <DashboardHero
        :summary="summary"
    />

    <DashboardStatGrid
        v-if="monitoring"
        :monitoring="monitoring"
    />

    <div
        class="
            grid
            grid-cols-1
            xl:grid-cols-3
            gap-6
            mt-8
        "
    >

        <div class="xl:col-span-2">

            <MonitoringChartCard
                :data="history"
            />

        </div>

        <div>

            <NutrientStatusCard
                v-if="monitoring"
                :monitoring="monitoring"
            />

            <MonitoringInsight
                v-if="monitoring"
                :monitoring="monitoring"
                :summary="summary"
            />

        </div>

    </div>

    <div class="mt-8">

        <MonitoringTableCard
            :data="history"
        />

    </div>

</div>
</template>
