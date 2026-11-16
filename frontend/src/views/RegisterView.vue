<script setup>
import { ref } from "vue";
import { useRouter, RouterLink } from "vue-router";
import { Leaf, UserRound, Mail, Lock, Eye, EyeOff } from "lucide-vue-next";
import { registerAccount } from "../services/authService";

const router = useRouter();
const fullName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const showPassword = ref(false);
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

const submitRegister = async () => {
  errorMessage.value = "";
  successMessage.value = "";

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
    successMessage.value = result.message;
    setTimeout(() => router.replace("/login"), 900);
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
    <section class="w-full max-w-md bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
      <div class="flex items-center gap-3 mb-7">
        <div class="w-12 h-12 rounded-xl bg-green-100 flex items-center justify-center">
          <Leaf class="w-7 h-7 text-green-700" />
        </div>
        <div>
          <h1 class="text-xl font-bold text-slate-800">Dashboard Monitoring Durian</h1>
          <p class="text-sm text-slate-500">Sistem Monitoring Nutrisi & Rekomendasi Pupuk</p>
        </div>
      </div>

      <div class="mb-5">
        <h2 class="text-2xl font-bold text-slate-800">Daftar Akun</h2>
        <p class="text-sm text-slate-500 mt-1">Buat akun untuk menggunakan sistem.</p>
      </div>

      <div v-if="errorMessage" class="mb-4 rounded-lg bg-red-50 border border-red-200 p-3 text-sm text-red-700" role="alert">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="mb-4 rounded-lg bg-green-50 border border-green-200 p-3 text-sm text-green-700" role="status">
        {{ successMessage }}
      </div>

      <form class="space-y-4" @submit.prevent="submitRegister">
        <div>
          <label for="full-name" class="block text-sm font-medium text-slate-700 mb-1">Nama Lengkap</label>
          <div class="relative">
            <UserRound class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input id="full-name" v-model="fullName" type="text" autocomplete="name" minlength="2" maxlength="100" required
              class="w-full rounded-lg border border-slate-300 pl-10 pr-3 py-3 outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600"
              placeholder="Nama lengkap" />
          </div>
        </div>

        <div>
          <label for="register-email" class="block text-sm font-medium text-slate-700 mb-1">Email</label>
          <div class="relative">
            <Mail class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input id="register-email" v-model="email" type="email" autocomplete="email" required
              class="w-full rounded-lg border border-slate-300 pl-10 pr-3 py-3 outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600"
              placeholder="nama@email.com" />
          </div>
        </div>

        <div>
          <label for="register-password" class="block text-sm font-medium text-slate-700 mb-1">Kata Sandi</label>
          <div class="relative">
            <Lock class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input id="register-password" v-model="password" :type="showPassword ? 'text' : 'password'"
              autocomplete="new-password" minlength="8" required
              class="w-full rounded-lg border border-slate-300 pl-10 pr-11 py-3 outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600"
              placeholder="Minimal 8 karakter" />
            <button type="button" @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700"
              :aria-label="showPassword ? 'Sembunyikan kata sandi' : 'Tampilkan kata sandi'">
              <EyeOff v-if="showPassword" class="w-4 h-4" />
              <Eye v-else class="w-4 h-4" />
            </button>
          </div>
        </div>

        <div>
          <label for="confirm-password" class="block text-sm font-medium text-slate-700 mb-1">Konfirmasi Kata Sandi</label>
          <input id="confirm-password" v-model="confirmPassword" type="password" autocomplete="new-password" minlength="8" required
            class="w-full rounded-lg border border-slate-300 px-3 py-3 outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600"
            placeholder="Ulangi kata sandi" />
        </div>

        <button type="submit" :disabled="loading"
          class="w-full rounded-lg bg-green-700 hover:bg-green-800 disabled:opacity-60 text-white font-semibold py-3 transition">
          {{ loading ? "Membuat akun..." : "Daftar" }}
        </button>
      </form>

      <p class="text-sm text-center text-slate-500 mt-6">
        Sudah memiliki akun?
        <RouterLink to="/login" class="font-semibold text-green-700 hover:text-green-800">Masuk</RouterLink>
      </p>
    </section>
  </main>
</template>
