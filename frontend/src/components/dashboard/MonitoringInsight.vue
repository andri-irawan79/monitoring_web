<script setup>

defineProps({

    monitoring:{

        type:Object,

        default:()=>({})

    },

    summary:{

        type:Object,

        default:()=>({})

    }

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
mt-1
">

<h2 class="text-xl font-bold">

Insight Monitoring

</h2>

<p class="text-slate-500 mb-6">

Rata-rata kondisi nutrisi terbaru

</p>

<div class="grid md:grid-cols-2 gap-5">

<div
class="
flex
items-center
justify-between
rounded-xl
bg-green-50
border
border-green-100
p-5
">

<div>

<p class="text-slate-500">

Nitrogen

</p>

<!-- <h3 class="text-3xl font-bold mt-2">

{{ monitoring.nitrogen }}

<span class="text-base">

mg/kg

</span>

</h3> -->

<p class="text-sm text-slate-500 mt-2">

Rata-rata

<b>

{{ summary.avg_nitrogen }}

mg/kg

</b>

</p>

</div>

</div>

<div
class="rounded-xl bg-blue-50 p-4">

<p class="text-slate-500">

Fosfor

</p>

<!-- <h3 class="text-3xl font-bold">

{{ monitoring.phosphorus || "-" }}

mg/kg

</h3> -->

<p class="text-blue-700">

Rata-rata :

{{ summary.avg_phosphorus || "-" }}

mg/kg

</p>

</div>

<div
class="rounded-xl bg-orange-50 p-4">

<p class="text-slate-500">

Kalium

</p>

<!-- <h3 class="text-3xl font-bold">

{{ monitoring.potassium || "-" }}

mg/kg

</h3> -->

<p class="text-orange-700">

Rata-rata :

{{ summary.avg_potassium || "-" }}

mg/kg

</p>

</div>

<div
class="rounded-xl bg-emerald-50 p-4">

<p class="text-slate-500">

pH

</p>

<!-- <h3 class="text-3xl font-bold">

{{ monitoring.ph || "-" }}

</h3> -->

<p class="text-emerald-700">

Rata-rata :

{{ summary.avg_ph || "-" }}

</p>

</div>

</div>

</div>

</template>
