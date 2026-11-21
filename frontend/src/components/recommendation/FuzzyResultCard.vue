<script setup>
import { computed } from "vue";
import { ChevronDown, SlidersHorizontal } from "lucide-vue-next";
import BaseCard from "../ui/BaseCard.vue";

const props = defineProps({
  fuzzy: {
    type: Object,
    default: null
  }
});

const variableOrder = [
  { key: "N", label: "Nitrogen (N)" },
  { key: "P", label: "Fosfor (P)" },
  { key: "K", label: "Kalium (K)" },
  { key: "PH", label: "pH Tanah" }
];

// Kelembapan tanah sengaja tidak dimasukkan ke panel fuzzifikasi FIS-1/FIS-2.
// Parameter tersebut ditampilkan terpisah sebagai informasi kondisi tanah.
const fuzzySections = computed(() => {
  if (!props.fuzzy || typeof props.fuzzy !== "object") return [];

  return variableOrder.flatMap((variable) => {
    const memberships = props.fuzzy[variable.key];
    if (!memberships || typeof memberships !== "object") return [];

    return [{
      key: variable.key,
      label: variable.label,
      memberships: Object.entries(memberships)
    }];
  });
});

const formatDegree = (value) => {
  const number = Number(value);
  return Number.isFinite(number) ? number.toFixed(3) : "0.000";
};

const width = (value) => {
  const number = Number(value);
  if (!Number.isFinite(number)) return "0%";
  return `${Math.min(100, Math.max(0, number * 100))}%`;
};
</script>

<template>
  <BaseCard>
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2">
        <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700">
          <SlidersHorizontal class="h-4 w-4" />
        </span>
        <div>
          <h2 class="text-lg font-bold tracking-tight text-slate-900">Hasil Fuzzifikasi</h2>
          <p class="text-xs text-slate-500">Derajat keanggotaan variabel yang digunakan dalam proses fuzzy.</p>
        </div>
      </div>
    </div>

    <div v-if="fuzzySections.length" class="mt-5">
      <details class="group overflow-hidden rounded-xl border border-slate-200 bg-white">
        <summary class="flex cursor-pointer list-none items-center justify-between gap-3 px-4 py-3.5 transition hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-emerald-500">
          <span>
            <span class="block text-sm font-semibold text-slate-800">Lihat detail proses fuzzifikasi</span>
            <span class="mt-0.5 block text-xs text-slate-500">N, P, K, dan pH tanah · derajat keanggotaan 0–1</span>
          </span>
          <ChevronDown class="h-4 w-4 shrink-0 text-slate-500 transition-transform duration-200 group-open:rotate-180" />
        </summary>

        <div class="space-y-5 border-t border-slate-100 px-4 py-5">
          <section v-for="section in fuzzySections" :key="section.key" class="space-y-3">
            <div class="flex items-center justify-between gap-3">
              <h3 class="text-sm font-bold text-slate-800">{{ section.label }}</h3>
              <span class="text-[11px] font-medium text-slate-400">{{ section.memberships.length }} himpunan</span>
            </div>

            <div v-for="[label, value] in section.memberships" :key="label" class="space-y-1.5">
              <div class="flex items-center justify-between gap-3 text-xs">
                <span class="capitalize text-slate-600">{{ label }}</span>
                <span class="font-semibold tabular-nums text-slate-700">{{ formatDegree(value) }}</span>
              </div>
              <div
                class="h-2.5 w-full overflow-hidden rounded-full bg-slate-100"
                role="img"
                :aria-label="`Derajat keanggotaan ${section.label} ${label}: ${formatDegree(value)}`"
              >
                <div
                  class="h-full rounded-full bg-emerald-600 transition-[width] duration-300"
                  :style="{ width: width(value) }"
                />
              </div>
            </div>
          </section>
        </div>
      </details>
    </div>

    <div v-else class="mt-5 rounded-xl bg-slate-50 px-4 py-7 text-center">
      <p class="text-sm font-medium text-slate-600">Belum ada proses fuzzifikasi</p>
      <p class="mt-1 text-xs text-slate-400">Detail akan tersedia setelah rekomendasi berhasil dihitung.</p>
    </div>
  </BaseCard>
</template>
