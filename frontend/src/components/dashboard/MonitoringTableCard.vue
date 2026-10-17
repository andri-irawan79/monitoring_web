<script setup>
import { computed, ref } from "vue";
import BaseCard from "../ui/BaseCard.vue";

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
});

const search = ref("");

// const filteredData = computed(() => {
//   if (!search.value) return props.data;

//   return props.data.filter((item) =>
//     item.simulation_date
//       ?.toLowerCase()
//       .includes(search.value.toLowerCase())
//   );
// });
// Nanti ubah jadi bagination dari backend
const filteredData = computed(() => {

  let data = props.data;

  if (search.value) {

    data = data.filter(item =>
      item.simulation_date
        ?.toLowerCase()
        .includes(search.value.toLowerCase())
    );

  }

  // hanya tampilkan 10 data terbaru
  return data.slice(0, 10);

});

function status(item) {
  if (
    item.nitrogen < 40 ||
    item.phosphorus < 30 ||
    item.potassium < 30
  ) {
    return {
      text: "Rendah",
      class: "bg-red-100 text-red-700"
    };
  }

  if (
    item.nitrogen > 90 ||
    item.phosphorus > 80 ||
    item.potassium > 70
  ) {
    return {
      text: "Tinggi",
      class: "bg-yellow-100 text-yellow-700"
    };
  }

  return {
    text: "Normal",
    class: "bg-green-100 text-green-700"
  };
}
</script>

<template>

<BaseCard>

    <div class="flex justify-between items-center mb-6">

        <div>

            <h2 class="text-xl font-bold">
                Riwayat Monitoring
            </h2>

            <p class="text-slate-500 text-sm">
                10 data monitoring terbaru
            </p>

        </div>

        <input
            v-model="search"
            type="text"
            placeholder="Cari tanggal..."
            class="border rounded-xl px-4 py-2 text-sm w-56"
        >

    </div>

    <div class="overflow-x-auto">

        <table class="min-w-full">

            <thead>

                <tr
                    class="
                        border-b
                        text-left
                        text-slate-500
                    "
                >

                    <th class="py-3 px-4">Tanggal</th>
                    <th class="py-3 px-4">N</th>
                    <th class="py-3 px-4">P</th>
                    <th class="py-3 px-4">K</th>
                    <th class="py-3 px-4">pH</th>
                    <th class="py-3 px-4">Suhu</th>
                    <th class="py-3 px-4">Kelembapan</th>
                    <th class="py-3 px-4">Curah Hujan</th>
                    <th class="py-3 px-4">Status</th>

                </tr>

            </thead>

            <tbody>

                <tr
                    v-for="item in filteredData"
                    :key="item.id"
                    class="
                        border-b
                        hover:bg-slate-50
                        transition
                    "
                >

                    <td class="px-4 py-3">
                        {{ item.simulation_date }}
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
                        {{ Number(item.temperature).toFixed(1) }}
                    </td>

                    <td class="px-4 py-3">
                        {{ Number(item.humidity).toFixed(1) }}
                    </td>

                    <td class="px-4 py-3">
                        {{ Number(item.rainfall).toFixed(1) }}
                    </td>

                    <td class="px-4 py-3">

                        <span
                            class="px-3 py-1 rounded-full text-xs font-medium"
                            :class="status(item).class"
                        >

                            {{ status(item).text }}

                        </span>

                    </td>

                </tr>

            </tbody>

        </table>

    </div>

</BaseCard>

</template>
