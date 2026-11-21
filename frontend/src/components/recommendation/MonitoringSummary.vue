<script setup>
import { computed } from "vue";
import { Leaf, FlaskConical, Droplets, Waves } from "lucide-vue-next";

const props = defineProps({ monitoring: { type: Object, default: null } });

const fmt = value => {
  const n = Number(value);
  return Number.isFinite(n) ? n.toFixed(2) : "-";
};

const items = [
  { key: "nitrogen", label: "Nitrogen", unit: "mg/kg", icon: Leaf, tone: "emerald" },
  { key: "phosphorus", label: "Fosfor", unit: "mg/kg", icon: FlaskConical, tone: "blue" },
  { key: "potassium", label: "Kalium", unit: "mg/kg", icon: Droplets, tone: "amber" },
  { key: "ph", label: "pH Tanah", unit: "skala pH", icon: Waves, tone: "violet" }
];

const tones = {
  emerald: "bg-emerald-50 text-emerald-700",
  blue: "bg-blue-50 text-blue-700",
  amber: "bg-amber-50 text-amber-700",
  violet: "bg-violet-50 text-violet-700"
};

const moistureStatus = computed(() =>
  props.monitoring?.fuzzy_status?.status_kelembapan_tanah || null
);

const moistureStatusTone = computed(() => {
  const status = String(moistureStatus.value || "").toLocaleLowerCase("id-ID");
  if (status === "kering") return "bg-amber-50 text-amber-800 ring-amber-200";
  if (status === "optimal") return "bg-emerald-50 text-emerald-800 ring-emerald-200";
  if (status === "basah") return "bg-sky-50 text-sky-800 ring-sky-200";
  return "bg-slate-50 text-slate-600 ring-slate-200";
});
</script>

<template>
  <div v-if="monitoring" class="mb-6 space-y-3">
    <section class="grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4" aria-label="Parameter monitoring untuk rekomendasi">
      <article
        v-for="item in items"
        :key="item.key"
        class="group relative overflow-hidden rounded-2xl border border-slate-200/80 bg-white p-4 shadow-[0_3px_14px_-10px_rgba(15,23,42,.24)] transition hover:-translate-y-0.5 hover:shadow-md sm:p-5"
      >
        <div class="flex items-center justify-between gap-2">
          <p class="text-xs font-semibold text-slate-500 sm:text-sm">{{ item.label }}</p>
          <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl" :class="tones[item.tone]">
            <component :is="item.icon" class="h-4 w-4" />
          </span>
        </div>
        <p class="mt-3 text-2xl font-bold tracking-tight text-slate-900 tabular-nums sm:text-3xl">
          {{ fmt(monitoring[item.key]) }}
        </p>
        <p class="mt-1 text-xs text-slate-400">{{ item.unit }}</p>
      </article>
    </section>

    <section
      v-if="monitoring.soil_moisture !== null && monitoring.soil_moisture !== undefined"
      class="flex flex-col gap-3 rounded-2xl border border-teal-100 bg-gradient-to-r from-teal-50/80 to-white p-4 shadow-[0_3px_14px_-10px_rgba(15,23,42,.18)] sm:flex-row sm:items-center sm:justify-between sm:px-5"
      aria-label="Informasi status kelembapan tanah"
    >
      <div class="flex min-w-0 items-start gap-3">
        <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-teal-100 text-teal-700">
          <Droplets class="h-5 w-5" />
        </span>
        <div class="min-w-0">
          <p class="text-[11px] font-bold uppercase tracking-[0.14em] text-teal-700">Informasi kondisi tanah</p>
          <h3 class="mt-0.5 text-sm font-bold text-slate-900">Status Kelembapan Tanah</h3>
          <p class="mt-1 max-w-2xl text-xs leading-5 text-slate-500">
            Informasi pendukung untuk catatan kondisi tanah; tidak mengubah nilai Z maupun dosis pupuk.
          </p>
        </div>
      </div>

      <div class="flex shrink-0 items-center justify-between gap-4 rounded-xl border border-white/80 bg-white/80 px-3.5 py-2.5 sm:min-w-[190px]">
        <div>
          <p class="text-[11px] font-medium text-slate-500">Nilai kelembapan</p>
          <p class="mt-0.5 text-lg font-extrabold tabular-nums text-slate-900">
            {{ fmt(monitoring.soil_moisture) }}<span class="ml-1 text-xs font-semibold text-slate-500">%</span>
          </p>
        </div>
        <span class="rounded-full px-3 py-1.5 text-xs font-bold ring-1 ring-inset" :class="moistureStatusTone">
          {{ moistureStatus || "Status belum tersedia" }}
        </span>
      </div>
    </section>
  </div>
</template>
