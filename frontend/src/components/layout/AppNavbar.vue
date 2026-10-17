<script setup>
import {
  Leaf,
  Bell,
  CalendarDays,
  UserCircle2
} from "lucide-vue-next";

const today = new Date().toLocaleDateString("id-ID", {
  weekday: "long",
  day: "numeric",
  month: "long",
  year: "numeric"
});
</script>

<template>

<header
class="
fixed
top-0
left-0
right-0
z-50
bg-white/90
backdrop-blur-md
border-b
border-slate-200
shadow-sm
">

<div
class="
max-w-screen-2xl
mx-auto
px-8
h-20
flex
items-center
justify-between
">

<!-- Logo -->

<div class="flex items-center gap-4">

<div
class="
w-14
h-14
rounded-2xl
bg-green-100
flex
items-center
justify-center
">

<Leaf class="w-7 h-7 text-green-700"/>

</div>

<div>

<h1 class="text-2xl font-bold text-slate-800">

DASHBOARD MONITORING DURIAN

</h1>

<p class="text-sm text-slate-500">

Monitoring Nutrisi & Rekomendasi Pemupukan Durian

</p>

</div>

</div>

<!-- Right -->

<div
class="
flex
items-center
gap-6
">

<div
class="
hidden
md:flex
items-center
gap-2
text-slate-500
">

<CalendarDays class="w-5 h-5"/>

{{ today }}

</div>

<button
class="
relative
w-11
h-11
rounded-xl
bg-slate-100
hover:bg-green-100
transition
">

<Bell
class="
w-5
h-5
mx-auto
text-slate-600
"/>

<span
class="
absolute
top-2
right-2
w-2
h-2
rounded-full
bg-green-500
">
</span>

</button>

<div
class="
flex
items-center
gap-3
">

<UserCircle2
class="
w-10
h-10
text-green-700
"/>

<div class="hidden md:block">

<p class="font-semibold">

Administrator

</p>

<p
class="
text-sm
text-slate-500
">

Online

</p>

</div>

</div>

</div>

</div>

</header>

</template>
