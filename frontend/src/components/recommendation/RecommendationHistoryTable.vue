<script setup>
import { computed, ref, watch } from "vue";
import {
  Download,
  Trash2,
  ChevronLeft,
  ChevronRight,
  ClipboardList,
  Search
} from "lucide-vue-next";
import BaseCard from "../ui/BaseCard.vue";
import { exportRecommendationCSV } from "../../services/recommendationService";

const props = defineProps({
  recommendations: { type: Array, default: () => [] },
  totalCount: { type: Number, default: null },
  deletingId: { type: [Number, String], default: null }
});
const emit = defineEmits(["delete"]);

const search = ref("");
const currentPage = ref(1);
const perPage = 10;

function formatStoredTimestamp(value) {
  if (!value) return "—";
  const match = String(value).match(
    /^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})(?::(\d{2}))?/
  );
  if (!match) return String(value);
  const [, year, month, day, hour, minute, second = "00"] = match;
  const date = new Date(Number(year), Number(month) - 1, Number(day));
  const dateLabel = new Intl.DateTimeFormat("id-ID", {
    day: "2-digit",
    month: "short",
    year: "numeric"
  }).format(date);
  return `${dateLabel}, ${hour}:${minute}:${second}`;
}

const filteredRecommendations = computed(() => {
  const term = search.value.trim().toLowerCase();
  return term
    ? props.recommendations.filter((item) =>
        [String(item.created_at || ""), formatStoredTimestamp(item.created_at)]
          .join(" ").toLowerCase().includes(term)
      )
    : props.recommendations;
});

const totalItems = computed(() => filteredRecommendations.value.length);
const totalStored = computed(() => {
  if (props.totalCount === null || props.totalCount === undefined) {
    return props.recommendations.length;
  }
  const count = Number(props.totalCount);
  return Number.isFinite(count) ? Math.max(0, count) : props.recommendations.length;
});
const totalPages = computed(() => Math.max(1, Math.ceil(totalItems.value / perPage)));
const paginatedData = computed(() =>
  filteredRecommendations.value.slice(
    (currentPage.value - 1) * perPage,
    currentPage.value * perPage
  )
);
const startItem = computed(() =>
  totalItems.value ? (currentPage.value - 1) * perPage + 1 : 0
);
const endItem = computed(() =>
  Math.min(currentPage.value * perPage, totalItems.value)
);

watch(search, () => {
  currentPage.value = 1;
});
watch(totalPages, (pages) => {
  if (currentPage.value > pages) currentPage.value = pages;
});

function fmt(value, digits = 2) {
  const n = Number(value);
  return Number.isFinite(n) ? n.toFixed(digits) : "-";
}

function doseText(detail) {
  if (detail.dosis_g !== null && detail.dosis_g !== undefined) {
    return Number(detail.dosis_g).toLocaleString("id-ID") + " g";
  }
  if (detail.dosis_min_g !== null && detail.dosis_min_g !== undefined) {
    return Number(detail.dosis_min_g).toLocaleString("id-ID") + "–" +
      Number(detail.dosis_maks_g).toLocaleString("id-ID") + " g";
  }
  if (detail.dosis_kg !== null && detail.dosis_kg !== undefined) {
    return Number(detail.dosis_kg).toFixed(2) + " kg";
  }
  return "-";
}

function fertilizerSummary(item) {
  const details = (item.items || []).filter((detail) => detail.direkomendasikan);
  if (details.length) {
    return details.map((detail) => detail.nama_pupuk + " (" + doseText(detail) + ")").join(" · ");
  }
  return item.jenis_pupuk || "Tidak ada dosis pupuk yang disarankan";
}
</script>

