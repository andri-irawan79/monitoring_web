<script setup>
defineProps({
    title: String,
    value: [String, Number],
    unit: String,
    icon: Object,
    status: {
        type: String,
        default: "Data simulasi"
    },
    color: {
        type: String,
        default: "green"
    }
});
</script>

<template>
    <div
        class="
            group
            relative
            h-full
            w-full
            overflow-hidden
            rounded-2xl
            sm:rounded-3xl
            border
            border-slate-200
            bg-gradient-to-br
            from-white
            to-green-50/70
            p-4
            sm:p-5
            lg:p-6
            shadow-sm
            transition-all
            duration-200
            hover:-translate-y-0.5
            hover:border-green-200
            hover:shadow-md
        "
    >
        <div
            class="
                pointer-events-none
                absolute
                -right-10
                -top-10
                h-28
                w-28
                rounded-full
                bg-green-100/50
                blur-3xl
            "
        />

        <div class="relative flex items-start justify-between gap-3">
            <div class="min-w-0 flex-1">
                <p class="text-sm font-medium text-slate-500">
                    {{ title }}
                </p>

                <h2 class="mt-2 break-words text-2xl sm:text-3xl font-bold leading-tight tracking-tight text-slate-800 tabular-nums">
                    {{ value ?? "-" }}
                </h2>

                <p v-if="unit" class="mt-1 text-xs sm:text-sm text-slate-400">
                    {{ unit }}
                </p>

                <div class="mt-4">
                    <span
                        class="
                            inline-flex
                            items-center
                            gap-2
                            rounded-full
                            bg-green-100
                            px-2.5
                            py-1.5
                            text-[11px]
                            sm:text-xs
                            font-semibold
                            text-green-700
                        "
                    >
                        <span class="h-1.5 w-1.5 rounded-full bg-green-600" />
                        {{ status }}
                    </span>
                </div>
            </div>

            <div
                class="
                    flex
                    h-11
                    w-11
                    sm:h-14
                    sm:w-14
                    shrink-0
                    items-center
                    justify-center
                    rounded-xl
                    sm:rounded-2xl
                    bg-green-100
                    text-green-700
                    transition-transform
                    duration-200
                    group-hover:scale-105
                "
            >
                <component :is="icon" class="h-5 w-5 sm:h-7 sm:w-7" />
            </div>
        </div>

        <div class="relative mt-4 flex justify-end border-t border-slate-100 pt-3">
            <span class="text-[11px] sm:text-xs font-medium text-slate-400">
                Tersimpan di sistem
            </span>
        </div>
    </div>
</template>
