<script setup>
import MonitoringChart from "../MonitoringChart.vue";

defineProps({
    data: Array
});
</script>

<template>

<div
    class="
        bg-white
        rounded-2xl
        shadow-sm
        border
        border-slate-200
        p-6
    "
>

    <div class="mb-6">

        <h2 class="text-xl font-semibold">

            Grafik Monitoring Nutrisi

        </h2>

        <p class="text-slate-500 text-sm">

            Perubahan nilai nutrisi tanaman

        </p>

    </div>

    <MonitoringChart
        :data="data"
    />

</div>

</template>
