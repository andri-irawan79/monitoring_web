<script setup>
import { computed, ref, watch } from "vue";
import { Search, ChevronLeft, ChevronRight, Database } from "lucide-vue-next";
import BaseCard from "../ui/BaseCard.vue";
const props = defineProps({ data: { type: Array, default: () => [] } });
const search = ref("");
const currentPage = ref(1);
const perPage = 10;
const filteredData = computed(() => {
  const term = search.value.trim().toLowerCase();
  return term ? props.data.filter(item => String(item.simulation_date || item.created_at || "").toLowerCase().includes(term)) : props.data;
});
const totalItems = computed(() => filteredData.value.length);
const totalPages = computed(() => Math.max(1, Math.ceil(totalItems.value / perPage)));
const paginatedData = computed(() => filteredData.value.slice((currentPage.value - 1) * perPage, currentPage.value * perPage));
const startItem = computed(() => totalItems.value ? (currentPage.value - 1) * perPage + 1 : 0);
const endItem = computed(() => Math.min(currentPage.value * perPage, totalItems.value));
watch(search, () => { currentPage.value = 1; });
watch(totalPages, pages => { if (currentPage.value > pages) currentPage.value = pages; });
function status(item) {
  if (item.nitrogen < 40 || item.phosphorus < 30 || item.potassium < 30) return { text: "Rendah", class: "bg-rose-50 text-rose-700 ring-1 ring-inset ring-rose-200" };
  if (item.nitrogen > 90 || item.phosphorus > 80 || item.potassium > 70) return { text: "Tinggi", class: "bg-amber-50 text-amber-700 ring-1 ring-inset ring-amber-200" };
  return { text: "Normal", class: "bg-emerald-50 text-emerald-700 ring-1 ring-inset ring-emerald-200" };
}
function fmt(value) { const n = Number(value); return Number.isFinite(n) ? n.toFixed(2) : "-"; }
</script>
<template>
<BaseCard class="w-full min-w-0">
  <div class="mb-5 flex flex-col gap-4 border-b border-slate-100 pb-5 sm:flex-row sm:items-center sm:justify-between">
    <div class="flex items-start gap-3"><div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700"><Database class="h-5 w-5" /></div><div><h2 class="text-lg font-bold tracking-tight text-slate-800">Riwayat Monitoring</h2><p class="mt-1 text-sm text-slate-500">Data kondisi tanah dari simulasi</p></div></div>
    <div class="relative w-full sm:max-w-xs"><Search class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" /><input v-model="search" type="search" placeholder="Cari tanggal..." class="min-h-10 w-full rounded-xl border border-slate-200 bg-white py-2 pl-9 pr-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-50"></div>
  </div>
  <div class="mb-3 flex flex-wrap items-center justify-between gap-2"><p class="text-sm text-slate-500">Menampilkan <span class="font-semibold text-slate-700">{{ startItem }}–{{ endItem }}</span> dari <span class="font-semibold text-slate-700">{{ totalItems }}</span> data</p><span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">10 data per halaman</span></div>
  <div class="overflow-hidden rounded-xl border border-slate-200"><div class="overflow-x-auto"><table class="min-w-[950px] w-full whitespace-nowrap text-sm">
    <thead class="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-slate-500"><tr><th class="px-4 py-3.5">Tanggal</th><th class="px-4 py-3.5">Nitrogen</th><th class="px-4 py-3.5">Fosfor</th><th class="px-4 py-3.5">Kalium</th><th class="px-4 py-3.5">pH</th><th class="px-4 py-3.5">Suhu</th><th class="px-4 py-3.5">Kelembapan</th><th class="px-4 py-3.5">Curah Hujan</th><th class="px-4 py-3.5">Status</th></tr></thead>
    <tbody class="divide-y divide-slate-100 bg-white"><tr v-for="item in paginatedData" :key="item.id" class="transition-colors hover:bg-emerald-50/40">
      <td class="px-4 py-3.5 font-medium text-slate-700">{{ item.simulation_date || item.created_at }}</td><td class="px-4 py-3.5 tabular-nums text-slate-600">{{ fmt(item.nitrogen) }}</td><td class="px-4 py-3.5 tabular-nums text-slate-600">{{ fmt(item.phosphorus) }}</td><td class="px-4 py-3.5 tabular-nums text-slate-600">{{ fmt(item.potassium) }}</td><td class="px-4 py-3.5 tabular-nums text-slate-600">{{ fmt(item.ph) }}</td><td class="px-4 py-3.5 tabular-nums text-slate-600">{{ fmt(item.temperature) }} °C</td><td class="px-4 py-3.5 tabular-nums text-slate-600">{{ fmt(item.humidity) }}%</td><td class="px-4 py-3.5 tabular-nums text-slate-600">{{ fmt(item.rainfall) }} mm</td><td class="px-4 py-3.5"><span class="inline-flex rounded-full px-2.5 py-1 text-xs font-semibold" :class="status(item).class">{{ status(item).text }}</span></td>
    </tr><tr v-if="!paginatedData.length"><td colspan="9" class="px-4 py-12 text-center"><p class="font-semibold text-slate-700">{{ search ? "Data tidak ditemukan" : "Belum ada data monitoring" }}</p><p class="mt-1 text-sm text-slate-500">{{ search ? "Coba gunakan kata kunci tanggal yang berbeda." : "Data simulasi yang dikirim akan muncul di tabel ini." }}</p></td></tr></tbody>
  </table></div></div>
  <div class="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"><p class="text-xs text-slate-500">Halaman {{ currentPage }} dari {{ totalPages }}</p><div class="flex items-center justify-end gap-2"><button type="button" :disabled="currentPage === 1" @click="currentPage--" class="inline-flex min-h-9 items-center gap-1 rounded-lg border border-slate-200 px-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"><ChevronLeft class="h-4 w-4" /> Sebelumnya</button><button type="button" :disabled="currentPage >= totalPages" @click="currentPage++" class="inline-flex min-h-9 items-center gap-1 rounded-lg border border-slate-200 px-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40">Berikutnya <ChevronRight class="h-4 w-4" /></button></div></div>
</BaseCard>
</template>