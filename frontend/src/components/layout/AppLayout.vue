<script setup>

import AppNavbar from "./AppNavbar.vue";
import AppSidebar from "./AppSidebar.vue";

</script>

<template>

<div
    class="
        min-h-screen
        bg-slate-100
    "
>

    <!-- Navbar -->

    <AppNavbar/>

    <!-- Body -->

    <div
        class="
            flex
            pt-20
        "
    >

        <!-- Sidebar -->

        <AppSidebar/>

        <!-- Content -->

        <main
            class="
            flex-1
            ml-72
            p-8
            overflow-y-auto
            "
        >

            <div
                class="
                    max-w-7xl
                    mx-auto
                "
            >

                <slot/>

            </div>

        </main>

    </div>

</div>

</template>
