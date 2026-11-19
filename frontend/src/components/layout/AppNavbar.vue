<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from "vue";
import {
  Leaf,
  LogOut,
  Menu,
  X,
  CircleAlert,
  KeyRound,
  ChevronDown,
  Mail,
  UserRound
} from "lucide-vue-next";
import { useRouter } from "vue-router";
import { currentUser } from "../../services/authState";
import { getCurrentAccount, logoutAccount } from "../../services/authService";

const props = defineProps({
  sidebarOpen: { type: Boolean, default: false }
});
const emit = defineEmits(["toggle-sidebar"]);
const router = useRouter();

const profileMenuOpen = ref(false);
const profileMenuRef = ref(null);
const showLogoutConfirm = ref(false);
const logoutButton = ref(null);
const cancelButton = ref(null);

const userName = computed(() => currentUser.value?.full_name || "Pengguna");
const userEmail = computed(() => currentUser.value?.email || "");
const userInitials = computed(() => {
  const parts = userName.value.trim().split(/\s+/).filter(Boolean).slice(0, 2);
  return parts.map(part => part[0]?.toUpperCase() || "").join("") || "P";
});

const closeProfileMenu = async (restoreFocus = false) => {
  profileMenuOpen.value = false;
  if (restoreFocus) {
    await nextTick();
    logoutButton.value?.focus();
  }
};

const toggleProfileMenu = () => {
  profileMenuOpen.value = !profileMenuOpen.value;
};

const handleOutsidePointer = (event) => {
  if (
    profileMenuOpen.value &&
    profileMenuRef.value &&
    !profileMenuRef.value.contains(event.target)
  ) {
    profileMenuOpen.value = false;
  }
};

const handleGlobalKeydown = (event) => {
  if (event.key === "Escape" && profileMenuOpen.value) {
    event.preventDefault();
    closeProfileMenu(true);
  }
};

const openLogoutConfirmation = async () => {
  profileMenuOpen.value = false;
  showLogoutConfirm.value = true;
  await nextTick();
  cancelButton.value?.focus();
};

const closeLogoutConfirmation = async () => {
  showLogoutConfirm.value = false;
  await nextTick();
  logoutButton.value?.focus();
};

const openAccountSecurity = () => {
  profileMenuOpen.value = false;
  router.push({ name: "account-security" });
};

const confirmLogout = () => {
  showLogoutConfirm.value = false;
  logoutAccount();
  router.replace("/login");
};

onMounted(async () => {
  document.addEventListener("pointerdown", handleOutsidePointer);
  document.addEventListener("keydown", handleGlobalKeydown);

  if (!currentUser.value) {
    try {
      await getCurrentAccount();
    } catch {
      // API interceptor handles invalid sessions and redirects to login.
    }
  }
});

onBeforeUnmount(() => {
  document.removeEventListener("pointerdown", handleOutsidePointer);
  document.removeEventListener("keydown", handleGlobalKeydown);
});
</script>

