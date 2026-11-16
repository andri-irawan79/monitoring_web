<script setup>
import { computed, nextTick, onMounted, ref } from "vue";
import { Leaf, LogOut, Menu, X, CircleAlert } from "lucide-vue-next";
import { useRouter } from "vue-router";
import { currentUser } from "../../services/authState";
import { getCurrentAccount, logoutAccount } from "../../services/authService";

const props = defineProps({
  sidebarOpen: { type: Boolean, default: false }
});
const emit = defineEmits(["toggle-sidebar"]);
const router = useRouter();

const showLogoutConfirm = ref(false);
const logoutButton = ref(null);
const cancelButton = ref(null);

const userName = computed(() => currentUser.value?.full_name || "Pengguna");
const userEmail = computed(() => currentUser.value?.email || "");
const userInitials = computed(() => {
  const parts = userName.value.trim().split(/\s+/).filter(Boolean).slice(0, 2);
  return parts.map(part => part[0]?.toUpperCase() || "").join("") || "P";
});

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

onMounted(async () => {
  if (!currentUser.value) {
    try {
      await getCurrentAccount();
    } catch {
      // API interceptor handles invalid sessions and redirects to login.
    }
  }
});
</script>

<template>
  <header class="fixed inset-x-0 top-0 z-50 h-20 border-b border-emerald-950/10 bg-white/95 shadow-[0_4px_24px_-18px_rgba(15,65,48,.42)] backdrop-blur-xl after:absolute after:inset-x-0 after:bottom-0 after:h-[2px] after:bg-gradient-to-r after:from-emerald-700 after:via-emerald-400 after:to-lime-300">
    <div class="mx-auto flex h-full w-full items-center justify-between gap-3 px-3 sm:px-5 lg:px-7">
      <div class="flex min-w-0 items-center gap-3 sm:gap-4">
        <button
          type="button"
          class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-slate-600 transition hover:bg-emerald-50 hover:text-emerald-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 lg:hidden"
          :aria-expanded="props.sidebarOpen"
          aria-controls="app-sidebar"
          :aria-label="props.sidebarOpen ? 'Tutup menu navigasi' : 'Buka menu navigasi'"
          @click="emit('toggle-sidebar')"
        >
          <X v-if="props.sidebarOpen" class="h-5 w-5" />
          <Menu v-else class="h-5 w-5" />
        </button>

        <div class="relative flex h-11 w-11 shrink-0 items-center justify-center overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-800 via-emerald-700 to-teal-600 text-white shadow-[0_5px_14px_-7px_rgba(4,120,87,.8)] ring-1 ring-emerald-900/10 sm:h-12 sm:w-12">
          <span class="absolute -right-3 -top-3 h-8 w-8 rounded-full bg-white/15"></span>
          <Leaf class="relative h-6 w-6 sm:h-7 sm:w-7" />
        </div>

        <div class="min-w-0">
          <div class="flex min-w-0 items-center gap-2">
            <h1 class="truncate text-base font-extrabold tracking-tight text-slate-900 sm:text-lg">Durian Monitor</h1>
            <span class="hidden rounded-full border border-emerald-100 bg-emerald-50 px-2 py-0.5 text-[9px] font-extrabold uppercase tracking-[0.14em] text-emerald-800 sm:inline-flex">Research</span>
          </div>
          <p class="hidden truncate text-[11px] font-medium text-slate-500 sm:block sm:text-xs">
            Monitoring kondisi tanah & rekomendasi pemupukan
          </p>
        </div>
      </div>

      <div class="flex shrink-0 items-center gap-2 sm:gap-3">
        <div class="hidden h-9 w-px bg-slate-200 md:block"></div>
        <div class="flex min-w-0 items-center gap-2.5 rounded-2xl border border-slate-200/80 bg-slate-50/80 py-1.5 pl-1.5 pr-2 sm:gap-3 sm:pl-2 sm:pr-2.5">
          <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-100 to-teal-100 text-xs font-extrabold text-emerald-800 ring-1 ring-emerald-200/70">
            {{ userInitials }}
          </div>
          <div class="hidden min-w-0 sm:block">
            <p class="max-w-36 truncate text-xs font-bold text-slate-800 sm:max-w-44">{{ userName }}</p>
            <p class="max-w-36 truncate text-[10px] text-slate-500 sm:max-w-44">{{ userEmail || "Akun pengguna" }}</p>
          </div>
          <button
            ref="logoutButton"
            type="button"
            class="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl border border-rose-100 bg-white text-rose-600 shadow-sm transition-all hover:border-rose-200 hover:bg-rose-50 hover:text-rose-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-300 focus-visible:ring-offset-2"
            aria-label="Keluar dari akun"
            @click="openLogoutConfirmation"
          >
            <LogOut class="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  </header>

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
