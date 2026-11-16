<script setup>
import {
    Database,
    ClipboardList,
    Activity
} from "lucide-vue-next";

defineProps({
    summary: {
        type: Object,
        default: () => ({})
    }
});

const today = new Date().toLocaleDateString(
    "id-ID",
    {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric"
    }
);
</script>

<template>
    <section
        class="
            mb-6
            sm:mb-8
            overflow-hidden
            rounded-2xl
            sm:rounded-3xl
            bg-gradient-to-r
            from-green-700
            to-emerald-600
            p-5
            sm:p-6
            lg:p-8
            text-white
            shadow-sm
        "
    >
        <div class="flex flex-col xl:flex-row xl:items-start xl:justify-between gap-6">
            <div class="min-w-0 max-w-2xl">
                <p class="text-sm sm:text-base text-green-100">
                    Selamat Datang
                </p>

                <h1 class="mt-2 text-2xl sm:text-3xl lg:text-4xl font-bold leading-tight tracking-tight">
                    Dashboard Monitoring Durian
                </h1>

                <p class="mt-3 max-w-xl text-sm sm:text-base leading-relaxed text-green-100">
                    Monitoring kondisi tanah dan rekomendasi pemupukan tanaman durian dengan metode Fuzzy Tsukamoto.
                </p>

                <p class="mt-4 text-xs sm:text-sm text-green-100/90">
                    {{ today }}
                </p>
            </div>

            <div class="grid w-full max-w-xl grid-cols-2 gap-3 sm:gap-4 xl:max-w-sm">
                <div class="rounded-xl sm:rounded-2xl bg-white/15 p-4 sm:p-5 backdrop-blur-sm">
                    <Database class="mb-2 sm:mb-3 h-6 w-6 sm:h-8 sm:w-8 text-green-100" />
                    <p class="text-xs sm:text-sm text-green-50">
                        Monitoring
                    </p>
                    <p class="mt-1 text-2xl sm:text-3xl font-bold tabular-nums">
                        {{ summary.total_monitoring ?? 0 }}
                    </p>
                </div>

                <div class="rounded-xl sm:rounded-2xl bg-white/15 p-4 sm:p-5 backdrop-blur-sm">
                    <ClipboardList class="mb-2 sm:mb-3 h-6 w-6 sm:h-8 sm:w-8 text-green-100" />
                    <p class="text-xs sm:text-sm text-green-50">
                        Rekomendasi
                    </p>
                    <p class="mt-1 text-2xl sm:text-3xl font-bold tabular-nums">
                        {{ summary.total_recommendation ?? 0 }}
                    </p>
                </div>

                <div class="col-span-2 flex items-center gap-3 sm:gap-4 rounded-xl sm:rounded-2xl bg-white/15 p-4 sm:p-5 backdrop-blur-sm">
                    <Activity class="h-8 w-8 sm:h-10 sm:w-10 shrink-0 text-green-100" />
                    <div class="min-w-0">
                        <p class="font-semibold">
                            Sumber Data Simulasi
                        </p>
                        <p class="mt-0.5 text-xs sm:text-sm text-green-100">
                            API FastAPI terhubung
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
