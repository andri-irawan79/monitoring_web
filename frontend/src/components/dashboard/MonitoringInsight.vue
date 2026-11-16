<script setup>
import { BarChart3 } from "lucide-vue-next";
defineProps({ monitoring: { type: Object, default: () => ({}) }, summary: { type: Object, default: () => ({}) } });
const metrics = [
  { key: "avg_nitrogen", label: "Rata-rata Nitrogen", short: "N", unit: "mg/kg", tone: "emerald" },
  { key: "avg_phosphorus", label: "Rata-rata Fosfor", short: "P", unit: "mg/kg", tone: "blue" },
  { key: "avg_potassium", label: "Rata-rata Kalium", short: "K", unit: "mg/kg", tone: "amber" },
  { key: "avg_ph", label: "Rata-rata pH", short: "pH", unit: "skala pH", tone: "violet" }
];
const tones = {
  emerald: "bg-emerald-50 text-emerald-800 border-emerald-100",
  blue: "bg-blue-50 text-blue-800 border-blue-100",
  amber: "bg-amber-50 text-amber-800 border-amber-100",
  violet: "bg-violet-50 text-violet-800 border-violet-100"
};
</script>

<template>
  <section class="rounded-2xl border border-slate-200/80 bg-white p-4 shadow-[0_3px_18px_-12px_rgba(15,23,42,.25)] sm:p-5">
    <div class="grid gap-4 lg:grid-cols-[minmax(190px,.7fr)_minmax(0,2.3fr)] lg:items-center">
      <div class="flex items-center gap-3 lg:border-r lg:border-slate-100 lg:pr-5">
        <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-700"><BarChart3 class="h-5 w-5" /></div>
        <div><h2 class="text-base font-bold tracking-tight text-slate-900">Insight Monitoring</h2><p class="mt-1 text-xs leading-5 text-slate-500">Rata-rata dari seluruh data tersimpan</p></div>
      </div>
      <div class="grid grid-cols-2 gap-2.5 sm:grid-cols-4">
        <div v-for="item in metrics" :key="item.key" class="min-w-0 rounded-xl border p-3" :class="tones[item.tone]">
          <p class="text-[11px] font-semibold opacity-75">{{ item.label }}</p>
          <p class="mt-2 truncate text-xl font-bold tracking-tight tabular-nums">{{ summary[item.key] ?? "-" }}</p>
          <p class="mt-0.5 text-[10px] opacity-65">{{ item.unit }}</p>
        </div>
      </div>
    </div>
  </section>
</template>