<template>
  <header class="fixed inset-x-0 top-0 z-50 h-20 border-b border-emerald-950/10 bg-white/95 shadow-[0_4px_24px_-18px_rgba(15,65,48,.42)] backdrop-blur-xl after:absolute after:inset-x-0 after:bottom-0 after:h-[2px] after:bg-gradient-to-r after:from-emerald-700 after:via-emerald-400 after:to-lime-300">
    <div class="mx-auto flex h-full w-full items-center justify-between gap-2 px-3 sm:gap-3 sm:px-5 lg:px-7">
      <div class="flex min-w-0 items-center gap-2 sm:gap-4">
        <button
          type="button"
          class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl sm:h-10 sm:w-10 text-slate-600 transition hover:bg-emerald-50 hover:text-emerald-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 lg:hidden"
          :aria-expanded="props.sidebarOpen"
          aria-controls="app-sidebar"
          :aria-label="props.sidebarOpen ? 'Tutup menu navigasi' : 'Buka menu navigasi'"
          @click="emit('toggle-sidebar')"
        >
          <X v-if="props.sidebarOpen" class="h-5 w-5" />
          <Menu v-else class="h-5 w-5" />
        </button>

        <div class="relative flex h-9 w-9 shrink-0 items-center justify-center overflow-hidden rounded-xl sm:h-12 sm:w-12 sm:rounded-2xl bg-gradient-to-br from-emerald-800 via-emerald-700 to-teal-600 text-white shadow-[0_5px_14px_-7px_rgba(4,120,87,.8)] ring-1 ring-emerald-900/10 sm:h-12 sm:w-12">
          <span class="absolute -right-3 -top-3 h-8 w-8 rounded-full bg-white/15"></span>
          <Leaf class="relative h-5 w-5 sm:h-7 sm:w-7" />
        </div>

        <div class="min-w-0">
          <div class="flex min-w-0 items-center gap-2">
            <h1 class="max-w-[112px] truncate text-sm font-extrabold tracking-tight text-slate-900 sm:max-w-none sm:text-lg">Durian Monitor</h1>
            <span class="hidden rounded-full border border-emerald-100 bg-emerald-50 px-2 py-0.5 text-[9px] font-extrabold uppercase tracking-[0.14em] text-emerald-800 sm:inline-flex">Simulasi</span>
          </div>
          <p class="hidden truncate text-[11px] font-medium text-slate-500 sm:block sm:text-xs">
            Monitoring kondisi tanah & rekomendasi pemupukan
          </p>
        </div>
      </div>

      <div class="flex shrink-0 items-center gap-2 sm:gap-3">
        <div class="hidden h-9 w-px bg-slate-200 md:block"></div>

        <div ref="profileMenuRef" class="relative">
          <button
            ref="logoutButton"
            type="button"
            class="group flex min-h-10 max-w-none items-center gap-2 rounded-2xl bg-transparent py-1.5 pl-1.5 pr-2 transition hover:bg-emerald-50/70 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 sm:max-w-[230px] sm:gap-2.5 sm:pl-2 sm:pr-2.5"
            :aria-expanded="profileMenuOpen"
            aria-haspopup="menu"
            aria-controls="account-profile-menu"
            :aria-label="profileMenuOpen ? 'Tutup menu akun' : 'Buka menu akun'"
            @click="toggleProfileMenu"
          >
            <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border border-emerald-300 bg-gradient-to-br from-emerald-100 to-teal-100 text-xs font-extrabold text-emerald-800 ring-1 ring-white">
              {{ userInitials }}
            </span>
            <span class="hidden min-w-0 flex-1 truncate text-left text-xs font-bold text-slate-800 sm:block sm:text-[13px]">
              {{ userName }}
            </span>
            <ChevronDown
              class="h-4 w-4 shrink-0 text-slate-500 transition-transform duration-200 group-hover:text-emerald-800"
              :class="profileMenuOpen ? 'rotate-180 text-emerald-800' : ''"
            />
          </button>

          <Transition name="profile-popover">
            <section
              v-if="profileMenuOpen"
              id="account-profile-menu"
              class="absolute right-0 top-full z-[70] mt-3 w-72 max-w-[calc(100vw-1.5rem)] origin-top-right overflow-hidden rounded-2xl border border-emerald-100/80 bg-white shadow-[0_18px_48px_-18px_rgba(15,65,48,.28)] ring-1 ring-slate-900/5 sm:w-[310px]"
              role="menu"
              aria-label="Menu akun"
              @keydown.esc.stop.prevent="closeProfileMenu(true)"
            >
              <div class="border-b border-slate-100 bg-gradient-to-br from-emerald-50/90 via-white to-lime-50/60 p-4">
                <div class="flex items-center gap-3">
                  <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-emerald-300 bg-gradient-to-br from-emerald-100 to-teal-100 text-sm font-extrabold text-emerald-800 ring-1 ring-white">
                    {{ userInitials }}
                  </div>
                  <div class="min-w-0 flex-1">
                    <p class="truncate text-sm font-extrabold text-slate-800">{{ userName }}</p>
                    <p class="mt-0.5 flex min-w-0 items-center gap-1.5 text-[11px] text-slate-500">
                      <Mail class="h-3.5 w-3.5 shrink-0 text-emerald-600" />
                      <span class="truncate">{{ userEmail || "Email belum tersedia" }}</span>
                    </p>
                  </div>
                </div>
                <div class="mt-3 inline-flex items-center gap-1.5 rounded-full border border-emerald-100 bg-white/80 px-2.5 py-1 text-[9px] font-bold uppercase tracking-wider text-emerald-800">
                  <UserRound class="h-3 w-3" />
                  Akun pengguna
                </div>
              </div>

              <div class="space-y-1 p-2.5">
                <button
                  type="button"
                  role="menuitem"
                  class="flex min-h-11 w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-xs font-semibold text-slate-700 transition hover:bg-emerald-50 hover:text-emerald-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500"
                  @click="openAccountSecurity"
                >
                  <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700">
                    <KeyRound class="h-4 w-4" />
                  </span>
                  <span class="flex-1">Ubah kata sandi</span>
                  <ChevronDown class="h-3.5 w-3.5 -rotate-90 text-slate-300" />
                </button>

                <div class="my-1 border-t border-slate-100"></div>

                <button
                  type="button"
                  role="menuitem"
                  class="flex min-h-11 w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-xs font-semibold text-rose-600 transition hover:bg-rose-50 hover:text-rose-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-300"
                  @click="openLogoutConfirmation"
                >
                  <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-rose-50 text-rose-600">
                    <LogOut class="h-4 w-4" />
                  </span>
                  <span class="flex-1">Keluar dari akun</span>
                </button>
              </div>
              <div class="border-t border-slate-100 bg-slate-50/80 px-4 py-2.5">
                <p class="text-center text-[10px] font-medium text-slate-400">Durian Monitor · Research</p>
              </div>
            </section>
          </Transition>
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

<style scoped>
.profile-popover-enter-active,
.profile-popover-leave-active {
  transition: opacity 160ms ease, transform 160ms ease;
}

.profile-popover-enter-from,
.profile-popover-leave-to {
  opacity: 0;
  transform: translateY(-5px) scale(0.98);
}

@media (prefers-reduced-motion: reduce) {
  .profile-popover-enter-active,
  .profile-popover-leave-active {
    transition: none;
  }

  .profile-popover-enter-from,
  .profile-popover-leave-to {
    transform: none;
  }
}
</style>
