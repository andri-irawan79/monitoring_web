<script setup>
import { computed } from "vue";
import { Activity, CheckCircle2 } from "lucide-vue-next";
import BaseCard from "../ui/BaseCard.vue";

const props = defineProps({ monitoring: { type: Object, default: null } });

const nutrients = computed(() => {
  if (!props.monitoring) return [];
  const items = [
    { key: "nitrogen", label: "Nitrogen", short: "N", value: Number(props.monitoring.nitrogen), unit: "mg/kg" },
    { key: "phosphorus", label: "Fosfor", short: "P", value: Number(props.monitoring.phosphorus), unit: "mg/kg" },
    { key: "potassium", label: "Kalium", short: "K", value: Number(props.monitoring.potassium), unit: "mg/kg" },
    { key: "ph", label: "pH Tanah", short: "pH", value: Number(props.monitoring.ph), unit: "skala pH" }
  ];
  if (props.monitoring.soil_moisture !== null && props.monitoring.soil_moisture !== undefined) {
    items.push({
      key: "soil_moisture",
      label: "Kelembapan Tanah",
      short: "SM",
      value: Number(props.monitoring.soil_moisture),
      unit: "%"
    });
  }
  return items;
});

function getStatus(type, value) {
  const statusKeys = {
    nitrogen: "status_n",
    phosphorus: "status_p",
    potassium: "status_k",
    ph: "status_ph",
    soil_moisture: "status_kelembapan_tanah"
  };
  const fuzzyLabel = props.monitoring?.fuzzy_status?.[statusKeys[type]];
  if (fuzzyLabel) {
    const label = String(fuzzyLabel).toLowerCase();
    if (type === "ph") {
      if (label === "masam") return { text: "Masam", tone: "rose" };
      if (label === "basa") return { text: "Basa", tone: "amber" };
      return { text: "Normal", tone: "emerald" };
    }
    if (type === "soil_moisture") {
      if (label === "kering") return { text: "Kering", tone: "rose" };
      if (label === "basah") return { text: "Basah", tone: "amber" };
      if (label === "optimal") return { text: "Optimal", tone: "emerald" };
    }
    if (label === "rendah") return { text: "Rendah", tone: "rose" };
    if (label === "sedang") return { text: "Sedang", tone: "amber" };
    if (label === "tinggi") return { text: "Tinggi", tone: "emerald" };
  }

  // Fallback saat membaca data lama dari API yang belum mengirim fuzzy_status.
  if (type === "nitrogen") return value < 40 ? { text: "Rendah", tone: "rose" } : value <= 70 ? { text: "Sedang", tone: "amber" } : { text: "Tinggi", tone: "emerald" };
  if (type === "phosphorus") return value < 30 ? { text: "Rendah", tone: "rose" } : value <= 60 ? { text: "Sedang", tone: "amber" } : { text: "Tinggi", tone: "emerald" };
  if (type === "potassium") return value < 30 ? { text: "Rendah", tone: "rose" } : value <= 50 ? { text: "Sedang", tone: "amber" } : { text: "Tinggi", tone: "emerald" };
  if (type === "ph") return value < 5.5 ? { text: "Masam", tone: "rose" } : value <= 6.5 ? { text: "Normal", tone: "emerald" } : { text: "Basa", tone: "amber" };
  if (type === "soil_moisture") return value <= 15 ? { text: "Kering", tone: "rose" } : value >= 25 ? { text: "Basah", tone: "amber" } : { text: "Optimal", tone: "emerald" };
  return { text: "-", tone: "slate" };
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
  ph: "bg-violet-50 text-violet-700",
  soil_moisture: "bg-teal-50 text-teal-700"
};
</script>

<template>
  <BaseCard class="h-full !p-0">
    <section class="flex h-full min-h-[470px] flex-col p-4 sm:p-6">
      <div class="mb-5 flex items-start justify-between gap-3">
        <div class="min-w-0">
          <p class="text-xs font-bold uppercase tracking-[0.16em] text-emerald-700">Kondisi terkini</p>
          <h2 class="mt-1 text-lg font-bold tracking-tight text-slate-900">Status Parameter Tanah</h2>
          <p class="mt-1 text-xs text-slate-500">Interpretasi nilai parameter terakhir</p>
        </div>
        <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700">
          <Activity class="h-5 w-5" />
        </div>
      </div>

      <div v-if="monitoring" class="flex flex-1 flex-col justify-between gap-2.5">
        <div
          v-for="item in nutrients"
          :key="item.key"
          class="flex flex-1 items-center gap-3 rounded-xl border border-slate-100 bg-slate-50/70 p-3"
        >
          <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-xs font-bold" :class="iconTone[item.key]">
            {{ item.short }}
          </div>
          <div class="min-w-0 flex-1">
            <p class="text-xs font-medium text-slate-500">{{ item.label }}</p>
            <p class="mt-0.5 text-base font-bold text-slate-800 tabular-nums">
              {{ Number.isFinite(item.value) ? item.value.toFixed(2) : "-" }}
              <span class="text-[10px] font-medium text-slate-400">{{ item.unit }}</span>
            </p>
          </div>
          <span class="shrink-0 rounded-full px-2.5 py-1 text-[11px] font-semibold ring-1 ring-inset" :class="toneClass[getStatus(item.key, item.value).tone]">
            {{ getStatus(item.key, item.value).text }}
          </span>
        </div>
      </div>

      <div v-else class="flex flex-1 items-center justify-center py-8 text-center text-sm text-slate-400">
        Data monitoring belum tersedia.
      </div>

      <div class="mt-4 flex items-start gap-2 rounded-xl border border-emerald-100 bg-emerald-50/70 p-3 text-xs leading-5 text-emerald-800">
        <CheckCircle2 class="mt-0.5 h-4 w-4 shrink-0" />
        <span>Kategori mengikuti fungsi keanggotaan Fuzzy yang dikonfigurasi dalam sistem dan bukan diagnosis agronomis kondisi tanah.</span>
      </div>
    </section>
  </BaseCard>
</template>
