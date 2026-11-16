<script setup>
import { Leaf, FlaskConical, Droplets, Waves } from "lucide-vue-next";
defineProps({ monitoring: { type: Object, default: null } });
const fmt = value => { const n = Number(value); return Number.isFinite(n) ? n.toFixed(2) : "-"; };
const items = [
  { key: "nitrogen", label: "Nitrogen", unit: "mg/kg", icon: Leaf, tone: "emerald" },
  { key: "phosphorus", label: "Fosfor", unit: "mg/kg", icon: FlaskConical, tone: "blue" },
  { key: "potassium", label: "Kalium", unit: "mg/kg", icon: Droplets, tone: "amber" },
  { key: "ph", label: "pH Tanah", unit: "skala pH", icon: Waves, tone: "violet" }
];
const tones = { emerald: "bg-emerald-50 text-emerald-700", blue: "bg-blue-50 text-blue-700", amber: "bg-amber-50 text-amber-700", violet: "bg-violet-50 text-violet-700" };
</script>

<template>
  <section v-if="monitoring" class="mb-6 grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4">
    <article v-for="item in items" :key="item.key" class="group relative overflow-hidden rounded-2xl border border-slate-200/80 bg-white p-4 shadow-[0_3px_14px_-10px_rgba(15,23,42,.24)] transition hover:-translate-y-0.5 hover:shadow-md sm:p-5">
      <div class="flex items-center justify-between gap-2"><p class="text-xs font-semibold text-slate-500 sm:text-sm">{{ item.label }}</p><span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl" :class="tones[item.tone]"><component :is="item.icon" class="h-4 w-4" /></span></div>
      <p class="mt-3 text-2xl font-bold tracking-tight text-slate-900 tabular-nums sm:text-3xl">{{ fmt(monitoring[item.key]) }}</p>
      <p class="mt-1 text-xs text-slate-400">{{ item.unit }}</p>
    </article>
  </section>
</template>