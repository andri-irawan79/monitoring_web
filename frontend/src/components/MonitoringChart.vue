<script setup>

import { computed } from "vue";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from "chart.js";

import { Line } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const props = defineProps({
  data: Array
});

const latestData = computed(() =>
  [...props.data]
    .reverse()
    .slice(-30)
)

const chartData = computed(() => ({

      labels: latestData.value.map(
        row => row.simulation_date
    ),

  datasets: [

  {
    label: "Nitrogen",
    data: latestData.value.map(
      row => row.nitrogen
    ),

        borderColor: "#22c55e",
        backgroundColor: "rgba(34,197,94,0.12)",

        fill: true,

        borderWidth: 3,

        pointRadius: 4,

        pointHoverRadius: 7,

        pointBackgroundColor: "#22c55e",

        pointBorderColor: "#fff",

        pointBorderWidth: 2,

        tension: 0.45
  },

  {
    label: "Fosfor",
    data: latestData.value.map(
      row => row.phosphorus
    ),

        borderColor:"#3b82f6",
        backgroundColor:"rgba(59,130,246,0.12)",

        fill: true,

        borderWidth: 3,

        pointRadius: 4,

        pointHoverRadius: 7,

        pointBackgroundColor: "#3b82f6",

        pointBorderColor: "#fff",

        pointBorderWidth: 2,

        tension: 0.45
  },

  {
    label: "Kalium",
    data: latestData.value.map(
      row => row.potassium
    ),

        borderColor:"#f59e0b",
        backgroundColor:"rgba(245,158,11,0.12)",

        fill: true,

        borderWidth: 3,

        pointRadius: 4,

        pointHoverRadius: 7,

        pointBackgroundColor: "#f59e0b",

        pointBorderColor: "#fff",

        pointBorderWidth: 2,

        tension: 0.45
  }

]

}));

const chartOptions = {

  responsive: true,

  maintainAspectRatio: false,

  interaction: {
    mode: "index",
    intersect: false
  },

  plugins: {

    legend: {

      position: "top",

      labels: {

        usePointStyle: true,

        pointStyle: "circle",

        padding: 20,

        font: {

          size: 13,

          weight: "bold"

        }

      }

    },

    tooltip: {

      backgroundColor: "#ffffff",

      titleColor: "#111827",

      bodyColor: "#374151",

      borderColor: "#e5e7eb",

      borderWidth: 1,

      padding: 12,

      displayColors: true

    }

  },

  scales: {

    x: {

      grid: {

        display: false,

      },

      ticks: {

        color: "#64748b",
        autoSkip:true,
        maxTicksLimit:10

      }

    },

    y: {

      beginAtZero: true,

      grid: {

        color:"#f1f5f9"

      },

      ticks: {

        color: "#64748b"

      }

    }

  }

}

</script>

<template>

  <div class="chart-container bg-white rounded-2xl p-6">

    <div class="h-[455px]">
      <Line
        :data="chartData"
        :options="chartOptions"
      />
    </div>

  </div>

</template>

<style scoped>

.chart-container{

  margin-top:30px;

  border-radius:24px;

}

.chart-container h2{

  font-size:24px;

  font-weight:700;

  color:#1e293b;

  margin-bottom:20px;

}

</style>
