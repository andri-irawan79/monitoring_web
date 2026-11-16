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
  CircleAlert,
  Microscope
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
  <main class="auth-page flex min-h-screen items-center justify-center px-4 py-8 sm:px-6">
    <section class="auth-shell grid w-full max-w-[1020px] grid-cols-1 overflow-hidden rounded-[28px] bg-white shadow-[0_24px_70px_-28px_rgba(30,35,70,0.38)] lg:min-h-[670px] lg:grid-cols-[1.12fr_0.88fr]">
      <div class="flex items-center px-6 py-9 sm:px-10 sm:py-11 lg:px-12">
        <div class="mx-auto w-full max-w-[410px]">
          <div class="mb-7 flex items-center justify-center gap-2 lg:justify-start">
            <div class="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-100 text-emerald-800">
              <Leaf class="h-5 w-5" />
            </div>
            <div>
              <p class="text-sm font-bold tracking-tight text-slate-800">Monitoring Tanah Durian</p>
              <p class="text-[11px] text-slate-400">Sistem pendukung penelitian</p>
            </div>
          </div>

          <Transition name="auth-feedback" mode="out-in">
            <div v-if="registrationComplete" key="success" class="py-3 text-center">
              <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-emerald-50 ring-8 ring-emerald-50/70">
                <CheckCircle2 class="h-9 w-9 text-emerald-600" />
              </div>

              <p class="mt-6 text-[11px] font-bold uppercase tracking-[0.2em] text-emerald-700">
                Registrasi berhasil
              </p>
              <h1 class="mt-2 text-2xl font-bold tracking-tight text-slate-900">
                Akun berhasil dibuat!
              </h1>
              <p class="mt-3 text-sm leading-6 text-slate-500">
                {{ successMessage }}
              </p>

              <div class="mt-6 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-left">
                <p class="flex items-center gap-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
                  <Mail class="h-4 w-4 text-emerald-700" />
                  Email akun
                </p>
                <p class="mt-1.5 break-all text-sm font-semibold text-slate-800">
                  {{ registeredEmail }}
                </p>
              </div>

              <RouterLink
                :to="{ name: 'login', query: { registered: '1' } }"
                class="auth-submit mt-6"
              >
                Lanjut ke Masuk
                <ArrowRight class="h-4 w-4" />
              </RouterLink>

              <p class="mt-5 text-[11px] leading-5 text-slate-400">
                Gunakan email dan kata sandi yang baru Anda daftarkan.
              </p>
            </div>

            <div v-else key="form">
              <div class="mb-6 text-center lg:text-left">
                <p class="mb-2 text-[11px] font-bold uppercase tracking-[0.2em] text-emerald-700">
                  Registrasi penelitian
                </p>
                <h1 class="text-3xl font-bold tracking-tight text-slate-900">Daftar akun</h1>
                <p class="mt-2 text-sm leading-6 text-slate-500">
                  Buat akun untuk mengakses data simulasi dan meninjau hasil pengujian sistem penelitian.
                </p>
              </div>

              <div
                v-if="errorMessage"
                class="mb-4 flex items-start gap-2.5 rounded-xl border border-rose-200 bg-rose-50 px-3.5 py-3 text-sm leading-5 text-rose-700"
                role="alert"
                aria-live="assertive"
              >
                <CircleAlert class="mt-0.5 h-4 w-4 shrink-0 text-rose-600" />
                <span>{{ errorMessage }}</span>
              </div>

              <form class="space-y-3.5" @submit.prevent="submitRegister">
                <div>
                  <label for="full-name" class="mb-1.5 block text-xs font-semibold text-slate-700">Nama Lengkap</label>
                  <div class="auth-input-wrap">
                    <UserRound class="auth-input-icon" />
                    <input
                      id="full-name"
                      v-model="fullName"
                      type="text"
                      autocomplete="name"
                      minlength="2"
                      maxlength="100"
                      required
                      :disabled="loading"
                      class="auth-input pl-10"
                      placeholder="Masukkan nama lengkap"
                    />
                  </div>
                </div>

                <div>
                  <label for="register-email" class="mb-1.5 block text-xs font-semibold text-slate-700">Email</label>
                  <div class="auth-input-wrap">
                    <Mail class="auth-input-icon" />
                    <input
                      id="register-email"
                      v-model="email"
                      type="email"
                      autocomplete="email"
                      required
                      :disabled="loading"
                      class="auth-input pl-10"
                      placeholder="nama@email.com"
                    />
                  </div>
                </div>

                <div>
                  <label for="register-password" class="mb-1.5 block text-xs font-semibold text-slate-700">Kata Sandi</label>
                  <div class="auth-input-wrap">
                    <Lock class="auth-input-icon" />
                    <input
                      id="register-password"
                      v-model="password"
                      :type="showPassword ? 'text' : 'password'"
                      autocomplete="new-password"
                      minlength="8"
                      required
                      :disabled="loading"
                      class="auth-input pl-10 pr-11"
                      placeholder="Minimal 8 karakter"
                    />
                    <button
                      type="button"
                      @click="showPassword = !showPassword"
                      :disabled="loading"
                      class="auth-visibility-button"
                      :aria-label="showPassword ? 'Sembunyikan kata sandi' : 'Tampilkan kata sandi'"
                    >
                      <EyeOff v-if="showPassword" class="h-4 w-4" />
                      <Eye v-else class="h-4 w-4" />
                    </button>
                  </div>
                </div>

                <div>
                  <label for="confirm-password" class="mb-1.5 block text-xs font-semibold text-slate-700">Konfirmasi Kata Sandi</label>
                  <div class="auth-input-wrap">
                    <Lock class="auth-input-icon" />
                    <input
                      id="confirm-password"
                      v-model="confirmPassword"
                      :type="showConfirmPassword ? 'text' : 'password'"
                      autocomplete="new-password"
                      minlength="8"
                      required
                      :disabled="loading"
                      class="auth-input pl-10 pr-11"
                      placeholder="Ulangi kata sandi"
                    />
                    <button
                      type="button"
                      @click="showConfirmPassword = !showConfirmPassword"
                      :disabled="loading"
                      class="auth-visibility-button"
                      :aria-label="showConfirmPassword ? 'Sembunyikan konfirmasi kata sandi' : 'Tampilkan konfirmasi kata sandi'"
                    >
                      <EyeOff v-if="showConfirmPassword" class="h-4 w-4" />
                      <Eye v-else class="h-4 w-4" />
                    </button>
                  </div>
                </div>

                <p class="pt-0.5 text-[11px] leading-5 text-slate-400">
                  Kata sandi harus terdiri dari minimal 8 karakter.
                </p>

                <button
                  type="submit"
                  :disabled="loading"
                  class="auth-submit mt-1"
                >
                  <LoaderCircle v-if="loading" class="h-4 w-4 animate-spin" />
                  <span>{{ loading ? "Membuat akun..." : "Daftar" }}</span>
                  <ArrowRight v-if="!loading" class="h-4 w-4" />
                </button>
              </form>

              <div class="mt-5 flex items-start gap-2 rounded-xl bg-slate-50 px-3.5 py-3 text-[11px] leading-5 text-slate-500">
                <Microscope class="mt-0.5 h-4 w-4 shrink-0 text-emerald-700" />
                <p>
                  Data simulasi digunakan dalam pengujian implementasi metode. Keluaran sistem tidak dimaksudkan sebagai pengganti pengukuran dan rekomendasi pemupukan lapangan.
                </p>
              </div>
            </div>
          </Transition>
        </div>
      </div>

      <aside class="auth-side relative flex min-h-[240px] items-center justify-center overflow-hidden px-8 py-10 text-center text-white sm:min-h-[260px] lg:min-h-0 lg:px-10">
        <div class="auth-side-orbit auth-side-orbit-one" />
        <div class="auth-side-orbit auth-side-orbit-two" />
        <div class="relative z-10 mx-auto max-w-[290px]">
          <div class="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-2xl border border-white/20 bg-white/10">
            <Leaf class="h-6 w-6 text-white" />
          </div>
          <p class="text-2xl font-bold tracking-tight sm:text-[27px]">Selamat datang!</p>
          <p class="mx-auto mt-3 max-w-[250px] text-sm leading-6 text-emerald-50/90">
            Sudah memiliki akun? Masuk kembali untuk melanjutkan akses ke data simulasi dan hasil pengujian penelitian.
          </p>
          <RouterLink to="/login" class="auth-side-button mt-6">
            Masuk
            <ArrowRight class="h-4 w-4" />
          </RouterLink>
          <p class="mt-7 text-[10px] leading-4 text-emerald-100/65">
            Sistem penelitian implementasi Fuzzy Tsukamoto untuk monitoring kondisi tanah dan pengujian rekomendasi pemupukan Durian Montong.
          </p>
        </div>
      </aside>
    </section>
  </main>
