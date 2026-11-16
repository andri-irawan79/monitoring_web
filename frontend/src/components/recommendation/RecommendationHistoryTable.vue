<script setup>
import BaseCard from "../ui/BaseCard.vue";
import { exportRecommendationCSV } from "../../services/recommendationService";

defineProps({
  recommendations: {
    type: Array,
    default: () => []
  }
});

function badge(kategori) {
  if (!kategori) return "bg-slate-100 text-slate-700";
  const value = kategori.toLowerCase();
  if (value === "tinggi") return "bg-red-100 text-red-700";
  if (value === "sedang") return "bg-yellow-100 text-yellow-700";
  return "bg-green-100 text-green-700";
}
</script>

<template>
  <BaseCard>
    <div class="mb-5 flex flex-col gap-4 sm:mb-6 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h2 class="text-xl font-bold">Riwayat Rekomendasi</h2>
        <p class="text-sm text-slate-500">10 rekomendasi terakhir untuk Durian Montong</p>
      </div>
      <button
        type="button"
        @click="exportRecommendationCSV"
        class="inline-flex min-h-10 w-full items-center justify-center rounded-xl bg-green-700 px-4 py-2 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-green-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-green-500 focus-visible:ring-offset-2 sm:w-auto"
      >
        Export CSV
      </button>
    </div>

    <div class="overflow-x-auto">
      <table class="min-w-full whitespace-nowrap text-sm">
        <thead>
          <tr class="border-b text-left text-slate-500">
            <th class="px-4 py-3">Tanggal</th>
            <th class="px-4 py-3">N</th>
            <th class="px-4 py-3">P</th>
            <th class="px-4 py-3">K</th>
            <th class="px-4 py-3">pH</th>
            <th class="px-4 py-3">Objek Tanaman</th>
            <th class="px-4 py-3">Fase</th>
            <th class="px-4 py-3">Pupuk</th>
            <th class="px-4 py-3">Dosis</th>
            <th class="px-4 py-3">Kategori</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in recommendations"
            :key="item.id"
            class="border-b transition hover:bg-slate-50"
          >
            <td class="px-4 py-3">{{ item.created_at }}</td>
            <td class="px-4 py-3">{{ item.nitrogen }}</td>
            <td class="px-4 py-3">{{ item.phosphorus }}</td>
            <td class="px-4 py-3">{{ item.potassium }}</td>
            <td class="px-4 py-3">{{ Number(item.ph).toFixed(1) }}</td>
            <td class="px-4 py-3">{{ item.objek_tanaman || "Durian Montong" }}</td>
            <td class="px-4 py-3">{{ item.fase }}</td>
            <td class="px-4 py-3">{{ item.jenis_pupuk }}</td>
            <td class="px-4 py-3">{{ item.dosis }} kg</td>
            <td class="px-4 py-3">
              <span
                class="rounded-full px-3 py-1 text-xs font-medium"
                :class="badge(item.kategori)"
              >
                {{ item.kategori }}
              </span>
            </td>
          </tr>
          <tr v-if="!recommendations.length">
            <td colspan="10" class="px-4 py-10 text-center">
              <p class="font-medium text-slate-700">Belum ada riwayat rekomendasi</p>
              <p class="mt-1 whitespace-normal text-sm text-slate-500">
                Rekomendasi yang berhasil dibuat akan tersimpan dan ditampilkan pada tabel ini.
              </p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </BaseCard>
</template>
