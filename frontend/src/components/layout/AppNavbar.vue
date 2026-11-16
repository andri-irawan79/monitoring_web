<script setup>
import { onMounted } from "vue";
import { Leaf, UserCircle2 } from "lucide-vue-next";
import { currentUser } from "../../services/authState";
import { getCurrentAccount } from "../../services/authService";

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
  <header class="fixed top-0 left-0 right-0 z-50 bg-white border-b border-slate-200 shadow-sm">
    <div class="max-w-screen-2xl mx-auto px-6 md:px-8 h-20 flex items-center justify-between">
      <div class="flex items-center gap-4 min-w-0">
        <div class="w-12 h-12 rounded-xl bg-green-100 flex items-center justify-center shrink-0">
          <Leaf class="w-7 h-7 text-green-700" />
        </div>
        <div class="min-w-0">
          <h1 class="text-lg md:text-2xl font-bold text-slate-800 truncate">
            DASHBOARD MONITORING DURIAN
          </h1>
          <p class="text-xs md:text-sm text-slate-500 truncate">
            Sistem Monitoring Nutrisi & Rekomendasi Pupuk
          </p>
        </div>
      </div>

      <div class="flex items-center gap-2 md:gap-5">
        <div class="hidden sm:flex items-center gap-2 min-w-0">
          <UserCircle2 class="w-8 h-8 text-green-700 shrink-0" />
          <div class="min-w-0">
            <p class="font-semibold text-sm text-slate-800 truncate max-w-40">
              {{ currentUser?.full_name || "Pengguna" }}
            </p>
            <p class="text-xs text-slate-500 truncate max-w-40">
              {{ currentUser?.email || "" }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>
