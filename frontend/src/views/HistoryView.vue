<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import {
  Activity,
  CheckCircle2,
  CircleAlert,
  ClipboardList,
  Trash2,
  Database,
  History as HistoryIcon,
  LoaderCircle,
  X
} from "lucide-vue-next";

import MonitoringTableCard from "../components/dashboard/MonitoringTableCard.vue";
import RecommendationHistoryTable from "../components/recommendation/RecommendationHistoryTable.vue";
import { getMonitoringHistory, deleteAllMonitoringHistory } from "../services/monitoringService";
import {
  getRecommendationHistory,
  deleteRecommendation
} from "../services/recommendationService";

const route = useRoute();

const monitoringHistory = ref([]);
const recommendationHistory = ref([]);
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
const deleteSuccessMessage = ref("");
const deletingAllMonitoring = ref(false);
const showDeleteMonitoringConfirm = ref(false);
const cancelDeleteButton = ref(null);

const totalMonitoring = computed(() => monitoringHistory.value.length);
const totalRecommendations = computed(() => recommendationHistory.value.length);
const activeTabLabel = computed(() =>
  activeTab.value === "monitoring" ? "Riwayat Monitoring" : "Riwayat Rekomendasi"
);

let monitoringRefreshInterval = null;

const loadHistory = async () => {
  pageLoading.value = true;
  loadWarning.value = "";

  const [monitoringResult, recommendationResult] = await Promise.allSettled([
    getMonitoringHistory(),
    getRecommendationHistory()
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

  if (failedSources.length) {
    loadWarning.value =
      "Sebagian data belum dapat dimuat: " +
      failedSources.join(", ") +
      ". Periksa koneksi server dan muat ulang halaman.";
  }

  pageLoading.value = false;
};

const refreshMonitoringHistory = async () => {
  if (refreshingMonitoring.value || pageLoading.value || deletingAllMonitoring.value) return;
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

const requestDeleteAllMonitoring = () => {
  if (deletingAllMonitoring.value || totalMonitoring.value === 0) return;
  actionError.value = "";
  showDeleteMonitoringConfirm.value = true;
};

const confirmDeleteAllMonitoring = async () => {
  if (deletingAllMonitoring.value || totalMonitoring.value === 0) return;

  const countBeforeDelete = totalMonitoring.value;
  deletingAllMonitoring.value = true;
  actionError.value = "";

  try {
    const response = await deleteAllMonitoringHistory();
    const deletedCount = Number(response?.deleted_count ?? countBeforeDelete);

    monitoringHistory.value = [];
    showDeleteMonitoringConfirm.value = false;
    deleteSuccessMessage.value = deletedCount > 0
      ? `${deletedCount} data riwayat monitoring berhasil dihapus. Riwayat rekomendasi tetap tersimpan.`
      : "Tidak ada data riwayat monitoring yang perlu dihapus.";
    showDeleteSuccessDialog.value = true;
  } catch (error) {
    console.error("Gagal menghapus seluruh riwayat monitoring:", error);
    showDeleteMonitoringConfirm.value = false;
    actionError.value =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      "Seluruh riwayat monitoring gagal dihapus. Silakan coba kembali.";
  } finally {
    deletingAllMonitoring.value = false;
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
    deleteSuccessMessage.value = "Data riwayat rekomendasi berhasil dihapus.";
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
  <div class="history-page space-y-6 sm:space-y-7">
    <section class="relative isolate overflow-hidden rounded-[1.75rem] border border-emerald-100 bg-white shadow-[0_14px_38px_-28px_rgba(15,65,48,.34)]">
      <div class="absolute inset-y-0 right-0 -z-10 w-1/2 bg-gradient-to-l from-emerald-50/90 to-transparent"></div>
      <div class="absolute -right-12 -top-24 -z-10 h-64 w-64 rounded-full bg-emerald-100/60 blur-3xl"></div>
      <div class="flex flex-col gap-5 p-6 sm:p-8 lg:flex-row lg:items-center lg:justify-between">
        <div class="max-w-2xl">
          <div class="inline-flex items-center gap-2 rounded-full border border-emerald-100 bg-emerald-50 px-3 py-1.5 text-[10px] font-extrabold uppercase tracking-[0.16em] text-emerald-800">
            <HistoryIcon class="h-3.5 w-3.5" />
            Pusat data tersimpan
          </div>
          <h1 class="mt-4 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">
            Riwayat
          </h1>
          <p class="mt-2 max-w-xl text-sm leading-6 text-slate-500 sm:text-base">
            Telusuri catatan kondisi tanah dan hasil rekomendasi pemupukan yang telah tersimpan.
          </p>
        </div>
        <div class="flex items-center gap-3 rounded-2xl border border-emerald-100 bg-white/90 p-3 shadow-sm sm:min-w-56">
          <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-emerald-700 text-white shadow-sm shadow-emerald-900/15">
            <Database class="h-5 w-5" />
          </div>
          <div class="min-w-0">
            <p class="text-xs font-semibold text-slate-500">Penyimpanan data</p>
            <p class="mt-0.5 text-sm font-extrabold text-slate-800">Riwayat sistem</p>
            <p class="mt-0.5 text-[10px] font-medium text-emerald-700">Monitoring & rekomendasi</p>
          </div>
        </div>
      </div>
    </section>

    <section class="grid grid-cols-1 gap-3 sm:grid-cols-2">
      <div class="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm shadow-slate-900/[0.02]">
        <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700">
          <Activity class="h-5 w-5" />
        </div>
        <div class="min-w-0">
          <p class="text-xs font-semibold text-slate-500">Total data monitoring</p>
          <p class="mt-0.5 text-2xl font-extrabold tabular-nums tracking-tight text-slate-900">{{ totalMonitoring }}</p>
        </div>
        <span class="ml-auto text-[10px] font-semibold text-slate-400">Catatan tanah</span>
      </div>
      <div class="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm shadow-slate-900/[0.02]">
        <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-lime-50 text-lime-700">
          <ClipboardList class="h-5 w-5" />
        </div>
        <div class="min-w-0">
          <p class="text-xs font-semibold text-slate-500">Total rekomendasi</p>
          <p class="mt-0.5 text-2xl font-extrabold tabular-nums tracking-tight text-slate-900">{{ totalRecommendations }}</p>
        </div>
        <span class="ml-auto text-[10px] font-semibold text-slate-400">Hasil pemupukan</span>
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

    <section class="rounded-2xl border border-slate-200 bg-white p-2 shadow-sm">
      <div class="flex flex-col gap-2 sm:flex-row">
        <button
          type="button"
          class="flex min-h-12 flex-1 items-center justify-between gap-3 rounded-xl px-4 py-2.5 text-left transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2"
          :class="activeTab === 'monitoring'
            ? 'bg-emerald-800 text-white shadow-sm'
            : 'text-slate-600 hover:bg-emerald-50 hover:text-emerald-800'"
          :aria-pressed="activeTab === 'monitoring'"
          @click="activeTab = 'monitoring'"
        >
          <span class="flex min-w-0 items-center gap-3">
            <span
              class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg"
              :class="activeTab === 'monitoring' ? 'bg-white/15 text-white' : 'bg-emerald-50 text-emerald-700'"
            >
              <Activity class="h-[18px] w-[18px]" />
            </span>
            <span class="min-w-0">
              <span class="block text-sm font-bold">Riwayat Monitoring</span>
              <span class="mt-0.5 block text-[10px]" :class="activeTab === 'monitoring' ? 'text-emerald-100/75' : 'text-slate-400'">Catatan kondisi tanah</span>
            </span>
          </span>
          <span
            class="rounded-full px-2.5 py-1 text-xs font-extrabold tabular-nums"
            :class="activeTab === 'monitoring' ? 'bg-white/15 text-white' : 'bg-slate-100 text-slate-600'"
          >{{ totalMonitoring }}</span>
        </button>

        <button
          type="button"
          class="flex min-h-12 flex-1 items-center justify-between gap-3 rounded-xl px-4 py-2.5 text-left transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2"
          :class="activeTab === 'recommendations'
            ? 'bg-emerald-800 text-white shadow-sm'
            : 'text-slate-600 hover:bg-emerald-50 hover:text-emerald-800'"
          :aria-pressed="activeTab === 'recommendations'"
          @click="activeTab = 'recommendations'"
        >
          <span class="flex min-w-0 items-center gap-3">
            <span
              class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg"
              :class="activeTab === 'recommendations' ? 'bg-white/15 text-white' : 'bg-lime-50 text-lime-700'"
            >
              <ClipboardList class="h-4.5 w-4.5" />
            </span>
            <span class="min-w-0">
              <span class="block text-sm font-bold">Riwayat Rekomendasi</span>
              <span class="mt-0.5 block text-[10px]" :class="activeTab === 'recommendations' ? 'text-emerald-100/75' : 'text-slate-400'">Hasil rekomendasi pemupukan</span>
            </span>
          </span>
          <span
            class="rounded-full px-2.5 py-1 text-xs font-extrabold tabular-nums"
            :class="activeTab === 'recommendations' ? 'bg-white/15 text-white' : 'bg-slate-100 text-slate-600'"
          >{{ totalRecommendations }}</span>
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
        <MonitoringTableCard
          :data="monitoringHistory"
          :deleting-all="deletingAllMonitoring"
          @delete-all="requestDeleteAllMonitoring"
        />
      </section>

      <section v-show="activeTab === 'recommendations'">
        <RecommendationHistoryTable
          :recommendations="recommendationHistory"
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
      v-if="showDeleteMonitoringConfirm"
      class="fixed inset-0 z-[120] flex items-center justify-center bg-slate-950/45 px-4 py-6 backdrop-blur-[3px]"
      role="presentation"
      @click.self="!deletingAllMonitoring && (showDeleteMonitoringConfirm = false)"
      @keydown.esc.stop.prevent="!deletingAllMonitoring && (showDeleteMonitoringConfirm = false)"
    >
      <section
        class="w-full max-w-md overflow-hidden rounded-2xl bg-white shadow-2xl ring-1 ring-slate-900/10"
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="clear-monitoring-title"
        aria-describedby="clear-monitoring-description"
        @click.stop
      >
        <div class="border-b border-rose-100 bg-gradient-to-br from-rose-50 via-white to-amber-50/70 px-6 pb-5 pt-6">
          <div class="flex items-start gap-4">
            <span class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-rose-100 text-rose-700 ring-1 ring-rose-200/70">
              <Trash2 class="h-5 w-5" />
            </span>
            <div class="min-w-0 flex-1">
              <p class="text-[10px] font-extrabold uppercase tracking-[0.16em] text-rose-700">Tindakan permanen</p>
              <h2 id="clear-monitoring-title" class="mt-1 text-lg font-extrabold tracking-tight text-slate-900">
                Hapus seluruh riwayat monitoring?
              </h2>
              <p id="clear-monitoring-description" class="mt-1.5 text-sm leading-6 text-slate-600">
                Anda akan menghapus <strong class="text-slate-900">{{ totalMonitoring }} catatan monitoring</strong> milik akun ini. Data yang dihapus tidak dapat dipulihkan.
              </p>
            </div>
          </div>
        </div>

        <div class="space-y-3 px-6 py-5">
          <div class="flex items-start gap-2.5 rounded-xl border border-amber-200 bg-amber-50 px-3.5 py-3">
            <CircleAlert class="mt-0.5 h-4 w-4 shrink-0 text-amber-700" />
            <p class="text-xs leading-5 text-amber-900">
              Riwayat rekomendasi tetap tersimpan. Namun, nilai N, P, K, pH, suhu, kelembapan, dan curah hujan dari monitoring yang dihapus tidak lagi tersedia pada detail riwayat rekomendasi.
            </p>
          </div>
          <p class="text-xs leading-5 text-slate-500">
            Pastikan simulasi sudah dihentikan sebelum melanjutkan. Penghapusan akan ditolak jika masih ada sesi simulasi yang berjalan.
          </p>
        </div>

        <div class="flex flex-col-reverse gap-2 border-t border-slate-100 bg-slate-50/70 px-6 py-4 sm:flex-row sm:justify-end">
          <button
            type="button"
            :disabled="deletingAllMonitoring"
            @click="showDeleteMonitoringConfirm = false"
            class="inline-flex min-h-10 items-center justify-center rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-300 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Batal
          </button>
          <button
            type="button"
            :disabled="deletingAllMonitoring"
            @click="confirmDeleteAllMonitoring"
            class="inline-flex min-h-10 items-center justify-center gap-2 rounded-xl bg-rose-600 px-4 py-2 text-sm font-bold text-white shadow-sm transition hover:bg-rose-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-400 focus-visible:ring-offset-2 disabled:cursor-wait disabled:opacity-60"
          >
            <LoaderCircle v-if="deletingAllMonitoring" class="h-4 w-4 animate-spin" />
            <Trash2 v-else class="h-4 w-4" />
            {{ deletingAllMonitoring ? "Menghapus data..." : "Ya, hapus seluruh data" }}
          </button>
        </div>
      </section>
    </div>
  </Teleport>

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
            Apakah Anda yakin ingin menghapus rekomendasi untuk fase
            <strong>{{ selectedDeleteItem?.fase || "-" }}</strong> dengan pupuk
            <strong>{{ selectedDeleteItem?.jenis_pupuk || "-" }}</strong>?
            Data yang dihapus tidak dapat dikembalikan.
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
            {{ deleteSuccessMessage }}
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
