<script setup>
import BaseCard from "../ui/BaseCard.vue";
import { Sprout, LoaderCircle, ClipboardList } from "lucide-vue-next";

defineProps({
  recommendation: {
    type: Object,
    default: null
  },
  initialLoading: {
    type: Boolean,
    default: false
  }
});

function badgeClass(kategori) {
  if (!kategori) return "bg-slate-100 text-slate-700";
  const value = kategori.toLowerCase();
  if (value === "tinggi") return "bg-red-100 text-red-700";
  if (value === "sedang") return "bg-yellow-100 text-yellow-700";
  return "bg-green-100 text-green-700";
}
</script>

<template>
  <BaseCard>
    <div class="mb-6 flex items-center gap-3">
      <Sprout class="h-7 w-7 text-green-600" />
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Hasil Rekomendasi</h2>
        <p class="mt-1 text-sm text-slate-500">Hasil perhitungan pemupukan Durian Montong</p>
      </div>
    </div>

    <div v-if="initialLoading" class="flex min-h-64 flex-col items-center justify-center py-10 text-center">
      <LoaderCircle class="h-8 w-8 animate-spin text-green-600" />
      <p class="mt-3 text-sm font-medium text-slate-600">Memuat hasil rekomendasi...</p>
    </div>

    <div v-else-if="recommendation" class="grid gap-6 md:grid-cols-2">
      <div>
        <p class="text-slate-500">Objek Tanaman</p>
        <h3 class="mt-2 text-xl font-semibold">
          {{ recommendation.objek_tanaman || "Durian Montong" }}
        </h3>
      </div>
      <div>
        <p class="text-slate-500">Jenis Pupuk</p>
        <h3 class="mt-2 text-2xl font-bold">{{ recommendation.jenis_pupuk }}</h3>
      </div>
      <div>
        <p class="text-slate-500">Dosis</p>
        <h3 class="mt-2 text-2xl font-bold">{{ recommendation.dosis }} kg/pohon</h3>
      </div>
      <div>
        <p class="text-slate-500">Kategori</p>
        <span
          class="mt-2 inline-block rounded-full px-4 py-2 font-semibold"
          :class="badgeClass(recommendation.kategori)"
        >
          {{ recommendation.kategori }}
        </span>
      </div>
      <div>
        <p class="text-slate-500">Fase Pertumbuhan</p>
        <h3 class="mt-2 text-xl font-semibold">{{ recommendation.fase }}</h3>
      </div>
      <div>
        <p class="text-slate-500">Tanggal</p>
        <h3 class="mt-2 text-base font-semibold">{{ recommendation.created_at }}</h3>
      </div>
    </div>

    <div
      v-else
      class="flex min-h-64 flex-col items-center justify-center rounded-xl border border-dashed border-slate-300 bg-slate-50 px-5 py-9 text-center"
    >
      <div class="flex h-14 w-14 items-center justify-center rounded-full bg-green-100 text-green-700">
        <ClipboardList class="h-7 w-7" />
      </div>
      <h3 class="mt-4 text-base font-semibold text-slate-800">Belum ada hasil rekomendasi</h3>
      <p class="mt-2 max-w-sm text-sm leading-relaxed text-slate-500">
        Hasil rekomendasi akan ditampilkan di sini setelah Anda memilih fase pertumbuhan dan menekan tombol
        <span class="font-semibold text-slate-700">Buat Rekomendasi</span>.
      </p>
    </div>
  </BaseCard>
</template>
