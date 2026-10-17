<script setup>

import BaseCard from "../ui/BaseCard.vue";

defineProps({

    fuzzy:{
        type:Object,
        default:null
    }

})

const width = (value)=>{

    return `${value*100}%`

}

</script>

<template>

<BaseCard>

    <h2
        class="
            text-2xl
            font-bold
            mb-6
        "
    >

        Hasil Fuzzifikasi

    </h2>

    <div
        v-if="fuzzy"
        class="space-y-8"
    >

        <div
            v-for="(groups,name) in fuzzy"
            :key="name"
        >

            <h3
                class="
                    font-semibold
                    text-lg
                    mb-4
                "
            >

                {{ name }}

            </h3>

            <div
                v-for="(nilai,label) in groups"
                :key="label"
                class="mb-4"
            >

                <div
                    class="
                        flex
                        justify-between
                        text-sm
                        mb-2
                    "
                >

                    <span>

                        {{ label }}

                    </span>

                    <span>

                        {{ Number(nilai).toFixed(3) }}

                    </span>

                </div>

                <div
                    class="
                        w-full
                        h-3
                        rounded-full
                        bg-slate-200
                    "
                >

                    <div

                        class="
                            h-3
                            rounded-full
                            bg-green-600
                        "

                        :style="{

                            width:width(nilai)

                        }"

                    />

                </div>

            </div>

        </div>

    </div>

    <div
        v-else
        class="
            text-center
            text-slate-400
            py-8
        "
    >

        Belum ada proses fuzzifikasi

    </div>

</BaseCard>

</template>
