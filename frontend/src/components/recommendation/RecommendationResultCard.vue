<script setup>
import { computed } from "vue";
import BaseCard from "../ui/BaseCard.vue";
import { Sprout, ClipboardList, CheckCircle2, Info, Leaf } from "lucide-vue-next";

const props = defineProps({
  recommendation: { type: Object, default: null },
  initialLoading: { type: Boolean, default: false }
});

const activeItems = computed(() =>
  (props.recommendation?.items || []).filter((item) => item.direkomendasikan)
);

function doseText(item) {
  if (item.dosis_g !== null && item.dosis_g !== undefined) {
    return Number(item.dosis_g).toLocaleString("id-ID") + " g/pohon";
  }
  if (item.dosis_min_g !== null && item.dosis_min_g !== undefined) {
    return Number(item.dosis_min_g).toLocaleString("id-ID") + "–" +
      Number(item.dosis_maks_g).toLocaleString("id-ID") + " g/pohon";
  }
  if (item.dosis_kg !== null && item.dosis_kg !== undefined) {
    return Number(item.dosis_kg).toFixed(2) + " kg/pohon";
  }
  return "-";
}
</script>

<template>
  <BaseCard class="h-full overflow-hidden !p-0 shadow-[0_8px_28px_-20px_rgba(15,23,42,.28)]">
    <div class="flex items-center gap-3 border-b border-slate-100 bg-gradient-to-br from-emerald-50 via-white to-lime-50/70 px-5 py-5 sm:px-6">
      <span class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700 shadow-sm">
        <ClipboardList class="h-5 w-5" />
      </span>
      <div class="min-w-0">
        <div class="flex flex-wrap items-center gap-2">
          <h2 class="text-lg font-bold tracking-tight text-slate-900">Paket Rekomendasi Pemupukan</h2>
          <span class="rounded-full bg-emerald-100 px-2 py-0.5 text-[9px] font-extrabold uppercase tracking-wider text-emerald-800">FIS-1 + FIS-2</span>
        </div>
        <p class="mt-0.5 text-xs text-slate-500">Dosis pupuk hara dan bahan koreksi pH hasil perhitungan</p>
      </div>
      <span v-if="recommendation" class="ml-auto inline-flex shrink-0 items-center gap-1 rounded-full bg-emerald-50 px-2.5 py-1 text-[10px] font-bold text-emerald-700 ring-1 ring-inset ring-emerald-100">
        <CheckCircle2 class="h-3.5 w-3.5" /> Selesai
      </span>
    </div>

    <div class="flex min-h-[330px] flex-col justify-center p-5 sm:p-6">
      <div v-if="initialLoading" class="flex min-h-64 flex-col items-center justify-center py-10 text-center">
        <p class="text-sm font-medium text-slate-600">Memuat hasil rekomendasi...</p>
      </div>

      <div v-else-if="recommendation" class="space-y-4">
        <div class="flex items-start justify-between gap-3 rounded-2xl border border-emerald-100 bg-emerald-50/70 p-4">
          <div>
            <p class="text-[10px] font-extrabold uppercase tracking-[0.15em] text-emerald-800/70">Objek tanaman</p>
            <p class="mt-1 text-lg font-extrabold text-emerald-950">{{ recommendation.objek_tanaman || "Durian Montong" }}</p>
            <p class="mt-1 text-sm text-slate-600">Fase {{ recommendation.fase || "-" }}</p>
            <p v-if="recommendation.profile" class="mt-1 text-[11px] font-medium text-emerald-800">
              Profil parameter Fuzzy: {{ recommendation.profile }}
            </p>
          </div>
          <span class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-white text-emerald-700 shadow-sm">
            <Leaf class="h-5 w-5" />
          </span>
        </div>

        <div>
          <div class="mb-3 flex items-center justify-between gap-3">
            <h3 class="text-sm font-bold text-slate-800">Pupuk yang direkomendasikan</h3>
            <span class="text-xs font-medium text-slate-500">{{ activeItems.length }} komponen</span>
          </div>
          <div v-if="activeItems.length" class="space-y-2">
            <div v-for="item in activeItems" :key="item.kode_pupuk"
              class="flex items-center justify-between gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3">
              <div class="min-w-0">
                <p class="font-bold text-slate-800">{{ item.nama_pupuk }}</p>
                <p class="mt-0.5 text-[11px] text-slate-500">{{ item.kategori }}</p>
              </div>
              <p class="shrink-0 text-sm font-extrabold tabular-nums text-emerald-800">{{ doseText(item) }}</p>
            </div>
          </div>
          <div v-else class="rounded-xl border border-dashed border-slate-300 bg-slate-50 px-4 py-5 text-center text-sm text-slate-500">
            Tidak ada dosis pupuk yang disarankan untuk kondisi input dan fase ini.
          </div>
        </div>

        <div v-if="recommendation.notes?.length" class="rounded-xl border border-amber-200 bg-amber-50/80 p-4">
          <p class="text-xs font-bold text-amber-900">Catatan kondisi</p>
          <ul class="mt-2 space-y-1 text-xs leading-5 text-amber-900">
            <li v-for="note in recommendation.notes" :key="note">• {{ note }}</li>
          </ul>
        </div>

        <div v-if="recommendation.parameter_warnings?.length" class="flex items-start gap-2 rounded-xl border border-slate-200 bg-slate-50 p-3 text-[11px] leading-5 text-slate-600">
          <Info class="mt-0.5 h-4 w-4 shrink-0" />
          <ul class="space-y-1">
            <li v-for="warning in recommendation.parameter_warnings" :key="warning">{{ warning }}</li>
          </ul>
        </div>

        <div class="border-t border-slate-100 pt-3 text-xs text-slate-500">
          Waktu perhitungan: {{ recommendation.created_at }}
        </div>
      </div>

      <div v-else class="flex min-h-64 flex-col items-center justify-center rounded-2xl border border-dashed border-emerald-200 bg-gradient-to-br from-emerald-50/70 to-slate-50 px-5 py-9 text-center">
        <div class="flex h-14 w-14 items-center justify-center rounded-2xl bg-white text-emerald-700 shadow-sm ring-1 ring-emerald-100">
          <Sprout class="h-7 w-7" />
        </div>
        <h3 class="mt-4 text-base font-bold text-slate-800">Siap menghasilkan rekomendasi</h3>
        <p class="mt-2 max-w-sm text-sm leading-relaxed text-slate-500">
          Pilih fase pertumbuhan lalu tekan Buat Rekomendasi untuk menghitung kebutuhan pupuk hara dan koreksi pH.
        </p>
      </div>
    </div>
  </BaseCard>
</template>
