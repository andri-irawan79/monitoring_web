<script setup>

defineProps({
  data: Array
})

</script>

<template>

  <div class="table-container">

    <h2>Riwayat Monitoring</h2>

    <table>

      <thead>
        <tr>
          <th>Tanggal</th>
          <th>N</th>
          <th>P</th>
          <th>K</th>
          <th>pH</th>
          <th>Suhu</th>
          <th>Kelembaban</th>
          <th>Curah Hujan</th>
        </tr>
      </thead>

      <tbody>

        <tr
          v-for="row in data"
          :key="row.id"
        >
          <td>{{ row.simulation_date }}</td>
          <td>{{ row.nitrogen }}</td>
          <td>{{ row.phosphorus }}</td>
          <td>{{ row.potassium }}</td>
          <td>{{ row.ph }}</td>
          <td>{{ row.temperature.toFixed(2) }}</td>
          <td>{{ row.humidity.toFixed(2) }}</td>
          <td>{{ row.rainfall.toFixed(2) }}</td>
        </tr>

      </tbody>

    </table>

  </div>

</template>

<style scoped>

.table-container{
  margin-top:40px;
}

table{
  width:100%;
  border-collapse:collapse;
}

th,
td{
  border:1px solid #ddd;
  padding:10px;
  text-align:center;
}

th{
  background:#f4f4f4;
}

</style>
