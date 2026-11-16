<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";
import {
  Leaf,
  UserRound,
  Mail,
  Lock,
  Eye,
  EyeOff,
  CheckCircle2,
  ArrowRight,
  LoaderCircle,
  Sprout,
  Droplets,
  Activity,
  ShieldCheck,
  CircleAlert
} from "lucide-vue-next";
import { registerAccount } from "../services/authService";

const fullName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const registrationComplete = ref(false);
const registeredEmail = ref("");

const submitRegister = async () => {
  if (loading.value) return;

  errorMessage.value = "";

  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Konfirmasi kata sandi tidak sama.";
    return;
  }
  if (password.value.length < 8) {
    errorMessage.value = "Kata sandi minimal 8 karakter.";
    return;
  }

  loading.value = true;
  try {
    const result = await registerAccount({
      full_name: fullName.value.trim(),
      email: email.value.trim(),
      password: password.value
    });

    registeredEmail.value = email.value.trim();
    successMessage.value =
      result.message || "Akun Anda berhasil dibuat. Silakan masuk untuk melanjutkan.";
    registrationComplete.value = true;
  } catch (error) {
    errorMessage.value =
      error.response?.data?.detail ||
      "Pendaftaran gagal. Periksa data dan koneksi.";
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
            MULAI PERJALANAN BUDIDAYA
          </div>
          <h1 class="max-w-lg text-4xl font-semibold leading-[1.15] tracking-tight xl:text-5xl">
            Satu akun untuk pengelolaan durian yang lebih terarah.
          </h1>
          <p class="mt-6 max-w-lg text-sm leading-7 text-emerald-50/75 xl:text-base">
            Buat akun untuk menyimpan data pemantauan, melihat riwayat, dan memperoleh rekomendasi pemupukan sesuai fase pertumbuhan Durian Montong.
          </p>

          <div class="mt-10 rounded-3xl border border-white/12 bg-white/8 p-5 backdrop-blur-sm xl:p-6">
            <p class="text-[11px] font-semibold uppercase tracking-[0.18em] text-emerald-100/60">Yang dapat Anda kelola</p>
            <div class="mt-5 space-y-4">
              <div class="flex items-center gap-3">
                <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-lime-200/15 text-lime-200">
                  <Droplets class="h-5 w-5" />
                </div>
                <div>
                  <p class="text-sm font-semibold text-white">Kondisi dan nutrisi tanah</p>
                  <p class="mt-0.5 text-xs text-emerald-100/55">N, P, K, pH, suhu, kelembapan, dan curah hujan</p>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-lime-200/15 text-lime-200">
                  <Activity class="h-5 w-5" />
                </div>
                <div>
                  <p class="text-sm font-semibold text-white">Analisis Fuzzy Tsukamoto</p>
                  <p class="mt-0.5 text-xs text-emerald-100/55">Pengolahan berdasarkan kondisi tanah dan fase</p>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-lime-200/15 text-lime-200">
                  <Sprout class="h-5 w-5" />
                </div>
                <div>
                  <p class="text-sm font-semibold text-white">Riwayat rekomendasi</p>
                  <p class="mt-0.5 text-xs text-emerald-100/55">Jenis pupuk dan dosis yang disarankan</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="relative z-10 flex items-center justify-between gap-4 border-t border-white/10 pt-6 text-xs text-emerald-100/55">
          <span>Mulai dengan akun pribadi Anda</span>
          <span class="inline-flex items-center gap-1.5"><ShieldCheck class="h-4 w-4" /> Akses akun terlindungi</span>
        </div>
      </section>

      <section class="relative flex min-h-screen items-center justify-center px-4 py-8 sm:px-8 lg:px-10 xl:px-16">
        <div class="w-full max-w-[480px]">
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
            <Transition name="auth-feedback" mode="out-in">
              <div v-if="registrationComplete" key="success" class="py-3 text-center">
                <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-emerald-50 ring-8 ring-emerald-50/70">
                  <CheckCircle2 class="h-9 w-9 text-emerald-600" />
                </div>

                <p class="mt-6 text-[11px] font-bold uppercase tracking-[0.18em] text-emerald-700">
                  REGISTRASI BERHASIL
                </p>
                <h2 class="mt-2 text-2xl font-bold tracking-tight text-slate-900">
                  Akun berhasil dibuat!
                </h2>
                <p class="mt-3 text-sm leading-6 text-slate-500">
                  {{ successMessage }}
                </p>

                <div class="mt-6 rounded-2xl border border-emerald-100 bg-emerald-50/60 p-4 text-left">
                  <div class="flex items-center gap-2 text-xs font-semibold text-emerald-800">
                    <Mail class="h-4 w-4" />
                    EMAIL AKUN TERDAFTAR
                  </div>
                  <p class="mt-2 break-all text-sm font-semibold text-slate-800">
                    {{ registeredEmail }}
                  </p>
                </div>

                <RouterLink
                  :to="{ name: 'login', query: { registered: '1' } }"
                  class="group mt-6 inline-flex min-h-[54px] w-full items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-[#176447] to-[#238052] px-5 py-3 text-sm font-bold text-white shadow-lg shadow-emerald-900/15 transition duration-200 hover:-translate-y-0.5 hover:shadow-xl focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-emerald-200"
                >
                  Lanjut ke Masuk
                  <ArrowRight class="h-4 w-4 transition-transform group-hover:translate-x-1" />
                </RouterLink>

                <p class="mt-5 flex items-center justify-center gap-2 text-xs text-slate-400">
                  <ShieldCheck class="h-4 w-4" />
                  Gunakan email dan kata sandi yang baru didaftarkan.
                </p>
              </div>

              <div v-else key="form">
                <div class="mb-7">
                  <div class="mb-5 inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-800">
                    <span class="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                    PENDAFTARAN AKUN
                  </div>
                  <h2 class="text-3xl font-bold tracking-tight text-slate-900">Buat akun baru</h2>
                  <p class="mt-2 text-sm leading-6 text-slate-500">
                    Lengkapi informasi berikut untuk mulai menggunakan sistem monitoring dan rekomendasi pemupukan.
                  </p>
                </div>

                <div
                  v-if="errorMessage"
                  class="mb-5 flex gap-3 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm leading-6 text-rose-700"
                  role="alert"
                  aria-live="assertive"
                >
                  <CircleAlert class="mt-0.5 h-5 w-5 shrink-0 text-rose-600" />
                  <span>{{ errorMessage }}</span>
                </div>

                <form class="space-y-4" @submit.prevent="submitRegister">
                  <div>
                    <label for="full-name" class="mb-2 block text-sm font-semibold text-slate-700">Nama Lengkap</label>
                    <div class="group relative">
                      <UserRound class="pointer-events-none absolute left-4 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-slate-400 transition group-focus-within:text-emerald-700" />
                      <input
                        id="full-name"
                        v-model="fullName"
                        type="text"
                        autocomplete="name"
                        minlength="2"
                        maxlength="100"
                        required
                        :disabled="loading"
                        class="min-h-[52px] w-full rounded-2xl border border-slate-200 bg-slate-50/70 py-3 pl-12 pr-4 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 hover:border-slate-300 focus:border-emerald-600 focus:bg-white focus:ring-4 focus:ring-emerald-50 disabled:cursor-not-allowed disabled:opacity-60"
                        placeholder="Masukkan nama lengkap"
                      />
                    </div>
                  </div>

                  <div>
                    <label for="register-email" class="mb-2 block text-sm font-semibold text-slate-700">Email</label>
                    <div class="group relative">
                      <Mail class="pointer-events-none absolute left-4 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-slate-400 transition group-focus-within:text-emerald-700" />
                      <input
                        id="register-email"
                        v-model="email"
                        type="email"
                        autocomplete="email"
                        required
                        :disabled="loading"
                        class="min-h-[52px] w-full rounded-2xl border border-slate-200 bg-slate-50/70 py-3 pl-12 pr-4 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 hover:border-slate-300 focus:border-emerald-600 focus:bg-white focus:ring-4 focus:ring-emerald-50 disabled:cursor-not-allowed disabled:opacity-60"
                        placeholder="nama@email.com"
                      />
                    </div>
                  </div>

                  <div>
                    <label for="register-password" class="mb-2 block text-sm font-semibold text-slate-700">Kata Sandi</label>
                    <div class="group relative">
                      <Lock class="pointer-events-none absolute left-4 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-slate-400 transition group-focus-within:text-emerald-700" />
                      <input
                        id="register-password"
                        v-model="password"
                        :type="showPassword ? 'text' : 'password'"
                        autocomplete="new-password"
                        minlength="8"
                        required
                        :disabled="loading"
                        class="min-h-[52px] w-full rounded-2xl border border-slate-200 bg-slate-50/70 py-3 pl-12 pr-12 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 hover:border-slate-300 focus:border-emerald-600 focus:bg-white focus:ring-4 focus:ring-emerald-50 disabled:cursor-not-allowed disabled:opacity-60"
                        placeholder="Buat kata sandi minimal 8 karakter"
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
                    <p class="mt-2 text-xs text-slate-400">Gunakan minimal 8 karakter untuk kata sandi Anda.</p>
                  </div>

                  <div>
                    <label for="confirm-password" class="mb-2 block text-sm font-semibold text-slate-700">Konfirmasi Kata Sandi</label>
                    <div class="group relative">
                      <Lock class="pointer-events-none absolute left-4 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-slate-400 transition group-focus-within:text-emerald-700" />
                      <input
                        id="confirm-password"
                        v-model="confirmPassword"
                        :type="showConfirmPassword ? 'text' : 'password'"
                        autocomplete="new-password"
                        minlength="8"
                        required
                        :disabled="loading"
                        class="min-h-[52px] w-full rounded-2xl border border-slate-200 bg-slate-50/70 py-3 pl-12 pr-12 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 hover:border-slate-300 focus:border-emerald-600 focus:bg-white focus:ring-4 focus:ring-emerald-50 disabled:cursor-not-allowed disabled:opacity-60"
                        placeholder="Ulangi kata sandi"
                      />
                      <button
                        type="button"
                        @click="showConfirmPassword = !showConfirmPassword"
                        :disabled="loading"
                        class="absolute right-3 top-1/2 flex h-9 w-9 -translate-y-1/2 items-center justify-center rounded-xl text-slate-400 transition hover:bg-slate-100 hover:text-slate-700 disabled:opacity-50"
                        :aria-label="showConfirmPassword ? 'Sembunyikan konfirmasi kata sandi' : 'Tampilkan konfirmasi kata sandi'"
                      >
                        <EyeOff v-if="showConfirmPassword" class="h-[18px] w-[18px]" />
                        <Eye v-else class="h-[18px] w-[18px]" />
                      </button>
                    </div>
                  </div>

                  <button
                    type="submit"
                    :disabled="loading"
                    class="group mt-2 flex min-h-[54px] w-full items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-[#176447] to-[#238052] px-5 py-3 text-sm font-bold text-white shadow-lg shadow-emerald-900/15 transition duration-200 hover:-translate-y-0.5 hover:from-[#12563c] hover:to-[#1b7047] hover:shadow-xl hover:shadow-emerald-900/20 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-emerald-200 disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0"
                  >
                    <LoaderCircle v-if="loading" class="h-4 w-4 animate-spin" />
                    <span>{{ loading ? "Membuat akun..." : "Buat Akun" }}</span>
                    <ArrowRight v-if="!loading" class="h-4 w-4 transition-transform group-hover:translate-x-1" />
                  </button>
                </form>

                <div class="my-6 flex items-center gap-3">
                  <div class="h-px flex-1 bg-slate-100" />
                  <span class="text-[11px] font-medium uppercase tracking-[0.14em] text-slate-400">ATAU</span>
                  <div class="h-px flex-1 bg-slate-100" />
                </div>

                <p class="text-center text-sm text-slate-500">
                  Sudah memiliki akun?
                  <RouterLink to="/login" class="font-bold text-emerald-700 transition hover:text-emerald-900 hover:underline">
                    Masuk di sini
                  </RouterLink>
                </p>
              </div>
            </Transition>
          </div>

          <p class="mt-6 flex items-center justify-center gap-2 text-center text-xs text-slate-400">
            <ShieldCheck class="h-4 w-4" />
            Data akun digunakan untuk mengelola akses dan riwayat Anda.
          </p>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
.auth-feedback-enter-active,
.auth-feedback-leave-active {
  transition: opacity 180ms ease, transform 180ms ease;
}

.auth-feedback-enter-from,
.auth-feedback-leave-to {
  opacity: 0;
  transform: translateY(6px);
}

@media (prefers-reduced-motion: reduce) {
  .auth-feedback-enter-active,
  .auth-feedback-leave-active {
    transition: none;
  }
}
</style>
