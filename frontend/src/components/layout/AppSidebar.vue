<script setup>
import { nextTick, ref } from "vue";
import {
    LayoutDashboard,
    FlaskConical,
    Wifi,
    Info,
    LogOut,
    CircleAlert
} from "lucide-vue-next";

import { RouterLink, useRoute, useRouter } from "vue-router";
import { logoutAccount } from "../../services/authService";

const route = useRoute();
const router = useRouter();

const showLogoutConfirm = ref(false);
const logoutButton = ref(null);
const cancelButton = ref(null);

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

const openLogoutConfirmation = async () => {
    showLogoutConfirm.value = true;
    await nextTick();
    cancelButton.value?.focus();
};

const closeLogoutConfirmation = async () => {
    showLogoutConfirm.value = false;
    await nextTick();
    logoutButton.value?.focus();
};

const confirmLogout = () => {
    showLogoutConfirm.value = false;
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

        <div class="p-4 pt-5 border-t border-slate-100 space-y-3">
            <button
                ref="logoutButton"
                type="button"
                @click="openLogoutConfirmation"
                aria-label="Keluar"
                class="
                    group
                    w-full
                    flex
                    items-center
                    gap-3
                    rounded-xl
                    border
                    border-rose-100
                    bg-rose-50/70
                    px-3
                    py-3
                    text-left
                    text-rose-700
                    transition-all
                    duration-200
                    hover:border-rose-200
                    hover:bg-rose-100
                    focus-visible:outline-none
                    focus-visible:ring-2
                    focus-visible:ring-rose-300
                    focus-visible:ring-offset-2
                "
            >
                <span
                    class="
                        flex
                        h-9
                        w-9
                        shrink-0
                        items-center
                        justify-center
                        rounded-lg
                        bg-rose-100
                        text-rose-600
                        transition-colors
                        group-hover:bg-rose-200
                    "
                >
                    <LogOut class="h-[18px] w-[18px]" />
                </span>

                <span class="text-sm font-semibold">
                    Keluar
                </span>
            </button>

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

            <div class="flex items-center gap-2 px-1 pt-1 text-slate-400 text-sm">
                <Info class="w-4 h-4" />
                <span>Versi 1.0.0</span>
            </div>
        </div>
    </aside>

    <Teleport to="body">
        <div
            v-if="showLogoutConfirm"
            class="
                fixed
                inset-0
                z-[100]
                flex
                items-center
                justify-center
                bg-slate-900/40
                px-4
                backdrop-blur-[2px]
            "
            role="presentation"
            @click.self="closeLogoutConfirmation"
            @keydown.esc.stop.prevent="closeLogoutConfirmation"
        >
            <section
                class="
                    w-full
                    max-w-sm
                    rounded-2xl
                    bg-white
                    p-6
                    shadow-2xl
                    ring-1
                    ring-slate-900/5
                "
                role="dialog"
                aria-modal="true"
                aria-labelledby="logout-dialog-title"
                aria-describedby="logout-dialog-description"
                @click.stop
            >
                <div
                    class="
                        mx-auto
                        flex
                        h-12
                        w-12
                        items-center
                        justify-center
                        rounded-full
                        bg-rose-50
                        text-rose-600
                    "
                >
                    <CircleAlert class="h-6 w-6" />
                </div>

                <div class="mt-4 text-center">
                    <h2
                        id="logout-dialog-title"
                        class="text-lg font-semibold text-slate-800"
                    >
                        Konfirmasi Keluar
                    </h2>
                    <p
                        id="logout-dialog-description"
                        class="mt-2 text-sm leading-6 text-slate-500"
                    >
                        Apakah Anda yakin ingin keluar dari akun?
                    </p>
                </div>

                <div class="mt-6 flex items-center justify-end gap-3">
                    <button
                        ref="cancelButton"
                        type="button"
                        @click="closeLogoutConfirmation"
                        class="
                            rounded-xl
                            border
                            border-slate-200
                            bg-white
                            px-4
                            py-2.5
                            text-sm
                            font-medium
                            text-slate-600
                            transition-colors
                            hover:bg-slate-50
                            focus-visible:outline-none
                            focus-visible:ring-2
                            focus-visible:ring-slate-300
                            focus-visible:ring-offset-2
                        "
                    >
                        Batal
                    </button>

                    <button
                        type="button"
                        @click="confirmLogout"
                        class="
                            rounded-xl
                            bg-rose-600
                            px-4
                            py-2.5
                            text-sm
                            font-semibold
                            text-white
                            transition-colors
                            hover:bg-rose-700
                            focus-visible:outline-none
                            focus-visible:ring-2
                            focus-visible:ring-rose-300
                            focus-visible:ring-offset-2
                        "
                    >
                        Keluar
                    </button>
                </div>
            </section>
        </div>
    </Teleport>
</template>
