<script setup>

import StatCard from "../ui/StatCard.vue";

import {
    Database,
    ClipboardList,
    Leaf,
    FlaskConical
} from "lucide-vue-next";

defineProps({

    summary:{

        type:Object,

        default:()=>({})

    }

});

</script>

<template>

<div
    class="
        grid
        grid-cols-1
        md:grid-cols-2
        xl:grid-cols-4
        gap-6
        mb-8
    "
>

    <StatCard

        title="Total Monitoring"

        :value="summary.total_monitoring"

        :icon="Database"

    />

    <StatCard

        title="Total Rekomendasi"

        :value="summary.total_recommendation"

        :icon="ClipboardList"

    />

    <StatCard

        title="Rata-rata Nitrogen"

        :value="summary.avg_nitrogen"

        unit="ppm"

        :icon="Leaf"

    />

    <StatCard

        title="Rata-rata pH"

        :value="summary.avg_ph"

        :icon="FlaskConical"

    />

</div>

</template>
