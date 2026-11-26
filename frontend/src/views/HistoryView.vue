<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import {
  CheckCircle2,
  CircleAlert,
  History as HistoryIcon,
  LoaderCircle,
  X
} from "lucide-vue-next";

import MonitoringTableCard from "../components/dashboard/MonitoringTableCard.vue";
import RecommendationHistoryTable from "../components/recommendation/RecommendationHistoryTable.vue";
import { getMonitoringHistory } from "../services/monitoringService";
import { getDashboardSummary } from "../services/dashboardService";
import {
  getRecommendationHistory,
  deleteRecommendation
} from "../services/recommendationService";

const route = useRoute();

const monitoringHistory = ref([]);
const recommendationHistory = ref([]);
const totalRecommendationCount = ref(null);
const activeTab = ref(
  route.hash === "#recommendation-history" ? "recommendations" : "monitoring"
);
const pageLoading = ref(true);
const refreshingMonitoring = ref(false);
const loadWarning = ref("");
const actionError = ref("");
const deletingId = ref(null);
const selectedDeleteItem = ref(null);
const showDeleteConfirm = ref(false);
const showDeleteSuccessDialog = ref(false);
const cancelDeleteButton = ref(null);

const activeTabLabel = computed(() =>
  activeTab.value === "monitoring" ? "Riwayat Monitoring" : "Riwayat Rekomendasi"
);

let monitoringRefreshInterval = null;

const loadHistory = async () => {
  pageLoading.value = true;
  loadWarning.value = "";

  const [monitoringResult, recommendationResult, summaryResult] = await Promise.allSettled([
    getMonitoringHistory(),
    getRecommendationHistory(10),
    getDashboardSummary()
  ]);

  const failedSources = [];

  if (monitoringResult.status === "fulfilled") {
    monitoringHistory.value = Array.isArray(monitoringResult.value)
      ? monitoringResult.value
      : [];
  } else {
    console.error("Gagal memuat riwayat monitoring:", monitoringResult.reason);
    failedSources.push("riwayat monitoring");
  }

  if (recommendationResult.status === "fulfilled") {
    recommendationHistory.value = Array.isArray(recommendationResult.value)
      ? recommendationResult.value
      : [];
  } else {
    console.error("Gagal memuat riwayat rekomendasi:", recommendationResult.reason);
    failedSources.push("riwayat rekomendasi");
  }

  if (summaryResult.status === "fulfilled") {
    const total = Number(summaryResult.value?.total_recommendation);
    totalRecommendationCount.value = Number.isFinite(total) ? total : null;
  } else {
    totalRecommendationCount.value = null;
    console.error("Gagal memuat jumlah total rekomendasi:", summaryResult.reason);
  }

  if (failedSources.length) {
    loadWarning.value =
      "Sebagian data belum dapat dimuat: " +
      failedSources.join(", ") +
      ". Periksa koneksi server dan muat ulang halaman.";
  }

  pageLoading.value = false;
};

const refreshMonitoringHistory = async () => {
  if (refreshingMonitoring.value || pageLoading.value) return;
  refreshingMonitoring.value = true;
  try {
    const records = await getMonitoringHistory();
    monitoringHistory.value = Array.isArray(records) ? records : [];
  } catch (error) {
    console.error("Gagal memperbarui riwayat monitoring:", error);
  } finally {
    refreshingMonitoring.value = false;
  }
};

const requestDeleteRecommendation = async (item) => {
  if (!item?.id || deletingId.value !== null) return;
  selectedDeleteItem.value = item;
  actionError.value = "";
  showDeleteConfirm.value = true;
  await nextTick();
  cancelDeleteButton.value?.focus();
};

const closeDeleteConfirmation = () => {
  showDeleteConfirm.value = false;
  selectedDeleteItem.value = null;
};

