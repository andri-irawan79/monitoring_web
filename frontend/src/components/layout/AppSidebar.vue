<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import {
  LayoutDashboard,
  FlaskConical,
  Info,
  ChevronRight,
  Play,
  Square,
  Terminal,
  Globe,
  LoaderCircle
} from "lucide-vue-next";
import { RouterLink, useRoute } from "vue-router";
import {
  getSimulatorStatus,
  getSimulationSessionStatus,
  startWebsiteSimulation,
  stopWebsiteSimulation
} from "../../services/monitoringService";

defineProps({
  mobileOpen: { type: Boolean, default: false }
});
const emit = defineEmits(["close"]);

const route = useRoute();

const simulatorStatus = ref({ active: false, last_received_at: null });
const simulatorSessionStatus = ref({ active: false, session: null });
const simulatorStatusUnavailable = ref(false);
const simulatorStatusLoading = ref(false);
const simulatorActionLoading = ref(false);
const simulatorActionError = ref("");
const simulatorMode = ref("website");
let simulatorStatusInterval = null;

const currentSession = computed(
  () => simulatorSessionStatus.value.session || null
);
const hasActiveSession = computed(
  () => Boolean(simulatorSessionStatus.value.active)
);
const websiteSessionCanStop = computed(
  () => hasActiveSession.value
    && currentSession.value?.mode === "website"
    && currentSession.value?.can_stop_from_website
);
const terminalSessionActive = computed(
  () => hasActiveSession.value && currentSession.value?.mode === "terminal"
);
const sessionProgress = computed(() => {
  const session = currentSession.value;
  if (!session) return 0;
  const target = Math.max(1, Number(session.target_count || 365));
  const received = Math.max(0, Number(session.received_count || 0));
  return Math.min(100, Math.round((received / target) * 100));
});
const sessionProgressLabel = computed(() => {
  const session = currentSession.value;
  if (!session) return "0/365 data";
  return String(session.received_count) + "/" + String(session.target_count) + " data";
});
const sessionStatusLabel = computed(() => {
  const session = currentSession.value;
  if (!session) return "Belum ada sesi simulasi";
  const labels = {
    starting: "Menyiapkan simulator",
    running: session.mode === "website"
      ? "Berjalan dari website"
      : "Berjalan dari Git Bash",
    completed: "Simulasi selesai",
    stopped: "Simulasi dihentikan",
    failed: "Simulasi gagal"
  };
  return labels[session.status] || "Status tidak diketahui";
});
const sessionModeLabel = computed(() => {
  if (!currentSession.value) return "";
  return currentSession.value.mode === "website" ? "WEBSITE" : "GIT BASH";
});
const lastReceivedLabel = computed(() => {
  const value = currentSession.value
    ? currentSession.value.last_received_at
    : simulatorStatus.value.last_received_at;
  if (!value) {
    return currentSession.value
      ? "Menunggu record pertama pada sesi ini"
      : "Belum ada data diterima";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Waktu penerimaan tidak tersedia";
  return "Data terakhir " + date.toLocaleTimeString("id-ID");
});
const statusDotActive = computed(() => {
  if (currentSession.value) return hasActiveSession.value;
  return simulatorStatus.value.active;
});

const refreshSimulatorStatus = async () => {
  if (simulatorStatusLoading.value) return;
  simulatorStatusLoading.value = true;
  try {
    const [legacyStatus, sessionStatus] = await Promise.all([
      getSimulatorStatus(),
      getSimulationSessionStatus()
    ]);
    simulatorStatus.value = legacyStatus || {
      active: false,
      last_received_at: null
    };
    simulatorSessionStatus.value = sessionStatus || {
      active: false,
      session: null
    };
    if (sessionStatus?.active && sessionStatus.session?.mode) {
      simulatorMode.value = sessionStatus.session.mode;
    }
    simulatorStatusUnavailable.value = false;
  } catch {
    simulatorStatusUnavailable.value = true;
    simulatorStatus.value = { active: false, last_received_at: null };
    simulatorSessionStatus.value = { active: false, session: null };
  } finally {
    simulatorStatusLoading.value = false;
  }
};

const startWebsiteSession = async () => {
  if (simulatorActionLoading.value || hasActiveSession.value) return;
  simulatorActionLoading.value = true;
  simulatorActionError.value = "";
  try {
    await startWebsiteSimulation();
    simulatorMode.value = "website";
    await refreshSimulatorStatus();
  } catch (error) {
    simulatorActionError.value =
      error.response?.data?.detail || "Simulator website gagal dijalankan.";
    await refreshSimulatorStatus();
  } finally {
    simulatorActionLoading.value = false;
  }
};

const stopWebsiteSession = async () => {
  const sessionId = currentSession.value?.id;
  if (!sessionId || simulatorActionLoading.value) return;
  simulatorActionLoading.value = true;
  simulatorActionError.value = "";
  try {
    await stopWebsiteSimulation(sessionId);
    await refreshSimulatorStatus();
  } catch (error) {
    simulatorActionError.value =
      error.response?.data?.detail || "Simulator tidak berhasil dihentikan.";
    await refreshSimulatorStatus();
  } finally {
    simulatorActionLoading.value = false;
  }
};

const selectSimulatorMode = (mode) => {
  if (!hasActiveSession.value) {
    simulatorMode.value = mode;
    simulatorActionError.value = "";
  }
};

onMounted(() => {
  refreshSimulatorStatus();
  simulatorStatusInterval = window.setInterval(refreshSimulatorStatus, 2000);
});

onBeforeUnmount(() => {
  if (simulatorStatusInterval) window.clearInterval(simulatorStatusInterval);
});

const menus = [
  { name: "Dashboard", description: "Ringkasan kondisi tanah", icon: LayoutDashboard, path: "/" },
  { name: "Rekomendasi", description: "Pengolahan Fuzzy Tsukamoto", icon: FlaskConical, path: "/recommendation" }
];

</script>

<template>
  <aside
    id="app-sidebar"
    class="fixed bottom-0 left-0 top-20 z-40 flex w-72 flex-col justify-between overflow-y-auto border-r border-emerald-950/10 bg-gradient-to-b from-white via-white to-[#f5faf7] shadow-[10px_0_35px_-30px_rgba(15,65,48,.3)] transition-transform duration-300 ease-in-out lg:translate-x-0"
    :class="mobileOpen ? 'translate-x-0' : '-translate-x-full'"
    aria-label="Menu navigasi utama"
  >
    <div class="px-4 pb-5 pt-6">
      <div class="mb-7 overflow-hidden rounded-2xl border border-emerald-100 bg-gradient-to-br from-emerald-50 via-white to-lime-50/70 p-4">
        <p class="text-sm font-extrabold tracking-tight text-slate-900">Durian Montong</p>
        <div class="mt-4 flex items-center justify-between gap-2 border-t border-emerald-100 pt-3">
          <span class="text-[10px] font-semibold text-slate-500">Monitoring & pemupukan</span>
          <span class="shrink-0 rounded-full bg-white px-2 py-1 text-[9px] font-bold text-emerald-800 ring-1 ring-emerald-100">Fuzzy Tsukamoto</span>
        </div>
      </div>

      <div class="mb-3 flex items-center justify-between px-2">
        <p class="text-[10px] font-extrabold uppercase tracking-[0.18em] text-slate-400">Menu utama</p>
        <span class="text-[9px] font-bold text-slate-300">NAVIGASI</span>
      </div>

      <nav class="space-y-2" aria-label="Navigasi utama">
        <RouterLink
          v-for="menu in menus"
          :key="menu.path"
          :to="menu.path"
          class="group relative flex items-center gap-3 overflow-hidden rounded-2xl border px-3 py-3 transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2"
          :class="route.path === menu.path
            ? 'border-emerald-800 bg-gradient-to-r from-emerald-800 to-emerald-700 text-white shadow-[0_8px_18px_-13px_rgba(4,120,87,.9)]'
            : 'border-transparent text-slate-600 hover:border-emerald-100 hover:bg-emerald-50/80 hover:text-emerald-900'"
          :aria-current="route.path === menu.path ? 'page' : undefined"
          @click="emit('close')"
        >
          <span
            class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl transition-colors"
            :class="route.path === menu.path
              ? 'bg-white/15 text-white'
              : 'bg-slate-100 text-slate-500 group-hover:bg-white group-hover:text-emerald-700'"
          >
            <component :is="menu.icon" class="h-[19px] w-[19px]" />
          </span>

          <span class="min-w-0 flex-1">
            <span class="block text-sm font-bold">{{ menu.name }}</span>
            <span class="mt-0.5 block truncate text-[10px] font-medium" :class="route.path === menu.path ? 'text-emerald-100/75' : 'text-slate-400 group-hover:text-emerald-700/70'">
              {{ menu.description }}
            </span>
          </span>

          <span v-if="route.path === menu.path" class="flex shrink-0 items-center gap-1 text-[9px] font-extrabold uppercase tracking-wider text-emerald-100">
            Aktif
            <ChevronRight class="h-3.5 w-3.5" />
          </span>
          <ChevronRight v-else class="h-4 w-4 shrink-0 text-slate-300 transition-transform group-hover:translate-x-0.5 group-hover:text-emerald-600" />
        </RouterLink>
      </nav>
    </div>

    <div class="shrink-0 space-y-3 border-t border-slate-200/80 bg-white/70 p-4">
      <section
        class="rounded-2xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-3.5 shadow-sm"
        aria-live="polite"
        aria-label="Kontrol dan progres sesi simulasi"
      >
        <div class="flex items-center justify-between gap-2">
          <div class="flex min-w-0 items-center gap-2">
            <span class="relative flex h-3 w-3 shrink-0 items-center justify-center">
              <span
                v-if="statusDotActive"
                class="absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75 animate-ping"
              ></span>
              <span
                class="relative h-2.5 w-2.5 rounded-full ring-2 ring-white"
                :class="statusDotActive
                  ? 'bg-emerald-500 shadow-[0_0_0_3px_rgba(16,185,129,.12)]'
                  : currentSession?.status === 'failed'
                    ? 'bg-rose-500 shadow-[0_0_0_3px_rgba(244,63,94,.10)]'
                    : 'bg-slate-300'"
              ></span>
            </span>
            <p class="truncate text-xs font-extrabold text-slate-800">Kontrol simulasi</p>
          </div>
          <span
            v-if="sessionModeLabel"
            class="shrink-0 rounded-full bg-slate-100 px-2 py-1 text-[8px] font-extrabold tracking-wide text-slate-600"
          >
            {{ sessionModeLabel }}
          </span>
        </div>

        <p class="mt-2 text-[10px] font-bold text-slate-700">
          {{ sessionStatusLabel }}
        </p>

        <div v-if="currentSession" class="mt-3">
          <div class="mb-1.5 flex items-center justify-between gap-2 text-[10px]">
            <span class="font-semibold text-slate-500">Progres sesi</span>
            <span class="font-extrabold tabular-nums text-slate-800">
              {{ sessionProgressLabel }} · {{ sessionProgress }}%
            </span>
          </div>
          <div
            class="h-2 overflow-hidden rounded-full bg-slate-200"
            role="progressbar"
            :aria-valuenow="sessionProgress"
            aria-valuemin="0"
            aria-valuemax="100"
            aria-label="Progres sesi simulasi"
          >
            <div
              class="h-full rounded-full bg-emerald-600 transition-all duration-500"
              :style="{ width: String(sessionProgress) + '%' }"
            ></div>
          </div>
        </div>
        <p v-else class="mt-2 text-[10px] leading-4 text-slate-500">
          Setiap sesi dimulai dari 0 dan menargetkan 365 data.
        </p>

        <p class="mt-2 text-[9px] leading-4 text-slate-400">
          {{ lastReceivedLabel }} · Data CSV, bukan sensor
        </p>
        <p
          v-if="currentSession?.error_message"
          class="mt-2 rounded-lg bg-rose-50 px-2 py-1.5 text-[9px] leading-4 text-rose-700"
        >
          {{ currentSession.error_message }}
        </p>

        <div class="mt-3 grid grid-cols-2 gap-1 rounded-xl bg-slate-100 p-1">
          <button
            type="button"
            class="flex min-h-8 items-center justify-center gap-1.5 rounded-lg px-2 text-[10px] font-bold transition-colors disabled:cursor-not-allowed disabled:opacity-50"
            :class="simulatorMode === 'website'
              ? 'bg-white text-emerald-800 shadow-sm'
              : 'text-slate-500 hover:text-slate-800'"
            :disabled="hasActiveSession"
            :aria-pressed="simulatorMode === 'website'"
            @click="selectSimulatorMode('website')"
          >
            <Globe class="h-3.5 w-3.5" />
            Website
          </button>
          <button
            type="button"
            class="flex min-h-8 items-center justify-center gap-1.5 rounded-lg px-2 text-[10px] font-bold transition-colors disabled:cursor-not-allowed disabled:opacity-50"
            :class="simulatorMode === 'terminal'
              ? 'bg-white text-emerald-800 shadow-sm'
              : 'text-slate-500 hover:text-slate-800'"
            :disabled="hasActiveSession"
            :aria-pressed="simulatorMode === 'terminal'"
            @click="selectSimulatorMode('terminal')"
          >
            <Terminal class="h-3.5 w-3.5" />
            Git Bash
          </button>
        </div>

        <div v-if="simulatorMode === 'website'" class="mt-2">
          <button
            v-if="websiteSessionCanStop"
            type="button"
            class="flex min-h-9 w-full items-center justify-center gap-2 rounded-xl bg-rose-600 px-3 py-2 text-[10px] font-extrabold text-white transition-colors hover:bg-rose-700 disabled:cursor-wait disabled:opacity-60"
            :disabled="simulatorActionLoading"
            @click="stopWebsiteSession"
          >
            <LoaderCircle v-if="simulatorActionLoading" class="h-3.5 w-3.5 animate-spin" />
            <Square v-else class="h-3 w-3 fill-current" />
            Hentikan simulasi
          </button>
          <button
            v-else
            type="button"
            class="flex min-h-9 w-full items-center justify-center gap-2 rounded-xl bg-emerald-700 px-3 py-2 text-[10px] font-extrabold text-white transition-colors hover:bg-emerald-800 disabled:cursor-not-allowed disabled:opacity-60"
            :disabled="simulatorActionLoading || hasActiveSession || simulatorStatusUnavailable"
            @click="startWebsiteSession"
          >
            <LoaderCircle v-if="simulatorActionLoading" class="h-3.5 w-3.5 animate-spin" />
            <Play v-else class="h-3.5 w-3.5 fill-current" />
            Mulai dari website
          </button>
          <p
            v-if="terminalSessionActive"
            class="mt-2 text-[9px] leading-4 text-amber-700"
          >
            Sesi aktif dari Git Bash. Hentikan melalui terminal dengan Ctrl+C.
          </p>
        </div>

        <div v-else class="mt-2 rounded-xl border border-slate-200 bg-white p-2.5">
          <p class="text-[9px] font-bold leading-4 text-slate-600">
            Jalankan dari folder utama proyek:
          </p>
          <code class="mt-1 block break-all rounded-md bg-slate-900 px-2 py-1.5 text-[9px] text-emerald-100">
            python backend/simulator/simulator.py
          </code>
          <p class="mt-1.5 text-[9px] leading-4 text-slate-500">
            Masukkan email dan kata sandi akun saat diminta di terminal.
          </p>
          <p class="mt-1 text-[9px] leading-4 text-slate-500">
            Tekan Ctrl+C di Git Bash untuk menghentikan sesi.
          </p>
          <p
            v-if="terminalSessionActive"
            class="mt-1 text-[9px] font-bold text-emerald-700"
          >
            Sesi Git Bash sedang mengirim data.
          </p>
        </div>

        <p
          v-if="simulatorActionError"
          class="mt-2 rounded-lg bg-rose-50 px-2 py-1.5 text-[9px] leading-4 text-rose-700"
        >
          {{ simulatorActionError }}
        </p>
        <p
          v-if="simulatorStatusUnavailable"
          class="mt-2 text-[9px] leading-4 text-rose-700"
        >
          API tidak dapat dihubungi. Periksa server backend.
        </p>
      </section>

      <div class="flex items-center justify-between px-1 pt-1 text-[10px] text-slate-400">
        <span class="inline-flex items-center gap-1.5"><Info class="h-3.5 w-3.5" />Durian Monitor</span>
        <span class="font-semibold tabular-nums">Versi 3.0.0</span>
      </div>
    </div>
  </aside>

</template>