</template>

<style scoped>
.auth-page {
  background:
    radial-gradient(ellipse at 12% 10%, rgba(167, 243, 208, 0.25), transparent 34%),
    #f5f8f6;
}

.auth-shell {
  isolation: isolate;
}

.auth-side {
  background: linear-gradient(118deg, #123d31 0%, #155342 58%, #17634c 100%);
}

.auth-side::before {
  content: "";
  position: absolute;
  z-index: 1;
  display: none;
  top: -13%;
  left: -142px;
  width: 220px;
  height: 126%;
  border-radius: 50%;
  background: #fff;
}

.auth-side-orbit {
  position: absolute;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 9999px;
  pointer-events: none;
}

.auth-side-orbit-one {
  width: 330px;
  height: 330px;
  top: -170px;
  right: -120px;
}

.auth-side-orbit-two {
  width: 250px;
  height: 250px;
  bottom: -160px;
  left: -110px;
}

.auth-input-wrap {
  position: relative;
}

.auth-input-icon {
  position: absolute;
  left: 13px;
  top: 50%;
  width: 16px;
  height: 16px;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none;
  transition: color 160ms ease;
}

.auth-input-wrap:focus-within .auth-input-icon {
  color: #047857;
}

.auth-input {
  display: block;
  width: 100%;
  min-height: 42px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #f4f4f6;
  padding-top: 9px;
  padding-bottom: 9px;
  padding-right: 12px;
  color: #1f2937;
  font-size: 13px;
  outline: none;
  transition: border-color 160ms ease, background 160ms ease, box-shadow 160ms ease;
}

.auth-input::placeholder {
  color: #a1a1aa;
}

.auth-input:hover {
  border-color: #d4d4dc;
}

.auth-input:focus {
  border-color: #059669;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.12);
}

.auth-input:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}

