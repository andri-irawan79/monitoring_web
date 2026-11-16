<script setup>
import BaseCard from "../ui/BaseCard.vue";
import { Sprout } from "lucide-vue-next";

defineProps({
  recommendation: {
    type: Object,
    default: null
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
    <div class="flex items-center gap-3 mb-6">
      <Sprout class="w-7 h-7 text-green-600" />
      <h2 class="text-2xl font-bold">Hasil Rekomendasi</h2>
    </div>

    <div v-if="recommendation" class="grid md:grid-cols-2 gap-6">
      <div>
        <p class="text-slate-500">Objek Tanaman</p>
        <h3 class="text-xl font-semibold mt-2">
          {{ recommendation.objek_tanaman || "Durian Montong" }}
        </h3>
      </div>
      <div>
        <p class="text-slate-500">Jenis Pupuk</p>
        <h3 class="text-2xl font-bold mt-2">{{ recommendation.jenis_pupuk }}</h3>
      </div>
      <div>
        <p class="text-slate-500">Dosis</p>
        <h3 class="text-2xl font-bold mt-2">{{ recommendation.dosis }} kg/pohon</h3>
      </div>
      <div>
        <p class="text-slate-500">Kategori</p>
        <span
          class="inline-block mt-2 px-4 py-2 rounded-full font-semibold"
          :class="badgeClass(recommendation.kategori)"
        >
          {{ recommendation.kategori }}
        </span>
      </div>
      <div>
        <p class="text-slate-500">Fase Pertumbuhan</p>
        <h3 class="text-xl font-semibold mt-2">{{ recommendation.fase }}</h3>
      </div>
      <div>
        <p class="text-slate-500">Tanggal</p>
        <h3 class="text-xl font-semibold mt-2">{{ recommendation.created_at }}</h3>
      </div>
    </div>

    <div v-else class="text-center text-slate-400 py-10">
      Belum ada rekomendasi.
    </div>
  </BaseCard>
</template>
