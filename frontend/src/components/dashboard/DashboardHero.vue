<script setup>
import { Database, ClipboardList, Activity, Clock3, Sprout } from "lucide-vue-next";

defineProps({
  summary: { type: Object, default: () => ({}) },
  lastUpdate: { type: String, default: "" }
});

const today = new Date().toLocaleDateString("id-ID", {
  weekday: "long", day: "numeric", month: "long", year: "numeric"
});
</script>

<template>
  <section class="hero-panel relative isolate overflow-hidden rounded-[1.75rem] bg-[#123d31] text-white shadow-[0_18px_45px_-24px_rgba(15,65,48,0.65)]">
    <div class="hero-orb hero-orb-one"></div>
    <div class="hero-orb hero-orb-two"></div>
    <div class="relative grid gap-8 p-6 sm:p-8 xl:grid-cols-[minmax(0,1.25fr)_minmax(340px,0.75fr)] xl:items-center xl:p-10">
      <div class="max-w-2xl">
        <div class="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-xs font-semibold tracking-wide text-emerald-100 backdrop-blur">
          <Sprout class="h-3.5 w-3.5" /> SISTEM MONITORING DURian MONTONG
        </div>
        <p class="mt-6 text-sm font-medium text-emerald-200">Selamat datang di dashboard</p>
        <h1 class="mt-2 max-w-xl text-3xl font-bold leading-tight tracking-tight sm:text-4xl xl:text-[2.7rem]">
          Pantau kondisi tanah, <span class="text-emerald-300">rawat kualitas durian.</span>
        </h1>
        <p class="mt-4 max-w-xl text-sm leading-7 text-emerald-50/75 sm:text-base">
          Ringkasan nutrisi tanah dan perkembangan data simulasi untuk mendukung rekomendasi pemupukan dengan metode Fuzzy Tsukamoto.
        </p>
        <div class="mt-6 flex flex-wrap items-center gap-x-5 gap-y-2 text-xs text-emerald-100/75">
          <span>{{ today }}</span>
          <span v-if="lastUpdate" class="inline-flex items-center gap-1.5"><Clock3 class="h-3.5 w-3.5" /> Diperbarui {{ lastUpdate }}</span>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div class="hero-stat rounded-2xl border border-white/10 bg-white/[0.09] p-4 backdrop-blur-sm sm:p-5">
          <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-300/15 text-emerald-200"><Database class="h-5 w-5" /></div>
          <p class="mt-5 text-xs font-medium text-emerald-100/70">Total monitoring</p>
          <p class="mt-1 text-3xl font-bold tracking-tight tabular-nums">{{ summary.total_monitoring ?? 0 }}</p>
          <p class="mt-1 text-[11px] text-emerald-100/55">Data tersimpan</p>
        </div>
        <div class="hero-stat rounded-2xl border border-white/10 bg-white/[0.09] p-4 backdrop-blur-sm sm:p-5">
          <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-lime-300/15 text-lime-200"><ClipboardList class="h-5 w-5" /></div>
          <p class="mt-5 text-xs font-medium text-emerald-100/70">Total rekomendasi</p>
          <p class="mt-1 text-3xl font-bold tracking-tight tabular-nums">{{ summary.total_recommendation ?? 0 }}</p>
          <p class="mt-1 text-[11px] text-emerald-100/55">Hasil perhitungan</p>
        </div>
        <div class="col-span-2 flex items-center gap-3 rounded-2xl border border-emerald-200/15 bg-emerald-300/10 p-4">
          <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-300/15 text-emerald-200"><Activity class="h-5 w-5" /></div>
          <div class="min-w-0">
            <p class="text-sm font-semibold">Sumber data simulasi</p>
            <p class="mt-0.5 text-xs text-emerald-100/65">Backend FastAPI terhubung · Bukan pembacaan sensor langsung</p>
          </div>
          <span class="ml-auto h-2.5 w-2.5 shrink-0 rounded-full bg-emerald-300 shadow-[0_0_0_5px_rgba(110,231,183,0.12)]"></span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero-panel { background-image: linear-gradient(118deg, #123d31 0%, #155342 58%, #17634c 100%); }
.hero-orb { position:absolute; z-index:-1; border-radius:9999px; pointer-events:none; }
.hero-orb-one { width:26rem;height:26rem;right:22%;top:-19rem;background:rgba(110,231,183,.13);filter:blur(2px); }
.hero-orb-two { width:22rem;height:22rem;right:-9rem;bottom:-15rem;background:rgba(190,242,100,.10);filter:blur(3px); }
.hero-stat { transition:transform .2s ease, background-color .2s ease; }
.hero-stat:hover { transform:translateY(-3px); background-color:rgba(255,255,255,.13); }
@media (prefers-reduced-motion: reduce) { .hero-stat { transition:none; } .hero-stat:hover { transform:none; } }
</style>