const removeRecommendation = async () => {
  const item = selectedDeleteItem.value;
  if (!item?.id || deletingId.value !== null) return;

  showDeleteConfirm.value = false;
  deletingId.value = item.id;
  actionError.value = "";

  try {
    await deleteRecommendation(item.id);
    recommendationHistory.value = recommendationHistory.value.filter(
      (row) => row.id !== item.id
    );
    if (totalRecommendationCount.value !== null) {
      totalRecommendationCount.value = Math.max(0, totalRecommendationCount.value - 1);
    }
    try {
      const latestRecords = await getRecommendationHistory(10);
      recommendationHistory.value = Array.isArray(latestRecords) ? latestRecords : [];
    } catch (refreshError) {
      console.error("Gagal mengisi ulang 10 rekomendasi terbaru:", refreshError);
    }
    showDeleteSuccessDialog.value = true;
  } catch (error) {
    console.error("Gagal menghapus rekomendasi:", error);
    actionError.value =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      "Terjadi kesalahan saat menghapus rekomendasi. Silakan coba kembali.";
  } finally {
    deletingId.value = null;
    selectedDeleteItem.value = null;
  }
};

const scrollToRequestedHistory = async () => {
  if (!route.hash) return;
  if (route.hash === "#recommendation-history") {
    activeTab.value = "recommendations";
  } else if (route.hash === "#monitoring-history") {
    activeTab.value = "monitoring";
  }
  await nextTick();
  window.setTimeout(() => {
    document.querySelector(route.hash)?.scrollIntoView({
      behavior: "smooth",
      block: "start"
    });
  }, 120);
};

onMounted(async () => {
  await loadHistory();
  await scrollToRequestedHistory();
  monitoringRefreshInterval = window.setInterval(refreshMonitoringHistory, 5000);
});

onBeforeUnmount(() => {
  if (monitoringRefreshInterval) {
    window.clearInterval(monitoringRefreshInterval);
  }
});
</script>

