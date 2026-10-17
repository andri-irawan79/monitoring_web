<script setup>
import { exportRecommendationCSV } from "../../services/recommendationService";

</script>

<template>

<div>

  <h2>Riwayat Rekomendasi</h2>
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

  <table>

    <thead>

      <tr>

        <th>ID</th>
        <th>Pupuk</th>
        <th>Dosis</th>
        <th>Kategori</th>

      </tr>

    </thead>

    <tbody>

      <tr
        v-for="item in recommendations"
        :key="item.id"
      >

        <td>{{ item.id }}</td>
        <td>{{ item.jenis_pupuk }}</td>
        <td>{{ item.dosis }}</td>
        <td>{{ item.kategori }}</td>

      </tr>

    </tbody>

  </table>

</div>

</template>

<script setup>

defineProps({
  recommendations: Array
})

</script>
