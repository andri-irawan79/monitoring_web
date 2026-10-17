<script setup>

import {
    Database,
    ClipboardList,
    Activity
} from "lucide-vue-next";

defineProps({

    summary:{

        type:Object,

        default:()=>({})
    }

});

const today = new Date().toLocaleDateString(

    "id-ID",

    {

        weekday:"long",

        day:"numeric",

        month:"long",

        year:"numeric"

    }

);

</script>

<template>

<div
class="
mb-8
rounded-3xl
bg-gradient-to-r
from-green-600
to-emerald-500
text-white
p-8
shadow-lg
">

<div
class="
flex
justify-between
items-start
flex-wrap
gap-6
">

<div>

<p
class="
text-green-100
text-lg
"
>

Selamat Datang 👋

</p>

<h1
class="
text-4xl
font-bold
mt-2
"
>

Dashboard Monitoring Durian

</h1>

<p
class="
mt-3
text-green-100
"
>

Implementasi Fuzzy Logic untuk Monitoring Kondisi Tanah
dan Rekomendasi Pemupukan Tanaman Durian

</p>

<p
class="
mt-4
text-green-200
"
>

{{ today }}

</p>

</div>

<div
class="
grid
grid-cols-2
gap-4
min-w-[300px]
">

<div
class="
bg-white/20
rounded-2xl
p-5
backdrop-blur
">

<Database class="w-8 h-8 mb-3"/>

<p class="text-sm">

Monitoring

</p>

<p
class="
text-3xl
font-bold
"
>

{{ summary.total_monitoring }}

</p>

</div>

<div
class="
bg-white/20
rounded-2xl
p-5
backdrop-blur
">

<ClipboardList class="w-8 h-8 mb-3"/>

<p class="text-sm">

Rekomendasi

</p>

<p
class="
text-3xl
font-bold
"
>

{{ summary.total_recommendation }}

</p>

</div>

<div
class="
col-span-2
bg-white/20
rounded-2xl
p-5
flex
items-center
gap-4
">

<Activity
class="
w-10
h-10
text-green-200
"/>

<div>

<p class="font-semibold">

Status Sistem

</p>

<p class="text-green-100">

Simulator Aktif • Backend Online

</p>

</div>

</div>

</div>

</div>

</div>

</template>
