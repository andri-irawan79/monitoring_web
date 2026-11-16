<script setup>
import BaseCard from "../ui/BaseCard.vue";
import { BookOpen, Calculator, ListChecks, Info } from "lucide-vue-next";

defineProps({
  fuzzy: { type: Object, default: () => ({}) },
  rule: { type: Object, default: () => ({}) },
  recommendation: { type: Object, default: () => ({}) },
  defuzzification: { type: Object, default: () => ({}) }
});

const dominantCategory = (obj) => {
  if (!obj) return { label: "-", value: "-" };

  let max = -1;
  let label = "-";
  Object.entries(obj).forEach(([key, value]) => {
    const numericValue = Number(value);
    if (Number.isFinite(numericValue) && numericValue > max) {
      max = numericValue;
      label = key;
    }
  });

  return { label, value: max >= 0 ? max.toFixed(3) : "-" };
};
</script>

<template>
  <BaseCard class="overflow-hidden !p-0">
    <div class="border-b border-slate-100 bg-gradient-to-r from-slate-50 via-white to-emerald-50/60 px-5 py-5 sm:px-6">
      <div class="flex items-center gap-3">
        <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-100 text-emerald-800">
          <BookOpen class="h-5 w-5" />
        </span>
        <div>
          <h2 class="text-lg font-extrabold tracking-tight text-slate-900 sm:text-xl">Penjelasan Hasil Pengolahan</h2>
          <p class="mt-1 text-xs leading-5 text-slate-500">Ringkasan tahapan inferensi berdasarkan masukan dan basis aturan sistem</p>
        </div>
      </div>
    </div>

    <div class="space-y-5 p-5 sm:p-6">
      <section>
        <div class="mb-3 flex items-center gap-2">
          <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-50 text-blue-700">
            <ListChecks class="h-4 w-4" />
          </span>
          <h3 class="text-sm font-bold text-slate-800">Hasil fuzzifikasi</h3>
        </div>

        <div class="grid gap-2 sm:grid-cols-2">
          <div v-for="item in [
            { key: 'N', label: 'Nitrogen', value: fuzzy?.N },
            { key: 'P', label: 'Fosfor', value: fuzzy?.P },
            { key: 'K', label: 'Kalium', value: fuzzy?.K },
            { key: 'PH', label: 'pH tanah', value: fuzzy?.PH }
          ]" :key="item.key" class="flex items-center justify-between gap-3 rounded-xl border border-slate-100 bg-slate-50/70 px-3.5 py-3">
            <div class="min-w-0">
              <p class="text-xs font-semibold text-slate-500">{{ item.label }}</p>
              <p class="mt-0.5 text-sm font-bold capitalize text-slate-800">{{ dominantCategory(item.value).label }}</p>
            </div>
            <span class="shrink-0 rounded-lg bg-white px-2.5 py-1.5 text-xs font-extrabold tabular-nums text-slate-700 ring-1 ring-slate-200">
              μ {{ dominantCategory(item.value).value }}
            </span>
          </div>
        </div>
        <p class="mt-2 text-[11px] leading-5 text-slate-400">Kategori ditampilkan berdasarkan derajat keanggotaan terbesar pada masing-masing parameter.</p>
      </section>

      <section class="border-t border-slate-100 pt-5">
        <div class="mb-3 flex items-center gap-2">
          <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-50 text-amber-700">
            <Calculator class="h-4 w-4" />
          </span>
          <h3 class="text-sm font-bold text-slate-800">Aturan dengan nilai aktivasi terbesar</h3>
        </div>
        <div class="rounded-xl border border-slate-200 bg-white p-4">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="text-sm font-extrabold text-slate-900">Rule R{{ rule?.rule_id ?? "-" }}</span>
            <span class="rounded-lg bg-amber-50 px-2.5 py-1.5 text-xs font-bold text-amber-800 ring-1 ring-amber-100">
              α = {{ rule?.alpha ?? "-" }}
            </span>
          </div>
          <p class="mt-2 text-xs leading-5 text-slate-500">
            Aturan ini memiliki nilai α terbesar di antara aturan yang dievaluasi pada proses perhitungan ini.
          </p>
        </div>
      </section>

      <section class="border-t border-slate-100 pt-5">
        <div class="mb-3 flex items-center gap-2">
          <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-violet-50 text-violet-700">
            <Calculator class="h-4 w-4" />
          </span>
          <h3 class="text-sm font-bold text-slate-800">Defuzzifikasi Tsukamoto</h3>
        </div>
        <div class="rounded-xl bg-slate-50 p-4">
          <p class="text-center text-sm font-bold tracking-wide text-slate-700">z = Σ(α × z) / Σα</p>
          <div class="mt-3 flex flex-wrap items-center justify-center gap-2 text-sm text-slate-600">
            <span class="rounded-lg bg-white px-3 py-2 font-semibold ring-1 ring-slate-200">{{ defuzzification?.alpha_z ?? "-" }}</span>
            <span class="text-slate-400">/</span>
            <span class="rounded-lg bg-white px-3 py-2 font-semibold ring-1 ring-slate-200">{{ defuzzification?.alpha ?? "-" }}</span>
            <span class="text-slate-400">=</span>
            <strong class="text-lg font-extrabold text-emerald-800">{{ defuzzification?.hasil ?? "-" }} kg/pohon</strong>
          </div>
        </div>
      </section>

      <section class="rounded-2xl border border-emerald-100 bg-emerald-50/70 p-4 sm:p-5">
        <p class="text-[10px] font-extrabold uppercase tracking-[0.15em] text-emerald-800/70">Ringkasan keluaran sistem</p>
        <p class="mt-2 text-sm leading-7 text-slate-700">
          Untuk kombinasi parameter masukan dan fase pertumbuhan pada perhitungan ini, proses inferensi dan defuzzifikasi menghasilkan keluaran berupa rekomendasi
          <strong class="font-extrabold text-emerald-950">{{ recommendation?.jenis_pupuk || "-" }}</strong>
          dengan dosis
          <strong class="font-extrabold text-emerald-950">{{ recommendation?.dosis ?? "-" }} kg/pohon</strong>.
          Keluaran tersebut merupakan hasil perhitungan berdasarkan rentang keanggotaan dan basis aturan yang dikonfigurasi pada sistem.
        </p>
      </section>

      <div class="flex items-start gap-2.5 rounded-xl border border-amber-200 bg-amber-50/70 p-3.5 text-xs leading-5 text-amber-900">
        <Info class="mt-0.5 h-4 w-4 shrink-0" />
        <p>
          Hasil ini merupakan keluaran sistem pendukung keputusan, bukan jaminan efektivitas pemupukan atau peningkatan hasil tanaman. Penerapan di lapangan tetap memerlukan pertimbangan agronomis dan pengujian menggunakan data kondisi lahan sebenarnya.
        </p>
      </div>
    </div>
  </BaseCard>
</template>
