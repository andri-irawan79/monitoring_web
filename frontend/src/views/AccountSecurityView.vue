<script setup>
import { computed, ref } from "vue";
import { RouterLink } from "vue-router";
import {
  ArrowLeft,
  CheckCircle2,
  CircleAlert,
  Eye,
  EyeOff,
  KeyRound,
  LockKeyhole,
  ShieldCheck,
  LoaderCircle,
  MonitorSmartphone,
  Info
} from "lucide-vue-next";
import { changePassword } from "../services/authService";

const currentPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const showCurrentPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

const newPasswordValid = computed(() => newPassword.value.length >= 8);
const passwordsMatch = computed(
  () => confirmPassword.value.length > 0 && newPassword.value === confirmPassword.value
);

const submitChangePassword = async () => {
  if (loading.value) return;

  errorMessage.value = "";
  successMessage.value = "";

  if (newPassword.value.length < 8) {
    errorMessage.value = "Kata sandi baru harus terdiri dari minimal 8 karakter.";
    return;
  }

  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = "Konfirmasi kata sandi baru belum sesuai.";
    return;
  }

  if (currentPassword.value === newPassword.value) {
    errorMessage.value = "Kata sandi baru harus berbeda dari kata sandi saat ini.";
    return;
  }

  loading.value = true;
  try {
    const response = await changePassword({
      current_password: currentPassword.value,
      new_password: newPassword.value
    });

    successMessage.value =
      response.message || "Kata sandi berhasil diperbarui.";

    currentPassword.value = "";
    newPassword.value = "";
    confirmPassword.value = "";
    showCurrentPassword.value = false;
    showNewPassword.value = false;
    showConfirmPassword.value = false;
  } catch (error) {
    const detail = error.response?.data?.detail;
    errorMessage.value =
      (typeof detail === "string" && detail) ||
      "Kata sandi belum dapat diperbarui. Periksa kata sandi saat ini dan koneksi server.";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="mx-auto w-full max-w-5xl">
    <div class="mb-6">
      <RouterLink
        to="/"
        class="inline-flex items-center gap-2 rounded-lg text-xs font-semibold text-slate-500 transition hover:text-emerald-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2"
      >
        <ArrowLeft class="h-4 w-4" />
        Kembali ke dashboard
      </RouterLink>

      <div class="mt-5 flex items-start gap-4">
        <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-emerald-100 text-emerald-800 ring-1 ring-emerald-200/70">
          <KeyRound class="h-6 w-6" />
        </div>
        <div class="min-w-0">
          <p class="text-[10px] font-extrabold uppercase tracking-[0.18em] text-emerald-700">
            Pengaturan akun
          </p>
          <h1 class="mt-1 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl">
            Keamanan akun
          </h1>
          <p class="mt-1.5 max-w-2xl text-sm leading-6 text-slate-500">
            Perbarui kata sandi untuk menjaga keamanan akses akun dan data penelitian Anda.
          </p>
        </div>
      </div>
    </div>

    <div class="mx-auto w-full max-w-3xl">
      <section class="min-w-0 rounded-2xl border border-slate-200/80 bg-white p-5 shadow-[0_8px_30px_-24px_rgba(15,65,48,.35)] sm:p-7">
        <div class="flex items-start gap-3 border-b border-slate-100 pb-5">
          <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700">
            <LockKeyhole class="h-5 w-5" />
          </div>
          <div>
            <h2 class="text-base font-bold text-slate-800">Ubah kata sandi</h2>
            <p class="mt-1 text-xs leading-5 text-slate-500">
              Masukkan kata sandi saat ini, lalu tentukan kata sandi baru.
            </p>
          </div>
        </div>

        <div
          v-if="successMessage"
          class="mt-5 flex items-start gap-3 rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm leading-6 text-emerald-800"
          role="status"
          aria-live="polite"
        >
          <CheckCircle2 class="mt-0.5 h-5 w-5 shrink-0 text-emerald-600" />
          <div>
            <p class="font-bold">Perubahan berhasil disimpan</p>
            <p class="mt-0.5">{{ successMessage }} Anda tetap masuk pada perangkat ini.</p>
          </div>
        </div>

        <div
          v-if="errorMessage"
          class="mt-5 flex items-start gap-3 rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm leading-6 text-rose-700"
          role="alert"
          aria-live="assertive"
        >
          <CircleAlert class="mt-0.5 h-5 w-5 shrink-0 text-rose-600" />
          <p>{{ errorMessage }}</p>
        </div>

        <form class="mt-6 space-y-5" @submit.prevent="submitChangePassword">
          <div>
            <label for="current-password" class="mb-2 block text-xs font-bold text-slate-700">
              Kata sandi saat ini
            </label>
            <div class="relative">
              <LockKeyhole class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
              <input
                id="current-password"
                v-model="currentPassword"
                :type="showCurrentPassword ? 'text' : 'password'"
                autocomplete="current-password"
                maxlength="128"
                required
                :disabled="loading"
                class="security-input pl-10 pr-12"
                placeholder="Masukkan kata sandi saat ini"
              />
              <button
                type="button"
                class="security-eye"
                :disabled="loading"
                :aria-label="showCurrentPassword ? 'Sembunyikan kata sandi saat ini' : 'Tampilkan kata sandi saat ini'"
                @click="showCurrentPassword = !showCurrentPassword"
              >
                <EyeOff v-if="showCurrentPassword" class="h-4 w-4" />
                <Eye v-else class="h-4 w-4" />
              </button>
            </div>
          </div>

          <div>
            <label for="new-password" class="mb-2 block text-xs font-bold text-slate-700">
              Kata sandi baru
            </label>
            <div class="relative">
              <KeyRound class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
              <input
                id="new-password"
                v-model="newPassword"
                :type="showNewPassword ? 'text' : 'password'"
                autocomplete="new-password"
                minlength="8"
                maxlength="128"
                required
                :disabled="loading"
                class="security-input pl-10 pr-12"
                placeholder="Buat kata sandi baru"
                aria-describedby="password-requirement"
              />
              <button
                type="button"
                class="security-eye"
                :disabled="loading"
                :aria-label="showNewPassword ? 'Sembunyikan kata sandi baru' : 'Tampilkan kata sandi baru'"
                @click="showNewPassword = !showNewPassword"
              >
                <EyeOff v-if="showNewPassword" class="h-4 w-4" />
                <Eye v-else class="h-4 w-4" />
              </button>
            </div>
            <p id="password-requirement" class="mt-2 flex items-center gap-2 text-[11px]" :class="newPassword.length === 0 || newPasswordValid ? 'text-slate-400' : 'text-rose-600'">
              <CheckCircle2 v-if="newPasswordValid" class="h-3.5 w-3.5 text-emerald-600" />
              <Info v-else class="h-3.5 w-3.5" />
              Minimal 8 karakter.
            </p>
          </div>

          <div>
            <label for="confirm-password" class="mb-2 block text-xs font-bold text-slate-700">
              Konfirmasi kata sandi baru
            </label>
            <div class="relative">
              <KeyRound class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
              <input
                id="confirm-password"
                v-model="confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                autocomplete="new-password"
                minlength="8"
                maxlength="128"
                required
                :disabled="loading"
                class="security-input pl-10 pr-12"
                placeholder="Ulangi kata sandi baru"
              />
              <button
                type="button"
                class="security-eye"
                :disabled="loading"
                :aria-label="showConfirmPassword ? 'Sembunyikan konfirmasi kata sandi' : 'Tampilkan konfirmasi kata sandi'"
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <EyeOff v-if="showConfirmPassword" class="h-4 w-4" />
                <Eye v-else class="h-4 w-4" />
              </button>
            </div>
            <p v-if="confirmPassword.length > 0" class="mt-2 flex items-center gap-2 text-[11px]" :class="passwordsMatch ? 'text-emerald-700' : 'text-rose-600'">
              <CheckCircle2 v-if="passwordsMatch" class="h-3.5 w-3.5" />
              <CircleAlert v-else class="h-3.5 w-3.5" />
              {{ passwordsMatch ? "Konfirmasi kata sandi sesuai." : "Konfirmasi kata sandi belum sesuai." }}
            </p>
          </div>

          <div class="flex flex-col-reverse gap-3 border-t border-slate-100 pt-5 sm:flex-row sm:items-center sm:justify-between">
            <RouterLink
              to="/"
              class="inline-flex min-h-11 items-center justify-center rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-600 transition hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2"
            >
              Batal
            </RouterLink>
            <button
              type="submit"
              :disabled="loading"
              class="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-emerald-800 px-5 py-2.5 text-xs font-extrabold text-white shadow-sm shadow-emerald-900/10 transition hover:-translate-y-0.5 hover:bg-emerald-900 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0"
            >
              <LoaderCircle v-if="loading" class="h-4 w-4 animate-spin" />
              <ShieldCheck v-else class="h-4 w-4" />
              {{ loading ? "Menyimpan perubahan..." : "Simpan kata sandi" }}
            </button>
          </div>
        </form>

        <div class="mt-6 space-y-3 border-t border-slate-100 pt-5">
          <div class="flex items-start gap-2.5">
            <ShieldCheck class="mt-0.5 h-4 w-4 shrink-0 text-emerald-700" />
            <p class="text-xs leading-5 text-slate-500">
              <span class="font-semibold text-slate-700">Perlindungan akun.</span>
              Kata sandi baru disimpan dalam bentuk hash pada server. Kata sandi asli tidak ditampilkan atau disimpan sebagai teks biasa.
            </p>
          </div>
          <div class="flex items-start gap-2.5">
            <MonitorSmartphone class="mt-0.5 h-4 w-4 shrink-0 text-emerald-700" />
            <p class="text-xs leading-5 text-slate-500">
              <span class="font-semibold text-slate-700">Sesi akun.</span>
              Setelah kata sandi diubah, sesi pada perangkat lain akan diminta masuk kembali. Sesi yang sedang digunakan tetap aktif.
            </p>
          </div>
          <p class="pl-6 text-[11px] leading-5 text-slate-400">
            Perubahan kata sandi hanya memengaruhi keamanan akun. Data monitoring simulasi dan riwayat pengujian tetap tersimpan.
          </p>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.security-input {
  display: block;
  width: 100%;
  min-height: 46px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #f8fafc;
  padding-top: 11px;
  padding-bottom: 11px;
  color: #1e293b;
  font-size: 13px;
  outline: none;
  transition: border-color 160ms ease, background 160ms ease, box-shadow 160ms ease;
}

.security-input::placeholder {
  color: #94a3b8;
}

.security-input:hover {
  border-color: #cbd5e1;
}

.security-input:focus {
  border-color: #059669;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.12);
}

.security-input:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.security-eye {
  position: absolute;
  top: 50%;
  right: 8px;
  display: flex;
  width: 32px;
  height: 32px;
  transform: translateY(-50%);
  align-items: center;
  justify-content: center;
  border-radius: 9px;
  color: #94a3b8;
  transition: background 160ms ease, color 160ms ease;
}

.security-eye:hover {
  background: #e2e8f0;
  color: #334155;
}

.security-eye:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

@media (prefers-reduced-motion: reduce) {
  .security-input,
  .security-eye {
    transition: none;
  }
}
</style>
