<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import AppNavbar from "./AppNavbar.vue";
import AppSidebar from "./AppSidebar.vue";

const sidebarOpen = ref(false);

const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value;
};

const closeSidebar = () => {
    sidebarOpen.value = false;
};

const handleKeydown = (event) => {
    if (event.key === "Escape") {
        closeSidebar();
    }
};

onMounted(() => {
    window.addEventListener("keydown", handleKeydown);
});

onBeforeUnmount(() => {
    window.removeEventListener("keydown", handleKeydown);
});
</script>

<template>
    <div class="min-h-screen bg-[#f5f8f6]">
        <AppNavbar
            :sidebar-open="sidebarOpen"
            @toggle-sidebar="toggleSidebar"
        />

        <div class="flex min-h-[calc(100vh-5rem)] pt-20">
            <button
                v-if="sidebarOpen"
                type="button"
                class="
                    fixed
                    inset-x-0
                    top-20
                    bottom-0
                    z-30
                    bg-slate-950/35
                    backdrop-blur-[1px]
                    lg:hidden
                "
                aria-label="Tutup menu navigasi"
                @click="closeSidebar"
            />

            <AppSidebar
                :mobile-open="sidebarOpen"
                @close="closeSidebar"
            />

            <main
                class="
                    min-w-0
                    w-full
                    flex-1
                    px-4
                    py-5
                    sm:px-6
                    sm:py-7
                    xl:px-8
                    xl:py-8
                    lg:ml-72
                "
            >
                <div class="mx-auto w-full max-w-[1480px] min-w-0">
                    <slot />
                </div>
            </main>
        </div>
    </div>
</template>
