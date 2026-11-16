<script setup>
import {
    LayoutDashboard,
    FlaskConical,
    Wifi,
    Info,
    LogOut
} from "lucide-vue-next";

import { RouterLink, useRoute, useRouter } from "vue-router";
import { logoutAccount } from "../../services/authService";

const route = useRoute();
const router = useRouter();

const menus = [
    {
        name: "Dashboard",
        icon: LayoutDashboard,
        path: "/"
    },
    {
        name: "Rekomendasi",
        icon: FlaskConical,
        path: "/recommendation"
    }
];

const handleLogout = () => {
    logoutAccount();
    router.replace("/login");
};
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
        "
    >
        <div>
            <div class="px-6 py-6">
                <p class="text-xs uppercase tracking-widest text-slate-400 font-semibold">
                    Menu Utama
                </p>
            </div>

            <nav class="px-4 space-y-2" aria-label="Navigasi utama">
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
                        duration-200
                    "
                    :class="
                        route.path === menu.path
                            ? 'bg-green-100 text-green-700 font-semibold'
                            : 'text-slate-600 hover:bg-slate-100'
                    "
                    :aria-current="route.path === menu.path ? 'page' : undefined"
                >
                    <component :is="menu.icon" class="w-5 h-5 shrink-0" />
                    <span>{{ menu.name }}</span>
                </RouterLink>
            </nav>
        </div>

        <div class="p-4 pt-5 border-t border-slate-100 space-y-4">
            <div class="bg-green-50 rounded-2xl p-4 border border-green-100">
                <div class="flex items-center gap-2">
                    <Wifi class="w-5 h-5 text-green-600" />
                    <span class="font-semibold text-slate-800">
                        Simulator Online
                    </span>
                </div>
                <p class="text-sm text-slate-500 mt-2">
                    Backend FastAPI terhubung
                </p>
            </div>

            <div class="flex items-center gap-2 px-1 text-slate-400 text-sm">
                <Info class="w-4 h-4" />
                <span>Versi 1.0.0</span>
            </div>

            <button
                type="button"
                @click="handleLogout"
                aria-label="Keluar dari akun"
                class="
                    group
                    w-full
                    flex
                    items-center
                    gap-3
                    rounded-xl
                    border
                    border-slate-200
                    bg-white
                    px-3
                    py-3
                    text-left
                    text-rose-600
                    transition-all
                    duration-200
                    hover:border-rose-200
                    hover:bg-rose-50
                    focus-visible:outline-none
                    focus-visible:ring-2
                    focus-visible:ring-rose-300
                    focus-visible:ring-offset-2
                "
            >
                <span
                    class="
                        flex
                        h-10
                        w-10
                        shrink-0
                        items-center
                        justify-center
                        rounded-lg
                        bg-rose-50
                        transition-colors
                        group-hover:bg-rose-100
                    "
                >
                    <LogOut class="h-5 w-5" />
                </span>

                <span class="min-w-0 flex-1">
                    <span class="block text-sm font-semibold">
                        Keluar
                    </span>
                    <span class="mt-0.5 block text-xs text-slate-500">
                        Akhiri sesi akun
                    </span>
                </span>
            </button>
        </div>
    </aside>
</template>
