<script setup>
import { ref } from "vue";
import { useRoute, useRouter, RouterLink } from "vue-router";
import {
  Leaf,
  Mail,
  Lock,
  Eye,
  EyeOff,
  CheckCircle2,
  LoaderCircle
} from "lucide-vue-next";
import { loginAccount } from "../services/authService";

const router = useRouter();
const route = useRoute();
const email = ref("");
const password = ref("");
const showPassword = ref(false);
const loading = ref(false);
const transitionActive = ref(false);
const errorMessage = ref("");

const expiredMessage = route.query.expired
  ? "Sesi Anda telah berakhir. Silakan masuk kembali."
  : "";

const registeredMessage = route.query.registered
  ? "Registrasi berhasil. Silakan masuk menggunakan akun yang baru dibuat."
  : "";

const submitLogin = async () => {
  if (loading.value) return;

  errorMessage.value = "";
  loading.value = true;

  try {
    await loginAccount({
      email: email.value.trim(),
      password: password.value
    });

    // Beri umpan balik visual sebelum berpindah ke halaman tujuan.
    transitionActive.value = true;
    await new Promise((resolve) => setTimeout(resolve, 1100));

    const destination =
      typeof route.query.redirect === "string"
        ? route.query.redirect
        : "/";

    await router.replace(destination);
  } catch (error) {
    transitionActive.value = false;
    errorMessage.value =
      error.response?.data?.detail ||
      "Tidak dapat masuk. Periksa koneksi dan data akun.";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <main class="min-h-screen bg-slate-100 flex items-center justify-center px-4 py-10">
    <section class="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-lg">
      <div class="mb-8 flex items-center gap-3">
        <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-green-100">
          <Leaf class="h-7 w-7 text-green-700" />
        </div>
        <div class="min-w-0">
          <h1 class="text-lg sm:text-xl font-bold text-slate-800">Dashboard Monitoring Durian</h1>
          <p class="text-xs sm:text-sm text-slate-500">Sistem Monitoring Nutrisi & Rekomendasi Pupuk</p>
        </div>
      </div>

      <div class="mb-6">
        <h2 class="text-2xl font-bold text-slate-800">Masuk</h2>
        <p class="mt-1 text-sm leading-relaxed text-slate-500">
          Masuk untuk mengakses dashboard dan rekomendasi pemupukan.
        </p>
      </div>

      <div
        v-if="registeredMessage"
        class="mb-4 rounded-xl border border-green-200 bg-green-50 p-3 text-sm leading-relaxed text-green-800"
        role="status"
        aria-live="polite"
      >
        {{ registeredMessage }}
      </div>

      <div
        v-if="expiredMessage"
        class="mb-4 rounded-xl border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800"
        role="status"
      >
        {{ expiredMessage }}
      </div>

      <div
        v-if="errorMessage"
        class="mb-4 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700"
        role="alert"
        aria-live="assertive"
      >
        {{ errorMessage }}
      </div>

      <form class="space-y-4" @submit.prevent="submitLogin">
        <div>
          <label for="email" class="mb-1 block text-sm font-medium text-slate-700">Email</label>
          <div class="relative">
            <Mail class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input
              id="email"
              v-model="email"
              type="email"
              autocomplete="email"
              required
              :disabled="loading"
              class="w-full rounded-xl border border-slate-300 py-3 pl-10 pr-3 text-sm outline-none transition focus:border-green-600 focus:ring-2 focus:ring-green-100 disabled:bg-slate-50"
              placeholder="nama@email.com"
            />
          </div>
        </div>

        <div>
          <label for="password" class="mb-1 block text-sm font-medium text-slate-700">Kata Sandi</label>
          <div class="relative">
            <Lock class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input
              id="password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="current-password"
              required
              :disabled="loading"
              class="w-full rounded-xl border border-slate-300 py-3 pl-10 pr-11 text-sm outline-none transition focus:border-green-600 focus:ring-2 focus:ring-green-100 disabled:bg-slate-50"
              placeholder="Masukkan kata sandi"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              :disabled="loading"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 transition hover:text-slate-700 disabled:opacity-50"
              :aria-label="showPassword ? 'Sembunyikan kata sandi' : 'Tampilkan kata sandi'"
            >
              <EyeOff v-if="showPassword" class="h-4 w-4" />
              <Eye v-else class="h-4 w-4" />
            </button>
          </div>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="
            flex
            min-h-12
            w-full
            items-center
            justify-center
            gap-2
            rounded-xl
            bg-green-700
            py-3
            text-sm
            font-semibold
            text-white
            shadow-sm
            transition
            hover:bg-green-800
            disabled:cursor-not-allowed
            disabled:opacity-60
            focus-visible:outline-none
            focus-visible:ring-2
            focus-visible:ring-green-500
            focus-visible:ring-offset-2
          "
        >
          <LoaderCircle v-if="loading" class="h-4 w-4 animate-spin" />
          {{ loading ? "Memverifikasi akun..." : "Masuk" }}
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-slate-500">
        Belum memiliki akun?
        <RouterLink to="/register" class="font-semibold text-green-700 hover:text-green-800">
          Daftar
        </RouterLink>
      </p>
    </section>
  </main>

  <Teleport to="body">
    <Transition name="login-transition">
      <div
        v-if="transitionActive"
        class="
          fixed
          inset-0
          z-[200]
          flex
          items-center
          justify-center
          bg-slate-900/35
          px-4
          backdrop-blur-sm
        "
        role="status"
        aria-live="polite"
        aria-label="Login berhasil, sedang menyiapkan dashboard"
      >
        <section class="w-full max-w-sm rounded-2xl border border-slate-100 bg-white p-7 text-center shadow-2xl sm:p-8">
          <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-50 ring-8 ring-green-50/70">
            <CheckCircle2 class="h-9 w-9 text-green-600" />
          </div>

          <p class="mt-6 text-xs font-semibold uppercase tracking-[0.16em] text-green-700">
            Autentikasi Berhasil
          </p>
          <h2 class="mt-2 text-xl font-bold text-slate-800">
            Berhasil masuk!
          </h2>
          <p class="mt-2 text-sm leading-6 text-slate-500">
            Menyiapkan dashboard Anda. Mohon tunggu sebentar.
          </p>

          <div class="mt-6 flex items-center justify-center gap-2 text-sm font-medium text-green-700">
            <LoaderCircle class="h-4 w-4 animate-spin" />
            <span>Membuka dashboard</span>
          </div>

          <div class="mt-4 h-1.5 overflow-hidden rounded-full bg-green-100">
            <div class="login-progress h-full rounded-full bg-green-600" />
          </div>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.login-transition-enter-active,
.login-transition-leave-active {
  transition: opacity 220ms ease;
}

.login-transition-enter-from,
.login-transition-leave-to {
  opacity: 0;
}

.login-progress {
  width: 100%;
  transform: scaleX(0);
  transform-origin: left;
  animation: login-progress 1.1s ease-out forwards;
}

@keyframes login-progress {
  to {
    transform: scaleX(1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .login-transition-enter-active,
  .login-transition-leave-active {
    transition: none;
  }

  .login-progress {
    animation-duration: 0.2s;
  }
}
</style>
