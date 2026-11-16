<script setup>
import { BarChart3 } from "lucide-vue-next";
import BaseCard from "../ui/BaseCard.vue";

defineProps({
  monitoring: { type: Object, default: () => ({}) },
  summary: { type: Object, default: () => ({}) }
});
</script>

<template>
  <BaseCard>
    <div class="mb-5 flex items-start gap-3">
      <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-700"><BarChart3 class="h-5 w-5" /></div>
      <div>
        <h2 class="text-lg font-bold tracking-tight text-slate-900">Insight Monitoring</h2>
        <p class="mt-1 text-xs text-slate-500">Rata-rata parameter dari seluruh data</p>
      </div>
    </div>
    <div class="grid grid-cols-2 gap-3">
      <div class="rounded-xl bg-emerald-50/80 p-3">
        <p class="text-xs font-medium text-emerald-800/70">Rata-rata N</p>
        <p class="mt-2 text-xl font-bold text-emerald-900 tabular-nums">{{ summary.avg_nitrogen ?? "-" }}</p>
        <p class="mt-0.5 text-[10px] text-emerald-800/60">mg/kg</p>
      </div>
      <div class="rounded-xl bg-blue-50/80 p-3">
        <p class="text-xs font-medium text-blue-800/70">Rata-rata P</p>
        <p class="mt-2 text-xl font-bold text-blue-900 tabular-nums">{{ summary.avg_phosphorus ?? "-" }}</p>
        <p class="mt-0.5 text-[10px] text-blue-800/60">mg/kg</p>
      </div>
      <div class="rounded-xl bg-amber-50/80 p-3">
        <p class="text-xs font-medium text-amber-800/70">Rata-rata K</p>
        <p class="mt-2 text-xl font-bold text-amber-900 tabular-nums">{{ summary.avg_potassium ?? "-" }}</p>
        <p class="mt-0.5 text-[10px] text-amber-800/60">mg/kg</p>
      </div>
      <div class="rounded-xl bg-violet-50/80 p-3">
        <p class="text-xs font-medium text-violet-800/70">Rata-rata pH</p>
        <p class="mt-2 text-xl font-bold text-violet-900 tabular-nums">{{ summary.avg_ph ?? "-" }}</p>
        <p class="mt-0.5 text-[10px] text-violet-800/60">skala pH</p>
      </div>
    </div>
  </BaseCard>
</template>