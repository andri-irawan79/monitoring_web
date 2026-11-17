<script setup>
import { computed } from "vue";
import { Database, ClipboardList, Activity, Clock3, Sprout, ArrowUpRight } from "lucide-vue-next";
import { currentUser } from "../../services/authState";
import { RouterLink } from "vue-router";
defineProps({
  summary: { type: Object, default: () => ({}) },
  lastUpdate: { type: String, default: "" }
});
const today = new Date().toLocaleDateString("id-ID", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
const userName = computed(() => currentUser.value?.full_name?.trim() || "Pengguna");
</script>

<template>
  <section class="hero-panel relative isolate overflow-hidden rounded-[1.75rem] bg-[#123d31] text-white shadow-[0_18px_45px_-24px_rgba(15,65,48,0.65)]">
    <div class="hero-orb hero-orb-one"></div><div class="hero-orb hero-orb-two"></div>
    <div class="relative grid gap-8 p-6 sm:p-8 xl:grid-cols-[minmax(0,1.25fr)_minmax(340px,0.75fr)] xl:items-center xl:p-10">
      <div class="max-w-2xl">
        <div class="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-xs font-semibold tracking-wide text-emerald-100 backdrop-blur"><Sprout class="h-3.5 w-3.5" /> SISTEM MONITORING DURIAN MONTONG</div>
        <p class="mt-6 text-sm font-medium text-emerald-200">Selamat datang, {{ userName }}</p>
        <h1 class="mt-2 max-w-xl text-3xl font-bold leading-tight tracking-tight sm:text-4xl xl:text-[2.7rem]">Monitoring kondisi tanah <span class="text-emerald-300">dan rekomendasi pemupukan.</span></h1>
        <p class="mt-4 max-w-xl text-sm leading-7 text-emerald-50/75 sm:text-base">Ringkasan parameter tanah dari data simulasi dan keluaran pengolahan menggunakan metode Fuzzy Tsukamoto.</p>
        <div class="mt-6 flex flex-wrap items-center gap-x-5 gap-y-2 text-xs text-emerald-100/75"><span>{{ today }}</span><span v-if="lastUpdate" class="inline-flex items-center gap-1.5"><Clock3 class="h-3.5 w-3.5" /> Diperbarui {{ lastUpdate }}</span></div>
      </div>
      <div class="grid grid-cols-2 gap-3">
        <RouterLink to="/#monitoring-history" class="hero-stat group rounded-2xl border border-white/10 bg-white/[0.09] p-4 text-left backdrop-blur-sm transition hover:-translate-y-1 hover:bg-white/[0.16] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-200 sm:p-5" aria-label="Lihat riwayat monitoring">
          <div class="flex items-center justify-between"><span class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-300/15 text-emerald-200"><Database class="h-5 w-5" /></span><ArrowUpRight class="h-4 w-4 text-emerald-100/50 transition group-hover:-translate-y-0.5 group-hover:translate-x-0.5" /></div>
          <p class="mt-5 text-xs font-medium text-emerald-100/70">Total monitoring</p><p class="mt-1 text-3xl font-bold tracking-tight tabular-nums">{{ summary.total_monitoring ?? 0 }}</p><p class="mt-1 text-[11px] text-emerald-100/55">Lihat riwayat data</p>
        </RouterLink>
        <RouterLink to="/recommendation#recommendation-history" class="hero-stat group rounded-2xl border border-white/10 bg-white/[0.09] p-4 text-left backdrop-blur-sm transition hover:-translate-y-1 hover:bg-white/[0.16] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-200 sm:p-5" aria-label="Lihat riwayat rekomendasi">
          <div class="flex items-center justify-between"><span class="flex h-10 w-10 items-center justify-center rounded-xl bg-lime-300/15 text-lime-200"><ClipboardList class="h-5 w-5" /></span><ArrowUpRight class="h-4 w-4 text-emerald-100/50 transition group-hover:-translate-y-0.5 group-hover:translate-x-0.5" /></div>
          <p class="mt-5 text-xs font-medium text-emerald-100/70">Total rekomendasi</p><p class="mt-1 text-3xl font-bold tracking-tight tabular-nums">{{ summary.total_recommendation ?? 0 }}</p><p class="mt-1 text-[11px] text-emerald-100/55">Lihat riwayat hasil</p>
        </RouterLink>
        <a
          href="https://www.kaggle.com/datasets/datasetengineer/smart-farming-data-2024-sf24"
          target="_blank"
          rel="noopener noreferrer"
          class="group col-span-2 flex items-center gap-3 rounded-2xl border border-emerald-200/15 bg-emerald-300/10 p-4 text-left transition duration-200 hover:-translate-y-0.5 hover:border-emerald-200/35 hover:bg-emerald-300/[0.16] hover:shadow-[0_10px_24px_-16px_rgba(110,231,183,0.55)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-200 focus-visible:ring-offset-2 focus-visible:ring-offset-[#155342]"
          aria-label="Buka sumber dataset simulasi di Kaggle pada tab baru"
        >
          <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-300/15 text-emerald-200 transition group-hover:bg-emerald-200/20 group-hover:text-emerald-100">
            <Activity class="h-5 w-5" />
          </span>
          <span class="min-w-0 flex-1">
            <span class="block text-sm font-semibold text-white">Sumber data simulasi</span>
            <span class="mt-0.5 block text-xs text-emerald-100/65">Parameter disajikan dari data simulasi · Bukan pembacaan sensor langsung</span>
            <span class="mt-1.5 inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-200 transition group-hover:text-white">Lihat dataset di Kaggle</span>
          </span>
          <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-emerald-200/20 bg-white/[0.06] text-emerald-200 transition group-hover:border-emerald-200/40 group-hover:bg-white/15 group-hover:text-white">
            <ArrowUpRight class="h-4 w-4 transition-transform duration-200 group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
          </span>
        </a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero-panel { background-image: linear-gradient(118deg, #123d31 0%, #155342 58%, #17634c 100%); }
.hero-orb { position:absolute; z-index:-1; border-radius:9999px; pointer-events:none; }
.hero-orb-one { width:26rem;height:26rem;right:22%;top:-19rem;background:rgba(110,231,183,.13);filter:blur(2px); }
.hero-orb-two { width:22rem;height:22rem;right:-9rem;bottom:-15rem;background:rgba(190,242,100,.10);filter:blur(3px); }
@media (prefers-reduced-motion: reduce) { .hero-stat { transition:none; } .hero-stat:hover { transform:none; } }
</style>