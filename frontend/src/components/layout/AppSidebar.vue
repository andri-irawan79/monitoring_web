<script setup>
import {
    LayoutDashboard,
    // Activity,
    FlaskConical,
    Wifi,
    Info
} from "lucide-vue-next";

import { RouterLink, useRoute } from "vue-router";

const route = useRoute();

const menus = [

    {
        name: "Dashboard",
        icon: LayoutDashboard,
        path: "/"
    },

    // {
    //     name: "Monitoring",
    //     icon: Activity,
    //     path: "/monitoring"
    // },

    {
        name: "Rekomendasi",
        icon: FlaskConical,
        path: "/recommendation"
    }

];
</script>

<template>

<aside
class="
fixed
left-0
top-20
bottom-0
w-72
bg-white
border-r
border-slate-200
flex
flex-col
justify-between
overflow-y-auto
z-40
">

<div>

<div class="px-6 py-6">

<p
class="
text-xs
uppercase
tracking-widest
text-slate-400
font-semibold
">

Menu Utama

</p>

</div>

<nav class="px-4 space-y-2">

<RouterLink

v-for="menu in menus"

:key="menu.path"

:to="menu.path"

class="
flex
items-center
gap-3
px-4
py-3
rounded-xl
transition-all
duration-300
"

:class="

route.path === menu.path

?

'bg-green-100 text-green-700 font-semibold'

:

'text-slate-600 hover:bg-slate-100'

"

>

<component

:is="menu.icon"

class="w-5 h-5"

/>

{{ menu.name }}

</RouterLink>

</nav>

</div>

<div class="p-5">

<div
class="
bg-green-50
rounded-2xl
p-4
border
border-green-100
">

<div class="flex items-center gap-2">

<Wifi class="w-5 h-5 text-green-600"/>

<span class="font-semibold">

Simulator Online

</span>

</div>

<p class="text-sm text-slate-500 mt-2">

Backend FastAPI terhubung

</p>

</div>

<div
class="
mt-5
flex
items-center
gap-2
text-slate-400
text-sm
">

<Info class="w-4 h-4"/>

Versi 1.0.0

</div>

</div>

</aside>

</template>
