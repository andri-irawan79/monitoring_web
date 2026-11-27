<script setup>
import { LoaderCircle, Sprout, CalendarDays, ArrowRight, CheckCircle2 } from "lucide-vue-next";

defineProps({
  fases: { type: Array, default: () => [] },
  selectedFase: { type: Number, required: true },
  loading: { type: Boolean, default: false },
  initialLoading: { type: Boolean, default: false }
});

const emit = defineEmits(["generate", "update:selectedFase"]);
</script>

<template>
  <section class="flex h-full flex-col overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-[0_8px_28px_-20px_rgba(15,23,42,.28)]">
    <div class="border-b border-slate-100 bg-gradient-to-br from-emerald-50 via-white to-lime-50/70 px-5 py-5 sm:px-6">
      <div class="flex items-start gap-3">
        <span class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700 shadow-sm">
          <Sprout class="h-5 w-5" />
        </span>
        <div class="min-w-0">
          <div class="flex flex-wrap items-center gap-2">
            <h2 class="text-lg font-bold tracking-tight text-slate-900">Parameter Rekomendasi</h2>
            <span class="rounded-full bg-emerald-100 px-2 py-0.5 text-[9px] font-extrabold uppercase tracking-wider text-emerald-800">Langkah 1</span>
          </div>
          <p class="mt-1 text-xs leading-5 text-slate-500">Pastikan data tanah tersedia, lalu tentukan fase pertumbuhan tanaman.</p>
        </div>
      </div>
    </div>

    <div class="flex flex-1 flex-col p-5 sm:p-6">
      <div class="space-y-6">
        <div>
          <div class="mb-2 flex items-center justify-between gap-2">
            <label class="text-xs font-bold uppercase tracking-[0.12em] text-slate-500">Objek tanaman</label>
            <span class="inline-flex items-center gap-1 text-[10px] font-semibold text-emerald-700">
              <CheckCircle2 class="h-3.5 w-3.5" /> Objek penelitian
            </span>
          </div>
          <div class="flex min-h-[68px] items-center gap-3 rounded-xl border border-emerald-100 bg-emerald-50/55 px-4 py-3">
            <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-emerald-700 shadow-sm">
              <Sprout class="h-5 w-5" />
            </span>
            <div class="min-w-0">
              <p class="text-sm font-bold text-slate-900">Durian Montong</p>
              <p class="mt-0.5 text-[11px] text-slate-500">Varietas tetap pada penelitian ini</p>
            </div>
          </div>
        </div>

        <div>
          <label class="mb-2 block text-xs font-bold uppercase tracking-[0.12em] text-slate-500" for="fase-pertumbuhan">Fase pertumbuhan</label>
          <div class="relative">
            <CalendarDays class="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-emerald-700" />
            <select
              id="fase-pertumbuhan"
              class="min-h-12 w-full appearance-none rounded-xl border border-slate-200 bg-white py-3 pl-10 pr-10 text-sm font-semibold text-slate-700 outline-none transition hover:border-emerald-300 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-50"
              :value="selectedFase"
              :disabled="initialLoading || loading || !fases.length"
              @change="emit('update:selectedFase', Number($event.target.value))"
            >
              <option v-for="fase in fases" :key="fase.id" :value="fase.id">{{ fase.nama }}</option>
            </select>
            <span class="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">⌄</span>
          </div>
          <p class="mt-2 text-xs leading-5 text-slate-400">Pilih fase yang sesuai dengan kondisi tanaman: pascapanen, vegetatif, prapembungaan, pembuahan, atau prapanen.</p>
        </div>
      </div>

      <div class="mt-auto pt-7">
        <button
          type="button"
          @click="emit('generate')"
          :disabled="loading || initialLoading || !fases.length"
          class="group inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-xl bg-emerald-700 px-5 py-3 text-sm font-bold text-white shadow-[0_8px_18px_-10px_rgba(4,120,87,.8)] transition duration-200 hover:-translate-y-0.5 hover:bg-emerald-800 hover:shadow-lg disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2"
        >
          <LoaderCircle v-if="loading" class="h-4 w-4 animate-spin" />
          <span>{{ loading ? "Sedang Menghitung..." : "Buat Rekomendasi" }}</span>
          <ArrowRight v-if="!loading" class="h-4 w-4 transition-transform group-hover:translate-x-1" />
        </button>
        <p class="mt-3 text-center text-[10px] leading-5 text-slate-400">Perhitungan menggunakan data monitoring terakhir dan metode Fuzzy Tsukamoto.</p>
      </div>
    </div>
  </section>
</template>
