<script setup>
import { onMounted } from "vue";
import { Leaf, UserCircle2, Menu, X } from "lucide-vue-next";
import { currentUser } from "../../services/authState";
import { getCurrentAccount } from "../../services/authService";

defineProps({
  sidebarOpen: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(["toggle-sidebar"]);

onMounted(async () => {
  if (!currentUser.value) {
    try {
      await getCurrentAccount();
    } catch {
      // API interceptor redirects to the login page when the session is invalid.
    }
  }
});
</script>

<template>
  <header class="fixed top-0 left-0 right-0 z-50 h-20 bg-white border-b border-slate-200 shadow-sm">
    <div class="max-w-screen-2xl mx-auto h-full px-4 sm:px-6 md:px-8 flex items-center justify-between gap-3">
      <div class="flex items-center gap-2 sm:gap-4 min-w-0">
        <button
          type="button"
          class="
            flex
            h-10
            w-10
            shrink-0
            items-center
            justify-center
            rounded-xl
            text-slate-600
            transition-colors
            hover:bg-slate-100
            focus-visible:outline-none
            focus-visible:ring-2
            focus-visible:ring-green-500
            lg:hidden
          "
          :aria-expanded="sidebarOpen"
          aria-controls="app-sidebar"
          :aria-label="sidebarOpen ? 'Tutup menu navigasi' : 'Buka menu navigasi'"
          @click="emit('toggle-sidebar')"
        >
          <X v-if="sidebarOpen" class="h-5 w-5" />
          <Menu v-else class="h-5 w-5" />
        </button>

        <div class="flex h-10 w-10 sm:h-12 sm:w-12 shrink-0 items-center justify-center rounded-xl bg-green-100">
          <Leaf class="h-6 w-6 sm:h-7 sm:w-7 text-green-700" />
        </div>

        <div class="min-w-0">
          <h1 class="truncate text-sm sm:text-lg md:text-2xl font-bold text-slate-800">
            DASHBOARD MONITORING DURIAN
          </h1>
          <p class="hidden xs:block truncate text-[10px] sm:text-xs md:text-sm text-slate-500">
            Sistem Monitoring Nutrisi & Rekomendasi Pupuk
          </p>
        </div>
      </div>

      <div class="hidden md:flex items-center gap-2 min-w-0 shrink-0">
        <UserCircle2 class="h-8 w-8 text-green-700 shrink-0" />
        <div class="min-w-0">
          <p class="max-w-40 truncate text-sm font-semibold text-slate-800">
            {{ currentUser?.full_name || "Pengguna" }}
          </p>
          <p class="max-w-40 truncate text-xs text-slate-500">
            {{ currentUser?.email || "" }}
          </p>
        </div>
      </div>
    </div>
  </header>
</template>
