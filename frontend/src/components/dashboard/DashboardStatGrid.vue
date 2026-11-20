<script setup>
import { Leaf, FlaskConical, Droplets, Thermometer, CloudRain, Waves } from "lucide-vue-next";
import StatCard from "../ui/StatCard.vue";

defineProps({ monitoring: Object });
const safeFixed = (value, digits = 2) => {
  const number = Number(value);
  return Number.isFinite(number) ? number.toFixed(digits) : "-";
};
</script>

<template>
  <div v-if="monitoring" class="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
    <StatCard title="Nitrogen" :value="safeFixed(monitoring.nitrogen)" unit="mg/kg" :icon="Leaf" color="emerald" />
    <StatCard title="Fosfor" :value="safeFixed(monitoring.phosphorus)" unit="mg/kg" :icon="FlaskConical" color="blue" />
    <StatCard title="Kalium" :value="safeFixed(monitoring.potassium)" unit="mg/kg" :icon="Droplets" color="amber" />
    <StatCard title="pH Tanah" :value="safeFixed(monitoring.ph, 2)" unit="Skala pH" :icon="Waves" color="violet" />
    <StatCard title="Suhu" :value="safeFixed(monitoring.temperature)" unit="°C" :icon="Thermometer" color="orange" />
    <StatCard title="Kelembapan Udara" :value="safeFixed(monitoring.humidity)" unit="%" :icon="Droplets" color="cyan" />
    <StatCard v-if="monitoring.soil_moisture !== null && monitoring.soil_moisture !== undefined" title="Kelembapan Tanah" :value="safeFixed(monitoring.soil_moisture)" unit="%" :icon="Droplets" color="teal" />
    <StatCard title="Curah Hujan" :value="safeFixed(monitoring.rainfall)" unit="mm" :icon="CloudRain" color="sky" />
  </div>
</template>
