<script setup>
import { computed } from "vue";
import { ChartNoAxesCombined, CalendarDays } from "lucide-vue-next";
import MonitoringChart from "../MonitoringChart.vue";

const props = defineProps({ data: { type: Array, default: () => [] } });
const recordCount = computed(() => Math.min(props.data.length, 30));
</script>

<template>
  <section class="flex h-full min-h-[470px] flex-col overflow-hidden rounded-2xl border border-slate-200/80 bg-white p-4 shadow-[0_3px_18px_-12px_rgba(15,23,42,.25)] sm:p-6">
    <div class="mb-5 flex flex-wrap items-start justify-between gap-3">
      <div class="flex min-w-0 items-start gap-3">
        <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700">
          <ChartNoAxesCombined class="h-5 w-5" />
        </div>
        <div class="min-w-0">
          <h2 class="text-lg font-bold tracking-tight text-slate-900 sm:text-xl">Tren Nutrisi Tanah</h2>
          <p class="mt-1 text-xs leading-5 text-slate-500 sm:text-sm">Perubahan Nitrogen, Fosfor, dan Kalium berdasarkan data simulasi</p>
        </div>
      </div>
      <span class="inline-flex shrink-0 items-center gap-1.5 rounded-full bg-slate-50 px-3 py-1.5 text-xs font-semibold text-slate-500">
        <CalendarDays class="h-3.5 w-3.5" />
        {{ recordCount }} data terakhir
      </span>
    </div>

    <div class="min-w-0 flex-1">
      <MonitoringChart :data="data" />
    </div>

    <p class="mt-auto pt-3 text-[11px] leading-5 text-slate-400">
      Sumbu vertikal menunjukkan konsentrasi unsur hara (ppm). Arah garis membantu melihat perubahan antar data simulasi.
    </p>
  </section>
</template>
