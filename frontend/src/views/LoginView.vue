<script setup>
import { ref } from "vue";
import { useRoute, useRouter, RouterLink } from "vue-router";
import { Leaf, Mail, Lock, Eye, EyeOff } from "lucide-vue-next";
import { loginAccount } from "../services/authService";

const router = useRouter();
const route = useRoute();
const email = ref("");
const password = ref("");
const showPassword = ref(false);
const loading = ref(false);
const errorMessage = ref("");
const expiredMessage = route.query.expired
  ? "Sesi kamu telah berakhir. Silakan masuk kembali."
  : "";

const submitLogin = async () => {
  errorMessage.value = "";
  loading.value = true;
  try {
    await loginAccount({
      email: email.value.trim(),
      password: password.value
    });
    await router.replace("/");
  } catch (error) {
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
    <section class="w-full max-w-md bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
      <div class="flex items-center gap-3 mb-8">
        <div class="w-12 h-12 rounded-xl bg-green-100 flex items-center justify-center">
          <Leaf class="w-7 h-7 text-green-700" />
        </div>
        <div>
          <h1 class="text-xl font-bold text-slate-800">Dashboard Monitoring Durian</h1>
          <p class="text-sm text-slate-500">Sistem Monitoring Nutrisi & Rekomendasi Pupuk</p>
        </div>
      </div>

      <div class="mb-6">
        <h2 class="text-2xl font-bold text-slate-800">Masuk</h2>
        <p class="text-sm text-slate-500 mt-1">Masuk untuk mengakses dashboard dan rekomendasi pemupukan.</p>
      </div>

      <div v-if="expiredMessage" class="mb-4 rounded-lg bg-amber-50 border border-amber-200 p-3 text-sm text-amber-800">
        {{ expiredMessage }}
      </div>
      <div v-if="errorMessage" class="mb-4 rounded-lg bg-red-50 border border-red-200 p-3 text-sm text-red-700" role="alert">
        {{ errorMessage }}
      </div>

      <form class="space-y-4" @submit.prevent="submitLogin">
        <div>
          <label for="email" class="block text-sm font-medium text-slate-700 mb-1">Email</label>
          <div class="relative">
            <Mail class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input id="email" v-model="email" type="email" autocomplete="email" required
              class="w-full rounded-lg border border-slate-300 pl-10 pr-3 py-3 outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600"
              placeholder="nama@email.com" />
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-slate-700 mb-1">Kata Sandi</label>
          <div class="relative">
            <Lock class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input id="password" v-model="password" :type="showPassword ? 'text' : 'password'"
              autocomplete="current-password" required
              class="w-full rounded-lg border border-slate-300 pl-10 pr-11 py-3 outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600"
              placeholder="Masukkan kata sandi" />
            <button type="button" @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700"
              :aria-label="showPassword ? 'Sembunyikan kata sandi' : 'Tampilkan kata sandi'">
              <EyeOff v-if="showPassword" class="w-4 h-4" />
              <Eye v-else class="w-4 h-4" />
            </button>
          </div>
        </div>

        <button type="submit" :disabled="loading"
          class="w-full rounded-lg bg-green-700 hover:bg-green-800 disabled:opacity-60 text-white font-semibold py-3 transition">
          {{ loading ? "Memproses..." : "Masuk" }}
        </button>
      </form>

      <p class="text-sm text-center text-slate-500 mt-6">
        Belum memiliki akun?
        <RouterLink to="/register" class="font-semibold text-green-700 hover:text-green-800">Daftar</RouterLink>
      </p>
    </section>
  </main>
</template>
