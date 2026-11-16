<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";
import { Leaf, UserRound, Mail, Lock, Eye, EyeOff, CheckCircle2, ArrowRight } from "lucide-vue-next";
import { registerAccount } from "../services/authService";

const fullName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const showPassword = ref(false);
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const registrationComplete = ref(false);
const registeredEmail = ref("");

const submitRegister = async () => {
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
  <main class="min-h-screen bg-slate-100 flex items-center justify-center px-4 py-10">
    <section class="w-full max-w-md overflow-hidden rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-lg">
      <div class="mb-7 flex items-center gap-3">
        <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-green-100">
          <Leaf class="h-7 w-7 text-green-700" />
        </div>
        <div class="min-w-0">
          <h1 class="text-lg sm:text-xl font-bold text-slate-800">Dashboard Monitoring Durian</h1>
          <p class="text-xs sm:text-sm text-slate-500">Sistem Monitoring Nutrisi & Rekomendasi Pupuk</p>
        </div>
      </div>

      <Transition name="auth-feedback" mode="out-in">
        <div v-if="registrationComplete" key="success" class="py-3 text-center">
          <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-50 ring-8 ring-green-50/60">
            <CheckCircle2 class="h-9 w-9 text-green-600" />
          </div>

          <p class="mt-6 text-xs font-semibold uppercase tracking-[0.16em] text-green-700">
            Registrasi Berhasil
          </p>
          <h2 class="mt-2 text-2xl font-bold text-slate-800">
            Akun berhasil dibuat!
          </h2>
          <p class="mt-3 text-sm leading-6 text-slate-500">
            {{ successMessage }}
          </p>

          <div class="mt-5 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-left">
            <p class="text-xs font-medium text-slate-500">Email akun</p>
            <p class="mt-1 break-all text-sm font-semibold text-slate-700">
              {{ registeredEmail }}
            </p>
          </div>

          <RouterLink
            :to="{ name: 'login', query: { registered: '1' } }"
            class="
              mt-6
              inline-flex
              min-h-12
              w-full
              items-center
              justify-center
              gap-2
              rounded-xl
              bg-green-700
              px-5
              py-3
              text-sm
              font-semibold
              text-white
              shadow-sm
              transition
              hover:bg-green-800
              focus-visible:outline-none
              focus-visible:ring-2
              focus-visible:ring-green-500
              focus-visible:ring-offset-2
            "
          >
            Lanjut ke Masuk
            <ArrowRight class="h-4 w-4" />
          </RouterLink>

          <p class="mt-4 text-xs text-slate-400">
            Gunakan email dan kata sandi yang baru Anda daftarkan.
          </p>
        </div>

        <div v-else key="form">
          <div class="mb-5">
            <h2 class="text-2xl font-bold text-slate-800">Daftar Akun</h2>
            <p class="mt-1 text-sm text-slate-500">Buat akun untuk menggunakan sistem.</p>
          </div>

          <div
            v-if="errorMessage"
            class="mb-4 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700"
            role="alert"
            aria-live="assertive"
          >
            {{ errorMessage }}
          </div>

          <form class="space-y-4" @submit.prevent="submitRegister">
            <div>
              <label for="full-name" class="mb-1 block text-sm font-medium text-slate-700">Nama Lengkap</label>
              <div class="relative">
                <UserRound class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <input
                  id="full-name"
                  v-model="fullName"
                  type="text"
                  autocomplete="name"
                  minlength="2"
                  maxlength="100"
                  required
                  class="w-full rounded-xl border border-slate-300 py-3 pl-10 pr-3 text-sm outline-none transition focus:border-green-600 focus:ring-2 focus:ring-green-100"
                  placeholder="Nama lengkap"
                />
              </div>
            </div>

            <div>
              <label for="register-email" class="mb-1 block text-sm font-medium text-slate-700">Email</label>
              <div class="relative">
                <Mail class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <input
                  id="register-email"
                  v-model="email"
                  type="email"
                  autocomplete="email"
                  required
                  class="w-full rounded-xl border border-slate-300 py-3 pl-10 pr-3 text-sm outline-none transition focus:border-green-600 focus:ring-2 focus:ring-green-100"
                  placeholder="nama@email.com"
                />
              </div>
            </div>

            <div>
              <label for="register-password" class="mb-1 block text-sm font-medium text-slate-700">Kata Sandi</label>
              <div class="relative">
                <Lock class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <input
                  id="register-password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  autocomplete="new-password"
                  minlength="8"
                  required
                  class="w-full rounded-xl border border-slate-300 py-3 pl-10 pr-11 text-sm outline-none transition focus:border-green-600 focus:ring-2 focus:ring-green-100"
                  placeholder="Minimal 8 karakter"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 transition hover:text-slate-700"
                  :aria-label="showPassword ? 'Sembunyikan kata sandi' : 'Tampilkan kata sandi'"
                >
                  <EyeOff v-if="showPassword" class="h-4 w-4" />
                  <Eye v-else class="h-4 w-4" />
                </button>
              </div>
            </div>

            <div>
              <label for="confirm-password" class="mb-1 block text-sm font-medium text-slate-700">Konfirmasi Kata Sandi</label>
              <input
                id="confirm-password"
                v-model="confirmPassword"
                type="password"
                autocomplete="new-password"
                minlength="8"
                required
                class="w-full rounded-xl border border-slate-300 px-3 py-3 text-sm outline-none transition focus:border-green-600 focus:ring-2 focus:ring-green-100"
                placeholder="Ulangi kata sandi"
              />
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="
                min-h-12
                w-full
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
              {{ loading ? "Membuat akun..." : "Daftar" }}
            </button>
          </form>

          <p class="mt-6 text-center text-sm text-slate-500">
            Sudah memiliki akun?
            <RouterLink to="/login" class="font-semibold text-green-700 hover:text-green-800">Masuk</RouterLink>
          </p>
        </div>
      </Transition>
    </section>
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