<template>
  <div class="history-page mx-auto w-full min-w-0 max-w-[1360px] space-y-6 sm:space-y-7">
    <section class="relative isolate overflow-hidden rounded-[1.75rem] border border-emerald-200/80 bg-gradient-to-br from-emerald-50/95 via-white to-emerald-100/75 shadow-[0_16px_42px_-28px_rgba(5,100,70,.38)]">
      <div class="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-emerald-700 via-emerald-500 to-lime-400"></div>
      <div class="absolute inset-y-0 right-0 -z-10 w-3/5 bg-gradient-to-l from-emerald-100/70 via-emerald-50/40 to-transparent"></div>
      <div class="absolute -right-12 -top-24 -z-10 h-64 w-64 rounded-full bg-emerald-200/55 blur-3xl"></div>
      <div class="absolute -bottom-24 left-1/3 -z-10 h-48 w-48 rounded-full bg-lime-100/50 blur-3xl"></div>
      <div class="p-6 sm:p-8 lg:p-9">
        <div class="max-w-3xl">
          <div class="inline-flex items-center gap-2 rounded-full border border-emerald-100 bg-emerald-50 px-3 py-1.5 text-[10px] font-extrabold uppercase tracking-[0.16em] text-emerald-800">
            <HistoryIcon class="h-3.5 w-3.5" />
            Pusat data tersimpan
          </div>
          <h1 class="mt-4 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">
            Riwayat
          </h1>
          <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
            Telusuri catatan kondisi tanah dan hasil rekomendasi pemupukan yang telah tersimpan.
          </p>
        </div>
      </div>
    </section>

    <div
      v-if="loadWarning"
      class="flex items-start gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-amber-800"
      role="status"
      aria-live="polite"
    >
      <CircleAlert class="mt-0.5 h-5 w-5 shrink-0 text-amber-600" />
      <p class="min-w-0 flex-1 text-sm leading-relaxed">{{ loadWarning }}</p>
      <button
        type="button"
        class="rounded-lg p-1 text-amber-700 transition hover:bg-amber-100"
        aria-label="Tutup pemberitahuan"
        @click="loadWarning = ''"
      >
        <X class="h-4 w-4" />
      </button>
    </div>

    <div
      v-if="actionError"
      class="flex items-start gap-3 rounded-xl border border-rose-200 bg-rose-50 p-4 text-rose-800"
      role="alert"
      aria-live="assertive"
    >
      <CircleAlert class="mt-0.5 h-5 w-5 shrink-0 text-rose-600" />
      <p class="min-w-0 flex-1 text-sm leading-relaxed">{{ actionError }}</p>
      <button
        type="button"
        class="rounded-lg p-1 text-rose-700 transition hover:bg-rose-100"
        aria-label="Tutup pesan kesalahan"
        @click="actionError = ''"
      >
        <X class="h-4 w-4" />
      </button>
    </div>

    <div class="px-1">
      <h2 class="text-sm font-extrabold tracking-tight text-slate-800">Kategori riwayat</h2>
      <p class="mt-0.5 text-xs text-slate-500">Pilih catatan yang ingin ditinjau.</p>
    </div>

    <section class="border-b border-slate-200">
      <div class="flex flex-wrap items-end gap-1">
        <button
          type="button"
          class="relative flex min-h-14 w-full min-w-0 items-center rounded-t-xl rounded-b-none border border-b-0 px-5 py-3 text-left transition-colors focus-visible:z-20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 sm:w-auto sm:min-w-[190px]"
          :class="activeTab === 'monitoring'
            ? 'z-10 border-slate-200 bg-white text-emerald-900 shadow-[0_1px_0_0_white]'
            : 'border-transparent bg-slate-100 text-slate-600 hover:bg-slate-200/80 hover:text-emerald-800'"
          :aria-pressed="activeTab === 'monitoring'"
          @click="activeTab = 'monitoring'"
        >
          <span class="min-w-0">
            <span class="block text-sm font-bold">Riwayat Monitoring</span>
            <span class="mt-0.5 block text-[11px]" :class="activeTab === 'monitoring' ? 'text-emerald-700/75' : 'text-slate-400'">Catatan kondisi tanah</span>
          </span>
        </button>

        <button
          type="button"
          class="relative flex min-h-14 w-full min-w-0 items-center rounded-t-xl rounded-b-none border border-b-0 px-5 py-3 text-left transition-colors focus-visible:z-20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 sm:w-auto sm:min-w-[190px]"
          :class="activeTab === 'recommendations'
            ? 'z-10 border-slate-200 bg-white text-emerald-900 shadow-[0_1px_0_0_white]'
            : 'border-transparent bg-slate-100 text-slate-600 hover:bg-slate-200/80 hover:text-emerald-800'"
          :aria-pressed="activeTab === 'recommendations'"
          @click="activeTab = 'recommendations'"
        >
          <span class="min-w-0">
            <span class="block text-sm font-bold">Riwayat Rekomendasi</span>
            <span class="mt-0.5 block text-[11px]" :class="activeTab === 'recommendations' ? 'text-emerald-700/75' : 'text-slate-400'">Hasil rekomendasi pemupukan</span>
          </span>
        </button>
      </div>
    </section>

    <div
      v-if="pageLoading"
      class="flex min-h-64 flex-col items-center justify-center rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm"
      role="status"
      aria-live="polite"
    >
      <span class="flex h-12 w-12 items-center justify-center rounded-full bg-emerald-50 text-emerald-700">
        <LoaderCircle class="h-6 w-6 animate-spin" />
      </span>
      <p class="mt-4 text-sm font-bold text-slate-800">Memuat data riwayat</p>
      <p class="mt-1 text-xs text-slate-500">Mengambil catatan monitoring dan rekomendasi.</p>
    </div>

    <template v-else>
      <section
        id="monitoring-history"
        v-show="activeTab === 'monitoring'"
        class="scroll-mt-24"
      >
        <MonitoringTableCard :data="monitoringHistory" />
      </section>

      <section v-show="activeTab === 'recommendations'">
        <RecommendationHistoryTable
          :recommendations="recommendationHistory"
          :total-count="totalRecommendationCount"
          :deleting-id="deletingId"
          @delete="requestDeleteRecommendation"
        />
      </section>

      <p class="text-center text-[11px] text-slate-400">
        Menampilkan {{ activeTabLabel.toLowerCase() }} · Data monitoring diperbarui otomatis saat halaman terbuka.
      </p>
    </template>
  </div>


  <Teleport to="body">
    <div
      v-if="showDeleteConfirm"
      class="fixed inset-0 z-[100] flex items-center justify-center bg-slate-900/40 px-4 backdrop-blur-[2px]"
      role="presentation"
      @click.self="closeDeleteConfirmation"
      @keydown.esc.stop.prevent="closeDeleteConfirmation"
    >
      <section
        class="w-full max-w-sm rounded-2xl bg-white p-6 shadow-2xl ring-1 ring-slate-900/5"
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-dialog-title"
        aria-describedby="delete-dialog-description"
        @click.stop
      >
        <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-rose-50 text-rose-600">
          <CircleAlert class="h-6 w-6" />
        </div>
        <div class="mt-4 text-center">
          <h2 id="delete-dialog-title" class="text-lg font-semibold text-slate-800">Konfirmasi Hapus</h2>
          <p id="delete-dialog-description" class="mt-2 text-sm leading-6 text-slate-500">
            Apakah Anda yakin ingin menghapus seluruh paket rekomendasi untuk fase
            <strong>{{ selectedDeleteItem?.fase || "-" }}</strong>?
            Semua rincian pupuk pada paket ini akan ikut dihapus dan tidak dapat dikembalikan.
          </p>
        </div>
        <div class="mt-6 flex items-center justify-end gap-3">
          <button
            ref="cancelDeleteButton"
            type="button"
            @click="closeDeleteConfirmation"
            class="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-300 focus-visible:ring-offset-2"
          >Batal</button>
          <button
            type="button"
            :disabled="deletingId !== null"
            @click="removeRecommendation"
            class="rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-rose-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-300 focus-visible:ring-offset-2 disabled:cursor-wait disabled:opacity-60"
          >Hapus</button>
        </div>
      </section>
    </div>
  </Teleport>

  <Teleport to="body">
    <div
      v-if="showDeleteSuccessDialog"
      class="fixed inset-0 z-[110] flex items-center justify-center bg-slate-900/40 px-4 backdrop-blur-[2px]"
      role="presentation"
      @click.self="showDeleteSuccessDialog = false"
      @keydown.esc.stop.prevent="showDeleteSuccessDialog = false"
    >
      <section
        class="w-full max-w-sm rounded-2xl bg-white p-6 shadow-2xl ring-1 ring-slate-900/5"
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-success-title"
        aria-describedby="delete-success-description"
      >
        <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-50 text-green-600">
          <CheckCircle2 class="h-6 w-6" />
        </div>
        <div class="mt-4 text-center">
          <h2 id="delete-success-title" class="text-lg font-semibold text-slate-800">Data berhasil dihapus</h2>
          <p id="delete-success-description" class="mt-2 text-sm leading-6 text-slate-500">
            Data riwayat rekomendasi telah berhasil dihapus dari sistem.
          </p>
        </div>
        <div class="mt-6 flex justify-center">
          <button
            type="button"
            autofocus
            @click="showDeleteSuccessDialog = false"
            class="min-w-24 rounded-xl bg-green-600 px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-green-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-green-300 focus-visible:ring-offset-2"
          >OK</button>
        </div>
      </section>
    </div>
  </Teleport>
</template>

<style scoped>
.history-page {
  animation: history-page-enter 420ms ease both;
}

@keyframes history-page-enter {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
  .history-page { animation: none; }
}
</style>
