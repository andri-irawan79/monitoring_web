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
  CircleAlert,
  Microscope
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
  <main class="auth-page flex min-h-screen items-center justify-center px-4 py-8 sm:px-6">
    <section class="auth-shell grid w-full max-w-[980px] grid-cols-1 overflow-hidden rounded-[28px] bg-white shadow-[0_24px_70px_-28px_rgba(30,35,70,0.38)] lg:min-h-[570px] lg:grid-cols-[1.08fr_0.92fr]">
      <div class="flex items-center px-6 py-9 sm:px-10 sm:py-12 lg:px-12">
        <div class="mx-auto w-full max-w-[370px]">
          <div class="mb-8 flex items-center justify-center gap-2 lg:justify-start">
            <div class="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-100 text-emerald-800">
              <Leaf class="h-5 w-5" />
            </div>
            <div>
              <p class="text-sm font-bold tracking-tight text-slate-800">Monitoring Tanah Durian</p>
              <p class="text-[11px] text-slate-400">Sistem pendukung penelitian</p>
            </div>
          </div>

          <div class="mb-6 text-center lg:text-left">
            <p class="mb-2 text-[11px] font-bold uppercase tracking-[0.2em] text-emerald-700">
              Selamat datang kembali
            </p>
            <h1 class="text-3xl font-bold tracking-tight text-slate-900">Masuk</h1>
            <p class="mt-2 text-sm leading-6 text-slate-500">
              Masuk untuk mengakses data simulasi, riwayat pengujian, dan keluaran sistem penelitian.
            </p>
          </div>

          <div
            v-if="registeredMessage"
            class="mb-4 flex items-start gap-2.5 rounded-xl border border-emerald-200 bg-emerald-50 px-3.5 py-3 text-sm leading-5 text-emerald-800"
            role="status"
            aria-live="polite"
          >
            <CheckCircle2 class="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" />
            <span>{{ registeredMessage }}</span>
          </div>

          <div
            v-if="expiredMessage"
            class="mb-4 flex items-start gap-2.5 rounded-xl border border-amber-200 bg-amber-50 px-3.5 py-3 text-sm leading-5 text-amber-800"
            role="status"
          >
            <CircleAlert class="mt-0.5 h-4 w-4 shrink-0 text-amber-600" />
            <span>{{ expiredMessage }}</span>
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

          <form class="space-y-4" @submit.prevent="submitLogin">
            <div>
              <label for="email" class="mb-1.5 block text-xs font-semibold text-slate-700">Email</label>
              <div class="auth-input-wrap">
                <Mail class="auth-input-icon" />
                <input
                  id="email"
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
              <label for="password" class="mb-1.5 block text-xs font-semibold text-slate-700">Kata Sandi</label>
              <div class="auth-input-wrap">
                <Lock class="auth-input-icon" />
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  autocomplete="current-password"
                  required
                  :disabled="loading"
                  class="auth-input pl-10 pr-11"
                  placeholder="Masukkan kata sandi"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  :disabled="loading"
                  class="absolute right-2 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-lg text-slate-400 transition hover:bg-slate-200/70 hover:text-slate-700 disabled:opacity-50"
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
              class="auth-submit mt-2"
            >
              <LoaderCircle v-if="loading" class="h-4 w-4 animate-spin" />
              <span>{{ loading ? "Memverifikasi akun..." : "Masuk" }}</span>
              <ArrowRight v-if="!loading" class="h-4 w-4" />
            </button>
          </form>

          <div class="mt-7 flex items-start gap-2 rounded-xl bg-slate-50 px-3.5 py-3 text-[11px] leading-5 text-slate-500">
            <Microscope class="mt-0.5 h-4 w-4 shrink-0 text-emerald-700" />
            <p>
              Penelitian menggunakan data simulasi. Keluaran sistem merupakan hasil pengujian metode, bukan rekomendasi pemupukan lapangan yang telah divalidasi.
            </p>
          </div>
        </div>
      </div>

      <aside class="auth-side relative flex min-h-[250px] items-center justify-center overflow-hidden px-8 py-10 text-center text-white sm:min-h-[275px] lg:min-h-0 lg:px-10">
        <div class="auth-side-orbit auth-side-orbit-one" />
        <div class="auth-side-orbit auth-side-orbit-two" />
        <div class="relative z-10 mx-auto max-w-[290px]">
          <div class="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-2xl border border-white/20 bg-white/10">
            <Leaf class="h-6 w-6 text-white" />
          </div>
          <p class="text-2xl font-bold tracking-tight sm:text-[27px]">Halo, Peneliti!</p>
          <p class="mx-auto mt-3 max-w-[250px] text-sm leading-6 text-emerald-50/90">
            Belum memiliki akun? Daftarkan akun untuk mengakses data simulasi dan meninjau proses pengujian Fuzzy Tsukamoto.
          </p>
          <RouterLink to="/register" class="auth-side-button mt-6">
            Daftar akun
            <ArrowRight class="h-4 w-4" />
          </RouterLink>
          <p class="mt-7 text-[10px] leading-4 text-emerald-100/65">
            Implementasi dan evaluasi metode pada sistem monitoring kondisi tanah Durian Montong.
          </p>
        </div>
      </aside>
    </section>
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
            <CheckCircle2 class="h-9 w-9 text-emerald-700" />
          </div>

          <p class="mt-6 text-[11px] font-bold uppercase tracking-[0.18em] text-emerald-700">
            Autentikasi Berhasil
          </p>
          <h2 class="mt-2 text-xl font-bold tracking-tight text-slate-900">
            Berhasil masuk!
          </h2>
          <p class="mt-2 text-sm leading-6 text-slate-500">
            Menyiapkan halaman sistem penelitian Anda.
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
  min-height: 43px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #f4f4f6;
  padding-top: 10px;
  padding-bottom: 10px;
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
.auth-side-button:focus-visible {
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

@media (min-width: 1024px) {
  .auth-side::before {
    display: block;
  }
}

@media (prefers-reduced-motion: reduce) {
  .auth-input,
  .auth-input-icon,
  .auth-submit,
  .auth-side-button,
  .login-transition-enter-active,
  .login-transition-leave-active {
    transition: none;
  }

  .login-progress {
    animation-duration: 0.2s;
  }
}
</style>
