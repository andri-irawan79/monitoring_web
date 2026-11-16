<script setup>
import { computed } from "vue";
import { Activity, CheckCircle2 } from "lucide-vue-next";
import BaseCard from "../ui/BaseCard.vue";

const props = defineProps({ monitoring: { type: Object, default: null } });

const nutrients = computed(() => {
  if (!props.monitoring) return [];
  return [
    { key: "nitrogen", label: "Nitrogen", short: "N", value: Number(props.monitoring.nitrogen), unit: "mg/kg" },
    { key: "phosphorus", label: "Fosfor", short: "P", value: Number(props.monitoring.phosphorus), unit: "mg/kg" },
    { key: "potassium", label: "Kalium", short: "K", value: Number(props.monitoring.potassium), unit: "mg/kg" },
    { key: "ph", label: "pH Tanah", short: "pH", value: Number(props.monitoring.ph), unit: "skala pH" }
  ];
});

function getStatus(type, value) {
  switch (type) {
    case "nitrogen":
      if (value < 40) return { text: "Rendah", tone: "rose" };
      if (value <= 70) return { text: "Normal", tone: "emerald" };
      return { text: "Tinggi", tone: "amber" };
    case "phosphorus":
      if (value < 30) return { text: "Rendah", tone: "rose" };
      if (value <= 60) return { text: "Normal", tone: "emerald" };
      return { text: "Tinggi", tone: "amber" };
    case "potassium":
      if (value < 30) return { text: "Rendah", tone: "rose" };
      if (value <= 50) return { text: "Normal", tone: "emerald" };
      return { text: "Tinggi", tone: "amber" };
    case "ph":
      if (value < 5.5) return { text: "Asam", tone: "rose" };
      if (value <= 7) return { text: "Optimal", tone: "emerald" };
      return { text: "Basa", tone: "amber" };
    default:
      return { text: "-", tone: "slate" };
  }
}
const toneClass = {
  rose: "bg-rose-50 text-rose-700 ring-rose-100",
  emerald: "bg-emerald-50 text-emerald-700 ring-emerald-100",
  amber: "bg-amber-50 text-amber-700 ring-amber-100",
  slate: "bg-slate-100 text-slate-600 ring-slate-200"
};
const iconTone = {
  nitrogen: "bg-emerald-50 text-emerald-700",
  phosphorus: "bg-blue-50 text-blue-700",
  potassium: "bg-amber-50 text-amber-700",
  ph: "bg-violet-50 text-violet-700"
};
</script>

<template>
  <BaseCard>
    <div class="mb-5 flex items-start justify-between gap-3">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.16em] text-emerald-700">Kondisi terkini</p>
        <h2 class="mt-1 text-lg font-bold tracking-tight text-slate-900">Status Nutrisi</h2>
        <p class="mt-1 text-xs text-slate-500">Interpretasi nilai parameter terakhir</p>
      </div>
      <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700"><Activity class="h-5 w-5" /></div>
    </div>
    <div v-if="monitoring" class="space-y-3">
      <div v-for="item in nutrients" :key="item.key" class="flex items-center gap-3 rounded-xl border border-slate-100 bg-slate-50/70 p-3">
        <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-xs font-bold" :class="iconTone[item.key]">{{ item.short }}</div>
        <div class="min-w-0 flex-1">
          <p class="text-xs font-medium text-slate-500">{{ item.label }}</p>
          <p class="mt-0.5 text-base font-bold text-slate-800 tabular-nums">{{ Number.isFinite(item.value) ? item.value.toFixed(2) : "-" }} <span class="text-[10px] font-medium text-slate-400">{{ item.unit }}</span></p>
        </div>
        <span class="shrink-0 rounded-full px-2.5 py-1 text-[11px] font-semibold ring-1 ring-inset" :class="toneClass[getStatus(item.key, item.value).tone]">{{ getStatus(item.key, item.value).text }}</span>
      </div>
    </div>
    <div v-else class="py-8 text-center text-sm text-slate-400">Data monitoring belum tersedia.</div>
    <div class="mt-4 flex items-start gap-2 rounded-xl border border-emerald-100 bg-emerald-50/70 p-3 text-xs leading-5 text-emerald-800">
      <CheckCircle2 class="mt-0.5 h-4 w-4 shrink-0" />
      Status ditampilkan berdasarkan batas kategori yang digunakan pada sistem.
    </div>
  </BaseCard>
</template>