.auth-visibility-button {
  position: absolute;
  top: 50%;
  right: 8px;
  display: flex;
  width: 30px;
  height: 30px;
  transform: translateY(-50%);
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  color: #9ca3af;
  transition: background 160ms ease, color 160ms ease;
}

.auth-visibility-button:hover {
  background: #e5e7eb;
  color: #374151;
}

.auth-visibility-button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.auth-submit {
  display: flex;
  width: 100%;
  min-height: 43px;
  align-items: center;
  justify-content: center;
  gap: 9px;
  border-radius: 10px;
  background: linear-gradient(100deg, #123d31, #17634c);
  padding: 10px 16px;
  color: white;
  font-size: 13px;
  font-weight: 700;
  box-shadow: 0 7px 16px rgba(15, 65, 48, 0.18);
  transition: transform 160ms ease, box-shadow 160ms ease, opacity 160ms ease;
}

.auth-submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 10px 20px rgba(15, 65, 48, 0.23);
}

.auth-submit:focus-visible,
.auth-side-button:focus-visible,
.auth-visibility-button:focus-visible {
  outline: 3px solid rgba(110, 231, 183, 0.55);
  outline-offset: 3px;
}

.auth-submit:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.auth-side-button {
  display: inline-flex;
  min-height: 38px;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: 1px solid rgba(255, 255, 255, 0.45);
  border-radius: 9px;
  padding: 8px 20px;
  color: white;
  font-size: 12px;
  font-weight: 700;
  transition: background 160ms ease, transform 160ms ease;
}

.auth-side-button:hover {
  transform: translateY(-1px);
  background: rgba(255, 255, 255, 0.12);
}

.auth-feedback-enter-active,
.auth-feedback-leave-active {
  transition: opacity 180ms ease, transform 180ms ease;
}

.auth-feedback-enter-from,
.auth-feedback-leave-to {
  opacity: 0;
  transform: translateY(6px);
}

@media (min-width: 1024px) {
  .auth-side::before {
    display: block;
  }
}

@media (prefers-reduced-motion: reduce) {
  .auth-input,
  .auth-input-icon,
  .auth-visibility-button,
  .auth-submit,
  .auth-side-button,
  .auth-feedback-enter-active,
  .auth-feedback-leave-active {
    transition: none;
  }

  .auth-feedback-enter-from,
  .auth-feedback-leave-to {
    transform: none;
  }
}
</style>
