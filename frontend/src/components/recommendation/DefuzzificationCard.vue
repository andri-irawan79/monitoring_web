<script setup>
import BaseCard from "../ui/BaseCard.vue";

defineProps({
    result: {
        type: Object,
        default: () => ({})
    }
});
</script>

<template>

<BaseCard>

    <h2 class="text-2xl font-bold mb-6">

        Defuzzifikasi Tsukamoto

    </h2>

    <div
        class="grid md:grid-cols-3 gap-6"
    >

        <div
            class="bg-slate-50 rounded-xl p-5 text-center"
        >

            <p class="text-slate-500">

                Σ(α × z)

            </p>

            <h2 class="text-3xl font-bold mt-2">

                {{ result.alpha_z }}

            </h2>

        </div>

        <div
            class="bg-slate-50 rounded-xl p-5 text-center"
        >

            <p class="text-slate-500">

                Σα

            </p>

            <h2 class="text-3xl font-bold mt-2">

                {{ result.alpha }}

            </h2>

        </div>

        <div
            class="bg-green-50 rounded-xl p-5 text-center border border-green-200"
        >

            <p class="text-green-700">

                Hasil Defuzzifikasi

            </p>

            <h2 class="text-4xl font-bold mt-2 text-green-700">

                {{ result.hasil }}

            </h2>

            <p class="mt-2">

                kg/pohon

            </p>

        </div>

    </div>

    <div
        class="mt-8 bg-blue-50 border border-blue-200 rounded-xl p-5"
    >

        <h3 class="font-semibold mb-3">

            Rumus

        </h3>

        <p>

            z =

            <strong>

                Σ(α × z) / Σα

            </strong>

        </p>

        <p class="mt-2">

            =

            <strong>

                {{ result.alpha_z }}

                /

                {{ result.alpha }}

            </strong>

        </p>

        <p class="mt-2 text-xl font-bold">

            = {{ result.hasil }}

        </p>

    </div>

</BaseCard>

</template>
