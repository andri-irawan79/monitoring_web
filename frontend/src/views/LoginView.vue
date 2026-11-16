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
  LoaderCircle,
  ArrowRight,
  Sprout,
  Droplets,
  Activity,
  ShieldCheck,
  CircleAlert
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

    // Pertahankan animasi autentikasi sebelum berpindah ke halaman tujuan.
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
  <main class="relative isolate min-h-screen overflow-hidden bg-[#f3f7f3]">
    <div class="pointer-events-none absolute -left-32 -top-32 h-80 w-80 rounded-full bg-emerald-200/40 blur-3xl" />
    <div class="pointer-events-none absolute -bottom-40 -right-20 h-96 w-96 rounded-full bg-lime-200/30 blur-3xl" />

    <div class="relative mx-auto grid min-h-screen w-full max-w-[1440px] grid-cols-1 lg:grid-cols-[1.04fr_0.96fr]">
      <section class="relative m-3 hidden min-h-[calc(100vh-1.5rem)] flex-col justify-between overflow-hidden rounded-[32px] bg-[#123b30] p-10 text-white shadow-2xl shadow-emerald-950/10 lg:flex xl:m-4 xl:p-14">
        <div class="pointer-events-none absolute -right-28 -top-28 h-96 w-96 rounded-full border border-white/10" />
        <div class="pointer-events-none absolute -right-12 -top-12 h-64 w-64 rounded-full border border-white/10" />
        <div class="pointer-events-none absolute -bottom-32 -left-24 h-80 w-80 rounded-full bg-emerald-400/10 blur-2xl" />
        <div class="relative z-10 flex items-center gap-3">
          <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-white/12 ring-1 ring-white/15">
            <Leaf class="h-6 w-6 text-lime-200" />
          </div>
          <div>
            <p class="text-sm font-bold tracking-wide">Durian Soil Monitor</p>
            <p class="mt-0.5 text-xs text-emerald-100/65">Monitoring & rekomendasi pemupukan</p>
          </div>
        </div>

        <div class="relative z-10 my-12 max-w-xl">
          <div class="mb-6 inline-flex items-center gap-2 rounded-full border border-emerald-100/15 bg-white/8 px-3.5 py-2 text-xs font-semibold tracking-wide text-emerald-100">
            <Sprout class="h-4 w-4 text-lime-200" />
            PENGELOLAAN TANAMAN DURIAN
          </div>
          <h1 class="max-w-lg text-4xl font-semibold leading-[1.15] tracking-tight xl:text-5xl">
            Kenali kondisi tanah. Rawat durian dengan lebih terarah.
          </h1>
          <p class="mt-6 max-w-lg text-sm leading-7 text-emerald-50/75 xl:text-base">
            Akses pemantauan data simulasi tanah dan dukungan rekomendasi pemupukan Durian Montong dalam satu sistem yang terintegrasi.
          </p>

          <div class="mt-10 rounded-3xl border border-white/12 bg-white/8 p-5 backdrop-blur-sm xl:p-6">
            <div class="flex items-center justify-between gap-4">
              <div>
                <p class="text-[11px] font-semibold uppercase tracking-[0.18em] text-emerald-100/60">Alur pengelolaan</p>
                <p class="mt-1 text-sm font-semibold text-white">Dari data menuju rekomendasi</p>
              </div>
              <div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-lime-200/15 text-lime-200">
                <Activity class="h-5 w-5" />
              </div>
            </div>
            <div class="mt-5 grid grid-cols-3 gap-3">
              <div class="rounded-2xl bg-black/10 p-3">
                <Droplets class="h-5 w-5 text-lime-200" />
                <p class="mt-3 text-xs font-semibold text-white">Kondisi tanah</p>
                <p class="mt-1 text-[11px] leading-4 text-emerald-100/55">Parameter nutrisi</p>
              </div>
              <div class="rounded-2xl bg-black/10 p-3">
                <Activity class="h-5 w-5 text-lime-200" />
                <p class="mt-3 text-xs font-semibold text-white">Analisis fuzzy</p>
                <p class="mt-1 text-[11px] leading-4 text-emerald-100/55">Metode Tsukamoto</p>
              </div>
              <div class="rounded-2xl bg-black/10 p-3">
                <Sprout class="h-5 w-5 text-lime-200" />
                <p class="mt-3 text-xs font-semibold text-white">Pemupukan</p>
                <p class="mt-1 text-[11px] leading-4 text-emerald-100/55">Jenis dan dosis</p>
              </div>
            </div>
          </div>
        </div>

        <div class="relative z-10 flex items-center justify-between gap-4 border-t border-white/10 pt-6 text-xs text-emerald-100/55">
          <span>Dirancang untuk mendukung keputusan budidaya</span>
          <span class="inline-flex items-center gap-1.5"><ShieldCheck class="h-4 w-4" /> Akses akun terlindungi</span>
        </div>
      </section>

      <section class="relative flex min-h-screen items-center justify-center px-4 py-8 sm:px-8 lg:px-10 xl:px-16">
        <div class="w-full max-w-[460px]">
          <div class="mb-7 flex items-center gap-3 lg:hidden">
            <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#123b30] shadow-lg shadow-emerald-900/10">
              <Leaf class="h-6 w-6 text-lime-200" />
            </div>
            <div>
              <p class="text-sm font-bold text-slate-800">Durian Soil Monitor</p>
              <p class="text-xs text-slate-500">Monitoring & rekomendasi pemupukan</p>
            </div>
          </div>

          <div class="rounded-[28px] border border-white/80 bg-white/95 p-6 shadow-[0_24px_70px_-30px_rgba(15,55,38,0.22)] backdrop-blur sm:p-9">
            <div class="mb-8">
              <div class="mb-5 inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-800">
                <span class="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                SELAMAT DATANG KEMBALI
              </div>
              <h2 class="text-3xl font-bold tracking-tight text-slate-900">Masuk ke akun Anda</h2>
              <p class="mt-2 text-sm leading-6 text-slate-500">
                Lanjutkan pemantauan kondisi tanah dan akses rekomendasi pemupukan tanaman durian.
              </p>
            </div>

            <div
              v-if="registeredMessage"
              class="mb-4 flex gap-3 rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm leading-6 text-emerald-800"
              role="status"
              aria-live="polite"
            >
              <CheckCircle2 class="mt-0.5 h-5 w-5 shrink-0 text-emerald-600" />
              <span>{{ registeredMessage }}</span>
            </div>

            <div
              v-if="expiredMessage"
              class="mb-4 flex gap-3 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm leading-6 text-amber-800"
              role="status"
            >
              <CircleAlert class="mt-0.5 h-5 w-5 shrink-0 text-amber-600" />
              <span>{{ expiredMessage }}</span>
            </div>

            <div
              v-if="errorMessage"
              class="mb-4 flex gap-3 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm leading-6 text-rose-700"
              role="alert"
              aria-live="assertive"
            >
              <CircleAlert class="mt-0.5 h-5 w-5 shrink-0 text-rose-600" />
              <span>{{ errorMessage }}</span>
            </div>

            <form class="space-y-5" @submit.prevent="submitLogin">
              <div>
                <label for="email" class="mb-2 block text-sm font-semibold text-slate-700">Email</label>
                <div class="group relative">
                  <Mail class="pointer-events-none absolute left-4 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-slate-400 transition group-focus-within:text-emerald-700" />
                  <input
                    id="email"
                    v-model="email"
                    type="email"
                    autocomplete="email"
                    required
                    :disabled="loading"
                    class="min-h-[54px] w-full rounded-2xl border border-slate-200 bg-slate-50/70 py-3 pl-12 pr-4 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 hover:border-slate-300 focus:border-emerald-600 focus:bg-white focus:ring-4 focus:ring-emerald-50 disabled:cursor-not-allowed disabled:opacity-60"
                    placeholder="nama@email.com"
                  />
                </div>
              </div>

              <div>
                <div class="mb-2 flex items-center justify-between gap-3">
                  <label for="password" class="block text-sm font-semibold text-slate-700">Kata Sandi</label>
                </div>
                <div class="group relative">
                  <Lock class="pointer-events-none absolute left-4 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-slate-400 transition group-focus-within:text-emerald-700" />
                  <input
                    id="password"
                    v-model="password"
                    :type="showPassword ? 'text' : 'password'"
                    autocomplete="current-password"
                    required
                    :disabled="loading"
                    class="min-h-[54px] w-full rounded-2xl border border-slate-200 bg-slate-50/70 py-3 pl-12 pr-12 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 hover:border-slate-300 focus:border-emerald-600 focus:bg-white focus:ring-4 focus:ring-emerald-50 disabled:cursor-not-allowed disabled:opacity-60"
                    placeholder="Masukkan kata sandi"
                  />
                  <button
                    type="button"
                    @click="showPassword = !showPassword"
                    :disabled="loading"
                    class="absolute right-3 top-1/2 flex h-9 w-9 -translate-y-1/2 items-center justify-center rounded-xl text-slate-400 transition hover:bg-slate-100 hover:text-slate-700 disabled:opacity-50"
                    :aria-label="showPassword ? 'Sembunyikan kata sandi' : 'Tampilkan kata sandi'"
                  >
                    <EyeOff v-if="showPassword" class="h-[18px] w-[18px]" />
                    <Eye v-else class="h-[18px] w-[18px]" />
                  </button>
                </div>
              </div>

              <button
                type="submit"
                :disabled="loading"
                class="group flex min-h-[54px] w-full items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-[#176447] to-[#238052] px-5 py-3 text-sm font-bold text-white shadow-lg shadow-emerald-900/15 transition duration-200 hover:-translate-y-0.5 hover:from-[#12563c] hover:to-[#1b7047] hover:shadow-xl hover:shadow-emerald-900/20 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-emerald-200 disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0"
              >
                <LoaderCircle v-if="loading" class="h-4 w-4 animate-spin" />
                <span>{{ loading ? "Memverifikasi akun..." : "Masuk ke Dashboard" }}</span>
                <ArrowRight v-if="!loading" class="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </button>
            </form>

            <div class="my-7 flex items-center gap-3">
              <div class="h-px flex-1 bg-slate-100" />
              <span class="text-[11px] font-medium uppercase tracking-[0.14em] text-slate-400">Akses sistem</span>
              <div class="h-px flex-1 bg-slate-100" />
            </div>

            <p class="text-center text-sm text-slate-500">
              Belum memiliki akun?
              <RouterLink to="/register" class="font-bold text-emerald-700 transition hover:text-emerald-900 hover:underline">
                Buat akun baru
              </RouterLink>
            </p>
          </div>

          <p class="mt-6 flex items-center justify-center gap-2 text-center text-xs text-slate-400">
            <ShieldCheck class="h-4 w-4" />
            Informasi akun Anda digunakan untuk mengelola akses sistem.
          </p>
        </div>
      </section>
    </div>
  </main>

  <Teleport to="body">
    <Transition name="login-transition">
      <div
        v-if="transitionActive"
        class="fixed inset-0 z-[200] flex items-center justify-center bg-slate-950/40 px-4 backdrop-blur-md"
        role="status"
        aria-live="polite"
        aria-label="Login berhasil, sedang menyiapkan dashboard"
      >
        <section class="w-full max-w-sm rounded-[28px] border border-white/70 bg-white p-7 text-center shadow-2xl shadow-slate-950/20 sm:p-8">
          <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-emerald-50 ring-8 ring-emerald-50/70">
            <CheckCircle2 class="h-9 w-9 text-emerald-600" />
          </div>

          <p class="mt-6 text-[11px] font-bold uppercase tracking-[0.18em] text-emerald-700">
            Autentikasi Berhasil
          </p>
          <h2 class="mt-2 text-xl font-bold tracking-tight text-slate-900">
            Berhasil masuk!
          </h2>
          <p class="mt-2 text-sm leading-6 text-slate-500">
            Menyiapkan dashboard Anda. Mohon tunggu sebentar.
          </p>

          <div class="mt-6 flex items-center justify-center gap-2 text-sm font-semibold text-emerald-700">
            <LoaderCircle class="h-4 w-4 animate-spin" />
            <span>Membuka dashboard</span>
          </div>

          <div class="mt-4 h-1.5 overflow-hidden rounded-full bg-emerald-100">
            <div class="login-progress h-full rounded-full bg-gradient-to-r from-emerald-500 to-lime-500" />
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
