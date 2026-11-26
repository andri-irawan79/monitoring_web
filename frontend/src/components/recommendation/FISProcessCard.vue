<script setup>
import BaseCard from "../ui/BaseCard.vue";

defineProps({
  fis1: { type: Object, default: () => ({}) },
  fis2: { type: Object, default: () => ({}) },
  zValues: { type: Object, default: () => ({}) },
  targetHara: { type: Object, default: () => ({}) },
  remainingHara: { type: Object, default: () => ({}) },
  doses: { type: Object, default: () => ({}) },
  corrections: { type: Object, default: () => ({}) }
});

const variables = ["N", "P", "K"];
const products = [
  { key: "urea", label: "Urea" },
  { key: "sp36", label: "SP-36" },
  { key: "kcl", label: "KCl" },
  { key: "npk", label: "NPK 16-16-16" }
];

function fmt(value, digits = 2) {
  if (value === null || value === undefined || value === "") return "-";
  const number = Number(value);
  return Number.isFinite(number) ? number.toFixed(digits) : "-";
}
</script>

<template>
  <BaseCard class="space-y-5">
    <div>
      <h2 class="text-lg font-extrabold text-slate-900">Rincian proses Fuzzy Tsukamoto</h2>
      <p class="mt-1 text-sm text-slate-500">Inferensi FIS-1 untuk unsur hara dan FIS-2 untuk koreksi pH.</p>
    </div>

    <section>
      <div class="mb-3 flex items-center justify-between gap-2">
        <h3 class="font-bold text-slate-800">FIS-1 · Kebutuhan N, P, dan K</h3>
        <span class="text-xs text-slate-500">Prioritas fase + status hara</span>
      </div>
      <div class="grid gap-3 md:grid-cols-3">
        <article v-for="variable in variables" :key="variable" class="rounded-xl border border-slate-200 bg-slate-50/70 p-4">
          <div class="flex items-center justify-between">
            <span class="text-sm font-extrabold text-slate-800">{{ variable }}</span>
            <span class="rounded-lg bg-white px-2 py-1 text-xs font-bold text-emerald-800 ring-1 ring-slate-200">
              Z akhir = {{ fmt(fis1[variable]?.z) }}
            </span>
          </div>
          <p class="mt-2 text-xs text-slate-500">Prioritas: <strong class="capitalize text-slate-700">{{ fis1[variable]?.priority || "-" }}</strong></p>
          <div class="mt-3 space-y-1.5 text-xs">
            <div v-for="(degree, label) in (fis1[variable]?.membership || {})" :key="label" class="flex justify-between gap-2">
              <span class="capitalize text-slate-500">{{ label }}</span>
              <strong class="tabular-nums text-slate-700">{{ fmt(degree, 4) }}</strong>
            </div>
          </div>
          <div class="mt-3 flex flex-wrap gap-2 border-t border-slate-200 pt-3 text-[10px] text-slate-500">
            <span>Raw Z: <strong class="text-slate-700">{{ fmt(fis1[variable]?.raw_z, 4) }}</strong></span>
            <span>Σα: <strong class="text-slate-700">{{ fmt(fis1[variable]?.denominator, 4) }}</strong></span>
            <span>Σ(αz): <strong class="text-slate-700">{{ fmt(fis1[variable]?.numerator, 4) }}</strong></span>
          </div>
        </article>
      </div>
    </section>

    <section class="border-t border-slate-100 pt-5">
      <div class="mb-3 flex items-center justify-between gap-2">
        <h3 class="font-bold text-slate-800">FIS-2 · Koreksi pH tanah</h3>
        <span class="text-xs text-slate-500">Masam · Normal · Basa</span>
      </div>
      <div class="grid gap-3 sm:grid-cols-2">
        <article v-for="key in ['dolomit', 'belerang']" :key="key" class="rounded-xl border border-slate-200 p-4">
          <p class="text-sm font-bold capitalize text-slate-800">{{ key === "dolomit" ? "Kapur Dolomit" : "Belerang" }}</p>
          <p class="mt-1 text-xs text-slate-500">Z akhir: <strong class="text-emerald-800">{{ fmt(fis2.outputs?.[key]?.z) }}</strong></p>
          <div class="mt-3 flex flex-wrap gap-2 text-xs">
            <span class="rounded-lg bg-slate-50 px-2.5 py-1.5">Raw Z = {{ fmt(fis2.outputs?.[key]?.raw_z, 4) }}</span>
            <span class="rounded-lg bg-slate-50 px-2.5 py-1.5">Σα = {{ fmt(fis2.outputs?.[key]?.denominator, 4) }}</span>
            <span class="rounded-lg bg-slate-50 px-2.5 py-1.5">Σ(αz) = {{ fmt(fis2.outputs?.[key]?.numerator, 4) }}</span>
          </div>
        </article>
      </div>
    </section>

    <section class="border-t border-slate-100 pt-5">
      <h3 class="mb-3 font-bold text-slate-800">Konversi kebutuhan hara menjadi dosis</h3>
      <div class="overflow-x-auto rounded-xl border border-slate-200">
        <table class="w-full min-w-[560px] text-sm">
          <thead class="bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th class="px-3 py-3">Unsur</th>
              <th class="px-3 py-3">Z (%)</th>
              <th class="px-3 py-3">Target hara (g)</th>
              <th class="px-3 py-3">Sisa setelah NPK (g)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="key in variables" :key="key">
              <td class="px-3 py-3 font-bold">{{ key }}</td>
              <td class="px-3 py-3 tabular-nums">{{ fmt(zValues[key.toLowerCase()]) }}</td>
              <td class="px-3 py-3 tabular-nums">{{ fmt(targetHara[key]) }}</td>
              <td class="px-3 py-3 tabular-nums">{{ fmt(remainingHara[key]) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="mt-3 grid gap-2 sm:grid-cols-2 xl:grid-cols-4">
        <div v-for="product in products" :key="product.key" class="rounded-xl bg-slate-50 p-3">
          <p class="text-xs text-slate-500">{{ product.label }}</p>
          <p class="mt-1 text-lg font-extrabold tabular-nums text-slate-800">{{ Number(doses[product.key] || 0).toLocaleString("id-ID") }} <span class="text-xs font-semibold text-slate-500">g/pohon</span></p>
        </div>
      </div>
      <p class="mt-3 text-xs leading-5 text-slate-500">
        Defuzzifikasi tiap keluaran menggunakan Z = Σ(α × z) / Σα. Nilai α dengan konsekuen yang sama digabungkan terlebih dahulu dengan batas maksimum 1, mengikuti algoritma proyek acuan.
      </p>
    </section>

    <section class="border-t border-slate-100 pt-5">
      <h3 class="mb-3 font-bold text-slate-800">Rentang bahan koreksi pH</h3>
      <div class="grid gap-3 sm:grid-cols-2">
        <div v-for="key in ['dolomit', 'belerang']" :key="key" class="rounded-xl border border-slate-200 px-4 py-3">
          <p class="text-xs text-slate-500">{{ key === "dolomit" ? "Kapur Dolomit" : "Belerang" }}</p>
          <p v-if="corrections[key]" class="mt-1 font-bold text-slate-800 tabular-nums">
            {{ corrections[key][0].toLocaleString("id-ID") }}–{{ corrections[key][1].toLocaleString("id-ID") }} g/pohon
          </p>
          <p v-else class="mt-1 font-bold text-slate-500">Tidak diberikan pada fase Panen</p>
        </div>
      </div>
    </section>
  </BaseCard>
</template>
