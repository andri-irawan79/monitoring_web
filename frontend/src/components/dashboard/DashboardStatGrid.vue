<script setup>
import {
    Leaf,
    FlaskConical,
    Droplets,
    Thermometer,
    CloudRain,
    Calendar
} from "lucide-vue-next";

import StatCard from "../ui/StatCard.vue";

defineProps({
    monitoring: Object
});
</script>

<template>

<div
    v-if="monitoring"
     class="
        grid
        grid-cols-1
        sm:grid-cols-2
        lg:grid-cols-4
        gap-6
    "
>

    <StatCard
        title="Nitrogen"
        :value="monitoring.nitrogen"
        unit="mg/kg"
        :icon="Leaf"
    />

    <StatCard
        title="Fosfor"
        :value="monitoring.phosphorus"
        unit="mg/kg"
        :icon="FlaskConical"
    />

    <StatCard
        title="Kalium"
        :value="monitoring.potassium"
        unit="mg/kg"
        :icon="Droplets"
    />

   <StatCard
        title="pH"
        :value="Number(monitoring.ph).toFixed(1)"
        :icon="FlaskConical"
    />

    <StatCard
        title="Suhu"
        :value="monitoring.temperature.toFixed(1)"
        unit="°C"
        :icon="Thermometer"
    />

    <StatCard
        title="Kelembaban"
        :value="monitoring.humidity.toFixed(1)"
        unit="%"
        :icon="Droplets"
    />

    <StatCard
        title="Curah Hujan"
        :value="monitoring.rainfall.toFixed(1)"
        unit="mm"
        :icon="CloudRain"
    />

    <StatCard
        title="Update Terakhir"
        :value="monitoring.simulation_date"
        :icon="Calendar"
    />

</div>

</template>
