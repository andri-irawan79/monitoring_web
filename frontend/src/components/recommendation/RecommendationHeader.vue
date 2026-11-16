<script setup>
import { Sprout, FlaskConical, ArrowRight, CheckCircle2 } from "lucide-vue-next";
</script>

<template>
  <header class="recommendation-hero relative isolate mb-6 overflow-hidden rounded-[1.75rem] border border-emerald-950/10 px-5 py-6 text-white shadow-[0_18px_45px_-24px_rgba(15,65,48,.65)] sm:px-8 sm:py-8 xl:px-9 xl:py-9">
    <div class="hero-glow hero-glow-one"></div>
    <div class="hero-glow hero-glow-two"></div>

    <div class="relative grid gap-8 xl:grid-cols-[minmax(0,1.2fr)_minmax(290px,.8fr)] xl:items-center">
      <div class="max-w-2xl">
        <div class="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-[10px] font-bold uppercase tracking-[0.16em] text-emerald-100 backdrop-blur sm:text-[11px]">
          <Sprout class="h-3.5 w-3.5" />
          Sistem Pendukung Keputusan
        </div>

        <p class="mt-5 text-xs font-semibold uppercase tracking-[0.18em] text-emerald-200">Durian Montong · Pemupukan terarah</p>
        <h1 class="mt-2 text-2xl font-extrabold leading-tight tracking-tight sm:text-3xl lg:text-4xl">
          Rekomendasi Pemupukan
          <span class="block text-emerald-200">berdasarkan kondisi tanah.</span>
        </h1>
        <p class="mt-4 max-w-xl text-sm leading-7 text-emerald-50/80 sm:text-base">
          Pilih fase pertumbuhan tanaman untuk memperoleh rekomendasi jenis dan dosis pupuk melalui metode Fuzzy Tsukamoto.
        </p>

        <div class="mt-6 flex flex-wrap gap-2">
          <span class="inline-flex items-center gap-1.5 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-xs font-semibold text-emerald-50">
            <FlaskConical class="h-3.5 w-3.5" /> Fuzzy Tsukamoto
          </span>
          <span class="inline-flex items-center gap-1.5 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-xs font-semibold text-emerald-50">
            <CheckCircle2 class="h-3.5 w-3.5" /> 5 fase pertumbuhan
          </span>
        </div>
      </div>

      <div class="rounded-2xl border border-white/15 bg-white/[0.08] p-4 shadow-inner backdrop-blur-sm sm:p-5">
        <div class="flex items-center justify-between gap-3">
          <div>
            <p class="text-xs font-bold uppercase tracking-[0.15em] text-emerald-100/70">Alur rekomendasi</p>
            <p class="mt-1 text-sm font-semibold text-white">Dari data menuju keputusan</p>
          </div>
          <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-300/15 text-emerald-200">
            <Sprout class="h-5 w-5" />
          </span>
        </div>

        <div class="mt-5 space-y-3">
          <div class="flex items-center gap-3">
            <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-white/10 text-xs font-extrabold text-emerald-100">01</span>
            <div class="min-w-0 flex-1">
              <p class="text-sm font-semibold text-white">Kondisi tanah</p>
              <p class="text-[11px] leading-5 text-emerald-100/65">N, P, K, dan pH dari data monitoring</p>
            </div>
            <CheckCircle2 class="h-4 w-4 text-emerald-300" />
          </div>
          <div class="ml-4 h-3 border-l border-dashed border-emerald-200/40"></div>
          <div class="flex items-center gap-3">
            <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-white/10 text-xs font-extrabold text-emerald-100">02</span>
            <div class="min-w-0 flex-1">
              <p class="text-sm font-semibold text-white">Fase pertumbuhan</p>
              <p class="text-[11px] leading-5 text-emerald-100/65">Pemilihan fase tanaman durian</p>
            </div>
            <CheckCircle2 class="h-4 w-4 text-emerald-300" />
          </div>
          <div class="ml-4 h-3 border-l border-dashed border-emerald-200/40"></div>
          <div class="flex items-center gap-3">
            <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-lime-300/15 text-xs font-extrabold text-lime-100">03</span>
            <div class="min-w-0 flex-1">
              <p class="text-sm font-semibold text-white">Hasil pemupukan</p>
              <p class="text-[11px] leading-5 text-emerald-100/65">Jenis pupuk dan dosis rekomendasi</p>
            </div>
            <ArrowRight class="h-4 w-4 text-lime-200" />
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.recommendation-hero {
  background: linear-gradient(118deg, #123d31 0%, #155342 58%, #17634c 100%);
}
.hero-glow {
  position: absolute;
  z-index: -1;
  border-radius: 9999px;
  pointer-events: none;
  filter: blur(3px);
}
.hero-glow-one {
  width: 27rem;
  height: 27rem;
  right: 18%;
  top: -22rem;
  background: rgba(110, 231, 183, .14);
}
.hero-glow-two {
  width: 24rem;
  height: 24rem;
  right: -10rem;
  bottom: -17rem;
  background: rgba(190, 242, 100, .1);
}
</style>
