<script setup>
import BaseCard from "../ui/BaseCard.vue";
import { Sprout, LoaderCircle, ClipboardList, CheckCircle2, Scale, Leaf, Sparkles } from "lucide-vue-next";

defineProps({
  recommendation: { type: Object, default: null },
  initialLoading: { type: Boolean, default: false }
});

function badgeClass(kategori) {
  if (!kategori) return "bg-slate-100 text-slate-700 ring-1 ring-inset ring-slate-200";
  const value = kategori.toLowerCase();
  if (value === "tinggi") return "bg-rose-50 text-rose-700 ring-1 ring-inset ring-rose-200";
  if (value === "sedang") return "bg-amber-50 text-amber-700 ring-1 ring-inset ring-amber-200";
  return "bg-emerald-50 text-emerald-700 ring-1 ring-inset ring-emerald-200";
}
</script>

<template>
  <BaseCard class="h-full overflow-hidden !p-0 shadow-[0_8px_28px_-20px_rgba(15,23,42,.28)]">
    <div class="flex items-center gap-3 border-b border-slate-100 bg-gradient-to-br from-emerald-50 via-white to-lime-50/70 px-5 py-5 sm:px-6">
      <span class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700 shadow-sm">
        <ClipboardList class="h-5 w-5" />
      </span>
      <div class="min-w-0">
        <div class="flex flex-wrap items-center gap-2">
          <h2 class="text-lg font-bold tracking-tight text-slate-900">Hasil Rekomendasi</h2>
          <span class="rounded-full bg-emerald-100 px-2 py-0.5 text-[9px] font-extrabold uppercase tracking-wider text-emerald-800">Langkah 2</span>
        </div>
        <p class="mt-0.5 text-xs text-slate-500">Hasil perhitungan pemupukan Durian Montong</p>
      </div>
      <span v-if="recommendation" class="ml-auto inline-flex shrink-0 items-center gap-1 rounded-full bg-emerald-50 px-2.5 py-1 text-[10px] font-bold text-emerald-700 ring-1 ring-inset ring-emerald-100">
        <CheckCircle2 class="h-3.5 w-3.5" /> Selesai
      </span>
    </div>

    <div class="flex min-h-[330px] flex-col justify-center p-5 sm:p-6">
      <div v-if="initialLoading" class="flex min-h-64 flex-col items-center justify-center py-10 text-center">
        <LoaderCircle class="h-8 w-8 animate-spin text-emerald-600" />
        <p class="mt-3 text-sm font-medium text-slate-600">Memuat hasil rekomendasi...</p>
      </div>

      <div v-else-if="recommendation" class="space-y-4">
        <div class="relative overflow-hidden rounded-2xl border border-emerald-200/80 bg-gradient-to-br from-emerald-50 via-white to-lime-50 p-4 sm:p-5">
          <div class="pointer-events-none absolute -right-8 -top-10 h-36 w-36 rounded-full bg-emerald-200/30 blur-2xl"></div>
          <div class="relative">
            <div class="flex items-center gap-2 text-[10px] font-extrabold uppercase tracking-[0.15em] text-emerald-800/70">
              <Sparkles class="h-3.5 w-3.5" /> Jenis pupuk yang disarankan
            </div>
            <div class="mt-3 flex items-center gap-3">
              <span class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-white text-emerald-700 shadow-sm ring-1 ring-emerald-100">
                <Leaf class="h-6 w-6" />
              </span>
              <h3 class="min-w-0 text-xl font-extrabold leading-tight tracking-tight text-emerald-950 sm:text-2xl">
                {{ recommendation.jenis_pupuk }}
              </h3>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div class="rounded-xl border border-slate-200 bg-slate-50/80 p-4">
            <div class="flex items-center gap-2 text-slate-500">
              <Scale class="h-4 w-4" />
              <span class="text-xs font-semibold">Dosis pemupukan</span>
            </div>
            <p class="mt-3 text-2xl font-extrabold tracking-tight text-slate-900 tabular-nums">
              {{ recommendation.dosis }}
              <span class="text-xs font-bold text-slate-500">kg/pohon</span>
            </p>
          </div>
          <div class="rounded-xl border border-slate-200 bg-slate-50/80 p-4">
            <p class="text-xs font-semibold text-slate-500">Kategori kebutuhan</p>
            <span class="mt-3 inline-flex rounded-full px-3 py-1.5 text-sm font-bold" :class="badgeClass(recommendation.kategori)">
              {{ recommendation.kategori || "Belum tersedia" }}
            </span>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-x-4 gap-y-3 border-t border-slate-100 pt-4 text-sm">
          <div>
            <p class="text-[10px] font-semibold uppercase tracking-wider text-slate-400">Objek tanaman</p>
            <p class="mt-1 font-bold text-slate-700">{{ recommendation.objek_tanaman || "Durian Montong" }}</p>
          </div>
          <div>
            <p class="text-[10px] font-semibold uppercase tracking-wider text-slate-400">Fase pertumbuhan</p>
            <p class="mt-1 font-bold text-slate-700">{{ recommendation.fase || "-" }}</p>
          </div>
          <div class="col-span-2">
            <p class="text-[10px] font-semibold uppercase tracking-wider text-slate-400">Tanggal perhitungan</p>
            <p class="mt-1 font-semibold text-slate-700">{{ recommendation.created_at }}</p>
          </div>
        </div>
      </div>

      <div v-else class="flex min-h-64 flex-col items-center justify-center rounded-2xl border border-dashed border-emerald-200 bg-gradient-to-br from-emerald-50/70 to-slate-50 px-5 py-9 text-center">
        <div class="flex h-14 w-14 items-center justify-center rounded-2xl bg-white text-emerald-700 shadow-sm ring-1 ring-emerald-100">
          <Sprout class="h-7 w-7" />
        </div>
        <h3 class="mt-4 text-base font-bold text-slate-800">Siap menghasilkan rekomendasi</h3>
        <p class="mt-2 max-w-sm text-sm leading-relaxed text-slate-500">
          Tentukan fase pertumbuhan pada panel parameter, lalu tekan
          <span class="font-semibold text-emerald-800">Buat Rekomendasi</span> untuk memulai perhitungan.
        </p>
      </div>
    </div>
  </BaseCard>
</template>
