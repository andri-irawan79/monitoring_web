<script setup>
import BaseCard from "../ui/BaseCard.vue";

defineProps({
    rule: {
        type: Object,
        default: null
    }
});
</script>

<template>

<BaseCard>

    <h2
        class="text-2xl font-bold mb-6"
    >
        Rule Dominan
    </h2>

    <div
        v-if="rule"
    >

        <div
            class="
                mb-5
                bg-green-50
                border
                border-green-200
                rounded-xl
                p-4
            "
        >

            <h3
                class="font-semibold text-lg"
            >
                Rule R{{ rule.rule_id }}
            </h3>

            <p class="text-slate-500 mt-1">

                Fase :

                {{ rule.fase }}

            </p>

        </div>

        <div class="mb-6">

            <h4 class="font-semibold mb-3">

                IF

            </h4>

            <div
                class="space-y-2"
            >

                <div

                    v-for="condition in rule.conditions"

                    :key="condition[0]"

                    class="flex gap-3"

                >

                    <span
                        class="
                            font-semibold
                            w-12
                        "
                    >

                        {{ condition[0] }}

                    </span>

                    <span>

                        =

                    </span>

                    <span>

                        {{ condition[1] }}

                    </span>

                </div>

            </div>

        </div>

        <div
            class="
                border-t
                pt-5
                space-y-2
            "
        >

            <p>

                <strong>THEN</strong>

            </p>

            <p>

                Pupuk :

                <strong>

                    {{ rule.pupuk }}

                </strong>

            </p>

            <p>

                Kategori :

                <strong>

                    {{ rule.output }}

                </strong>

            </p>

            <p>

                α :

                <strong>

                    {{ rule.alpha }}

                </strong>

            </p>

            <p>

                z :

                <strong>

                    {{ rule.z }}

                </strong>

            </p>

        </div>

    </div>

    <div
        v-else
        class="text-slate-400"
    >

        Belum ada rule yang dipilih

    </div>

</BaseCard>

</template>
