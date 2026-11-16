<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from "vue";
import {
  LayoutDashboard,
  FlaskConical,
  Database,
  Info,
  LogOut,
  CircleAlert,
  ChevronRight
} from "lucide-vue-next";
import { RouterLink, useRoute, useRouter } from "vue-router";
import { logoutAccount } from "../../services/authService";
import { getSimulatorStatus } from "../../services/monitoringService";

defineProps({
  mobileOpen: { type: Boolean, default: false }
});
const emit = defineEmits(["close"]);

const route = useRoute();
const router = useRouter();
const showLogoutConfirm = ref(false);
const logoutButton = ref(null);
const cancelButton = ref(null);
const simulatorStatus = ref({ active: false, last_received_at: null });
const simulatorStatusUnavailable = ref(false);
const simulatorStatusLoading = ref(false);
let simulatorStatusInterval = null;

const simulatorStatusLabel = computed(() => {
  if (simulatorStatusUnavailable.value) return "API tidak dapat dihubungi";
  return simulatorStatus.value.active ? "Data simulasi diterima" : "Menunggu data simulator Python";
});

const lastReceivedLabel = computed(() => {
  const value = simulatorStatus.value.last_received_at;
  if (!value) return "Belum ada data diterima";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Waktu penerimaan tidak tersedia";
  return `Terakhir diterima ${date.toLocaleTimeString("id-ID")}`;
});

const refreshSimulatorStatus = async () => {
  if (simulatorStatusLoading.value) return;
  simulatorStatusLoading.value = true;
  try {
    const status = await getSimulatorStatus();
    simulatorStatus.value = status || { active: false, last_received_at: null };
    simulatorStatusUnavailable.value = false;
  } catch (error) {
    simulatorStatusUnavailable.value = true;
    simulatorStatus.value = { active: false, last_received_at: null };
  } finally {
    simulatorStatusLoading.value = false;
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

const openLogoutConfirmation = async () => {
  showLogoutConfirm.value = true;
  await nextTick();
  cancelButton.value?.focus();
};

const closeLogoutConfirmation = async () => {
  showLogoutConfirm.value = false;
  await nextTick();
  logoutButton.value?.focus();
};

const confirmLogout = () => {
  showLogoutConfirm.value = false;
  logoutAccount();
  router.replace("/login");
};
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
        <div class="min-w-0">
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

    <div class="space-y-3 border-t border-slate-200/80 bg-white/70 p-4">
      <section
        class="rounded-2xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-3.5 shadow-sm"
        aria-live="polite"
        aria-label="Status penerimaan data simulator"
      >
        <div class="flex items-center justify-between gap-3">
          <div class="flex min-w-0 items-center gap-2.5">
            <span class="relative flex h-3 w-3 shrink-0 items-center justify-center">
              <span v-if="simulatorStatus.active" class="absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75 animate-ping"></span>
              <span
                class="relative h-2.5 w-2.5 rounded-full ring-2 ring-white"
                :class="simulatorStatus.active ? 'bg-emerald-500 shadow-[0_0_0_3px_rgba(16,185,129,.12)]' : 'bg-rose-500 shadow-[0_0_0_3px_rgba(244,63,94,.10)]'"
              ></span>
            </span>
            <div class="min-w-0">
              <p class="text-xs font-extrabold text-slate-800">Status simulasi</p>
              <p class="mt-0.5 truncate text-[10px] font-semibold" :class="simulatorStatus.active ? 'text-emerald-700' : 'text-rose-700'">
                {{ simulatorStatusLabel }}
              </p>
            </div>
          </div>
          <span
            class="shrink-0 rounded-full px-2 py-1 text-[9px] font-extrabold uppercase tracking-wide"
            :class="simulatorStatus.active ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-50 text-rose-700'"
          >
            {{ simulatorStatus.active ? "Aktif" : "Tidak aktif" }}
          </span>
        </div>
        <p class="mt-2 pl-5 text-[10px] leading-4 text-slate-500">{{ lastReceivedLabel }}</p>
      </section>

      <button
        ref="logoutButton"
        type="button"
        @click="openLogoutConfirmation"
        aria-label="Keluar dari akun"
        class="group flex min-h-11 w-full items-center gap-3 rounded-xl border border-rose-100/80 bg-rose-50/45 px-3 py-2.5 text-left text-slate-700 shadow-sm transition-all duration-200 hover:border-rose-200 hover:bg-rose-50/90 hover:text-rose-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-300 focus-visible:ring-offset-2"
      >
        <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-white text-rose-600 ring-1 ring-rose-100 transition-colors group-hover:bg-rose-100 group-hover:text-rose-700">
          <LogOut class="h-4 w-4" />
        </span>
        <span class="flex-1 text-xs font-bold">Keluar dari akun</span>
        <ChevronRight class="h-4 w-4 text-rose-300 transition-transform group-hover:translate-x-0.5 group-hover:text-rose-600" />
      </button>

      <div class="flex items-center justify-between px-1 pt-1 text-[10px] text-slate-400">
        <span class="inline-flex items-center gap-1.5"><Info class="h-3.5 w-3.5" />Durian Monitor</span>
        <span class="font-semibold tabular-nums">Versi 3.0.0</span>
      </div>
    </div>
  </aside>

  <Teleport to="body">
    <div
      v-if="showLogoutConfirm"
      class="fixed inset-0 z-[100] flex items-center justify-center bg-slate-950/40 px-4 backdrop-blur-[3px]"
      role="presentation"
      @click.self="closeLogoutConfirmation"
      @keydown.esc.stop.prevent="closeLogoutConfirmation"
    >
      <section
        class="w-full max-w-sm rounded-2xl bg-white p-6 shadow-2xl ring-1 ring-slate-900/5"
        role="dialog"
        aria-modal="true"
        aria-labelledby="logout-dialog-title"
        aria-describedby="logout-dialog-description"
        @click.stop
      >
        <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-rose-50 text-rose-600">
          <CircleAlert class="h-6 w-6" />
        </div>
        <div class="mt-4 text-center">
          <h2 id="logout-dialog-title" class="text-lg font-bold text-slate-800">Konfirmasi Keluar</h2>
          <p id="logout-dialog-description" class="mt-2 text-sm leading-6 text-slate-500">Apakah Anda yakin ingin keluar dari akun?</p>
        </div>
        <div class="mt-6 flex items-center justify-end gap-3">
          <button
            ref="cancelButton"
            type="button"
            @click="closeLogoutConfirmation"
            class="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-600 transition-colors hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-300 focus-visible:ring-offset-2"
          >
            Batal
          </button>
          <button
            type="button"
            @click="confirmLogout"
            class="rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-bold text-white transition-colors hover:bg-rose-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-300 focus-visible:ring-offset-2"
          >
            Keluar
          </button>
        </div>
      </section>
    </div>
  </Teleport>
</template>