<template>
  <BaseCard id="recommendation-history" class="scroll-mt-24 w-full min-w-0">
    <div class="mb-5 flex flex-col gap-4 border-b border-slate-100 pb-5 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex items-start gap-3">
        <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700">
          <ClipboardList class="h-5 w-5" />
        </div>
        <div>
          <h2 class="text-lg font-bold tracking-tight text-slate-800">Riwayat Rekomendasi</h2>
          <p class="mt-1 text-sm text-slate-500">Daftar hasil rekomendasi pemupukan Durian Montong</p>
        </div>
      </div>

      <div class="flex w-full flex-col gap-2 sm:w-auto sm:flex-row sm:items-center">
        <div class="relative w-full sm:w-64">
          <Search class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            v-model="search"
            type="search"
            placeholder="Cari tanggal..."
            aria-label="Cari tanggal rekomendasi"
            class="min-h-10 w-full rounded-xl border border-slate-200 bg-white py-2 pl-9 pr-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-50"
          />
        </div>

        <button
          type="button"
          @click="exportRecommendationCSV"
          class="inline-flex min-h-10 w-full shrink-0 items-center justify-center gap-2 rounded-xl bg-emerald-700 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 sm:w-auto"
        >
          <Download class="h-4 w-4" />
          Export CSV
        </button>
      </div>
    </div>

    <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
      <p class="text-sm text-slate-500">
        Menampilkan
        <span class="font-semibold text-slate-700">{{ startItem }}–{{ endItem }}</span>
        dari
        <span class="font-semibold text-slate-700">{{ totalItems }}</span>
        {{ search ? "hasil pencarian pada 10 rekomendasi terbaru" : "rekomendasi terbaru" }}
        <span v-if="totalStored > recommendations.length" class="ml-1 text-slate-400">· Total tersimpan: {{ totalStored }}</span>
      </p>
      <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
        10 data per halaman
      </span>
    </div>

    <div class="overflow-hidden rounded-xl border border-slate-200">
      <div class="overflow-x-auto">
        <table class="min-w-[1220px] w-full whitespace-nowrap text-sm">
          <thead class="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
            <tr>
              <th class="px-4 py-3.5">Waktu dibuat</th>
              <th class="px-4 py-3.5">N (ppm)</th>
              <th class="px-4 py-3.5">P (ppm)</th>
              <th class="px-4 py-3.5">K (ppm)</th>
              <th class="px-4 py-3.5">pH</th>
              <th class="px-4 py-3.5">Kelembapan Tanah</th>
              <th class="px-4 py-3.5">Objek Tanaman</th>
              <th class="px-4 py-3.5">Fase</th>
              <th class="px-4 py-3.5">Rincian Pupuk</th>
              <th class="px-4 py-3.5 text-right">Aksi</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-slate-100 bg-white">
            <tr
              v-for="item in paginatedData"
              :key="item.id"
              class="transition-colors hover:bg-emerald-50/40"
            >
              <td class="px-4 py-3.5 font-medium text-slate-700">{{ formatStoredTimestamp(item.created_at) }}</td>
              <td class="px-4 py-3.5 tabular-nums text-slate-600">{{ fmt(item.nitrogen) }}</td>
              <td class="px-4 py-3.5 tabular-nums text-slate-600">{{ fmt(item.phosphorus) }}</td>
              <td class="px-4 py-3.5 tabular-nums text-slate-600">{{ fmt(item.potassium) }}</td>
              <td class="px-4 py-3.5 tabular-nums text-slate-600">{{ fmt(item.ph) }}</td>
              <td class="px-4 py-3.5 tabular-nums text-slate-600">{{ item.soil_moisture === null || item.soil_moisture === undefined ? "-" : fmt(item.soil_moisture) + " %" }}</td>
              <td class="px-4 py-3.5 text-slate-600">{{ item.objek_tanaman || "Durian Montong" }}</td>
              <td class="px-4 py-3.5 text-slate-600">{{ item.fase }}</td>
              <td class="max-w-[460px] whitespace-normal px-4 py-3.5 font-medium leading-6 text-slate-700">
                {{ fertilizerSummary(item) }}
              </td>
              <td class="px-4 py-3.5 text-right">
                <button
                  type="button"
                  :disabled="deletingId === item.id"
                  @click="emit('delete', item)"
                  class="inline-flex min-h-9 items-center gap-1.5 rounded-lg border border-rose-200 px-3 text-xs font-semibold text-rose-700 transition hover:bg-rose-50 disabled:cursor-wait disabled:opacity-50"
                >
                  <Trash2 class="h-3.5 w-3.5" />
                  {{ deletingId === item.id ? "Menghapus..." : "Hapus" }}
                </button>
              </td>
            </tr>

            <tr v-if="!paginatedData.length">
              <td colspan="10" class="px-4 py-12 text-center">
                <p class="font-semibold text-slate-700">
                  {{ search ? "Data tidak ditemukan" : "Belum ada riwayat rekomendasi" }}
                </p>
                <p class="mt-1 text-sm text-slate-500">
                  {{ search
                    ? "Coba gunakan kata kunci tanggal yang berbeda."
                    : "Rekomendasi yang berhasil dibuat akan muncul di sini." }}
                </p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <p class="text-xs text-slate-500">Halaman {{ currentPage }} dari {{ totalPages }}</p>
      <div class="flex items-center justify-end gap-2">
        <button
          type="button"
          :disabled="currentPage === 1"
          @click="currentPage--"
          class="inline-flex min-h-9 items-center gap-1 rounded-lg border border-slate-200 px-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
        >
          <ChevronLeft class="h-4 w-4" />
          Sebelumnya
        </button>
        <button
          type="button"
          :disabled="currentPage >= totalPages"
          @click="currentPage++"
          class="inline-flex min-h-9 items-center gap-1 rounded-lg border border-slate-200 px-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Berikutnya
          <ChevronRight class="h-4 w-4" />
        </button>
      </div>
    </div>
  </BaseCard>
</template>
