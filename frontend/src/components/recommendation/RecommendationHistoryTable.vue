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

    if (!kategori)
        return "bg-slate-100 text-slate-700";

    kategori = kategori.toLowerCase();

    if (kategori === "tinggi")
        return "bg-red-100 text-red-700";

    if (kategori === "sedang")
        return "bg-yellow-100 text-yellow-700";

    return "bg-green-100 text-green-700";

}
</script>

<template>

<BaseCard>

    <div class="flex justify-between items-center mb-6">

        <div>

            <h2 class="text-xl font-bold">

                Riwayat Rekomendasi

            </h2>

            <p class="text-slate-500 text-sm">

                10 rekomendasi terakhir

            </p>

        </div>
        <div class="flex justify-end mb-4">
        <button
            @click="exportRecommendationCSV"

            class="

                bg-green-600

                hover:bg-green-700

                text-white

                px-4

                py-2

                rounded-lg

            "
        >
            Export CSV

        </button>
    </div>

    </div>

    <div class="overflow-x-auto">

        <table class="min-w-full">

            <thead>

                <tr class="border-b text-left text-slate-500">

                    <th class="px-4 py-3">Tanggal</th>

                    <th class="px-4 py-3">N</th>

                    <th class="px-4 py-3">P</th>

                    <th class="px-4 py-3">K</th>

                    <th class="px-4 py-3">pH</th>

                    <th class="px-4 py-3">Varietas</th>

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
                    class="
                        border-b
                        hover:bg-slate-50
                        transition
                    "
                >

                    <td class="px-4 py-3">

                        {{ item.created_at }}

                    </td>

                    <td class="px-4 py-3">

                        {{ item.nitrogen }}

                    </td>

                    <td class="px-4 py-3">

                        {{ item.phosphorus }}

                    </td>

                    <td class="px-4 py-3">

                        {{ item.potassium }}

                    </td>

                    <td class="px-4 py-3">

                        {{ Number(item.ph).toFixed(1) }}

                    </td>

                    <td class="px-4 py-3">

                        {{ item.varietas }}

                    </td>

                    <td class="px-4 py-3">

                        {{ item.fase }}

                    </td>

                    <td class="px-4 py-3">

                        {{ item.jenis_pupuk }}

                    </td>

                    <td class="px-4 py-3">

                        {{ item.dosis }}

                        kg

                    </td>

                    <td class="px-4 py-3">

                        <span
                            class="
                                px-3
                                py-1
                                rounded-full
                                text-xs
                                font-medium
                            "
                            :class="badge(item.kategori)"
                        >

                            {{ item.kategori }}

                        </span>

                    </td>

                </tr>

            </tbody>

        </table>

    </div>

</BaseCard>

</template>
