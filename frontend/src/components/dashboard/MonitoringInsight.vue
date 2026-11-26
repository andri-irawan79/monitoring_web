<script setup>
import { BarChart3 } from "lucide-vue-next";

defineProps({
  monitoring: { type: Object, default: () => ({}) },
  summary: { type: Object, default: () => ({}) }
});

const metrics = [
  { key: "avg_nitrogen", label: "Rata-rata Nitrogen", short: "N", unit: "ppm", tone: "emerald" },
  { key: "avg_phosphorus", label: "Rata-rata Fosfor", short: "P", unit: "ppm", tone: "blue" },
  { key: "avg_potassium", label: "Rata-rata Kalium", short: "K", unit: "ppm", tone: "amber" },
  { key: "avg_ph", label: "Rata-rata pH", short: "pH", unit: "skala pH", tone: "violet" }
];

const tones = {
  emerald: "border-emerald-100 bg-emerald-50/80 text-emerald-900",
  blue: "border-blue-100 bg-blue-50/80 text-blue-900",
  amber: "border-amber-100 bg-amber-50/80 text-amber-900",
  violet: "border-violet-100 bg-violet-50/80 text-violet-900"
};
</script>

<template>
  <section class="overflow-hidden rounded-2xl border border-slate-200/80 bg-white p-4 shadow-[0_3px_18px_-12px_rgba(15,23,42,.25)] sm:p-5">
    <div class="grid gap-4 lg:grid-cols-[minmax(205px,.72fr)_minmax(0,2.28fr)] lg:items-stretch">
      <div class="flex items-center gap-3 border-b border-slate-100 pb-4 lg:border-b-0 lg:border-r lg:pb-0 lg:pr-5">
        <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-700">
          <BarChart3 class="h-5 w-5" />
        </div>
        <div class="min-w-0">
          <h2 class="text-base font-bold tracking-tight text-slate-900">Insight Monitoring</h2>
          <p class="mt-1 text-xs leading-5 text-slate-500">Ringkasan rata-rata dari seluruh data tersimpan</p>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-2.5 sm:grid-cols-4">
        <article
          v-for="item in metrics"
          :key="item.key"
          class="flex min-h-[116px] min-w-0 flex-col rounded-xl border p-3 sm:p-3.5"
          :class="tones[item.tone]"
        >
          <div class="flex items-center justify-between gap-2">
            <span class="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-white/80 text-[11px] font-extrabold shadow-sm">
              {{ item.short }}
            </span>
            <span class="text-[9px] font-bold uppercase tracking-[0.12em] opacity-50">Rata-rata</span>
          </div>
          <p class="mt-2 min-h-[2rem] text-[10px] font-semibold leading-4 opacity-75 sm:text-[11px]">
            {{ item.label }}
          </p>
          <div class="mt-auto flex items-baseline gap-1.5">
            <p class="truncate text-lg font-extrabold leading-none tracking-tight tabular-nums sm:text-xl">
              {{ summary[item.key] ?? "-" }}
            </p>
            <span class="shrink-0 text-[9px] font-medium opacity-60">{{ item.unit }}</span>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>
