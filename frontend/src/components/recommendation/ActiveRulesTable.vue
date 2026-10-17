<script setup>
import BaseCard from "../ui/BaseCard.vue";

defineProps({
    rules: {
        type: Array,
        default: () => []
    }
});
</script>

<template>

<BaseCard>

    <h2 class="text-2xl font-bold mb-6">

        Rule Aktif

    </h2>

    <div
        v-if="rules.length"
        class="overflow-x-auto"
    >

        <table class="w-full text-sm">

            <thead>

                <tr class="border-b">

                    <th class="text-left py-3">Rule</th>

                    <th class="text-left py-3">Kondisi</th>

                    <th class="text-center py-3">α</th>

                    <th class="text-center py-3">z</th>

                    <th class="text-center py-3">Pupuk</th>

                    <th class="text-center py-3">Output</th>

                </tr>

            </thead>

            <tbody>

                <tr
                    v-for="rule in rules"
                    :key="rule.rule_id"
                    class="border-b hover:bg-slate-50"
                >

                    <td class="py-4">

                        R{{ rule.rule_id }}

                    </td>

                    <td>

                        <div
                            v-for="c in rule.conditions"
                            :key="c[0]"
                        >

                            {{ c[0] }} = {{ c[1] }}

                        </div>

                    </td>

                    <td class="text-center">

                        {{ rule.alpha }}

                    </td>

                    <td class="text-center">

                        {{ rule.z }}

                    </td>

                    <td class="text-center">

                        {{ rule.pupuk }}

                    </td>

                    <td class="text-center">

                        {{ rule.output }}

                    </td>

                </tr>

            </tbody>

        </table>

    </div>

    <div
        v-else
        class="text-slate-400"
    >

        Tidak ada rule aktif.

    </div>

</BaseCard>

</template>
