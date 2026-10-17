<script setup>

defineProps({
    monitoring:Object
})

</script>

<template>

<div
v-if="monitoring"
class="
grid
grid-cols-2
lg:grid-cols-4
gap-4
mb-8
">

    <div
    class="
    bg-white
    rounded-xl
    p-5
    shadow-sm
    border
    "
    >

        <p class="text-slate-500">
            Nitrogen
        </p>

        <h2 class="text-3xl font-bold">

            {{ monitoring.nitrogen }}

        </h2>

        <p class="text-sm text-slate-400">

            mg/kg

        </p>

    </div>

    <div
    class="
    bg-white
    rounded-xl
    p-5
    shadow-sm
    border
    "
    >

        <p class="text-slate-500">
            Fosfor
        </p>

        <h2 class="text-3xl font-bold">

            {{ monitoring.phosphorus }}

        </h2>

        <p class="text-sm text-slate-400">

            mg/kg

        </p>

    </div>

    <div
    class="
    bg-white
    rounded-xl
    p-5
    shadow-sm
    border
    "
    >

        <p class="text-slate-500">
            Kalium
        </p>

        <h2 class="text-3xl font-bold">

            {{ monitoring.potassium }}

        </h2>

        <p class="text-sm text-slate-400">

            mg/kg

        </p>

    </div>

    <div
    class="
    bg-white
    rounded-xl
    p-5
    shadow-sm
    border
    "
    >

        <p class="text-slate-500">
            pH
        </p>

        <h2 class="text-3xl font-bold">

            {{ Number(monitoring.ph).toFixed(1) }}

        </h2>

    </div>

</div>

</template>
