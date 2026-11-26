<script setup>
import BaseCard from "../ui/BaseCard.vue";
defineProps({ rules: { type: Array, default: () => [] } });
function fmt(value) {
  const number = Number(value);
  return Number.isFinite(number) ? number.toFixed(4) : "-";
}
</script>

<template>
  <BaseCard>
    <div class="mb-5">
      <h2 class="text-lg font-extrabold text-slate-900">Aturan yang Aktif</h2>
      <p class="mt-1 text-sm text-slate-500">Aturan FIS-1 dan FIS-2 dengan derajat aktivasi lebih besar dari nol.</p>
    </div>
    <div v-if="rules.length" class="overflow-x-auto">
      <table class="w-full min-w-[640px] text-sm">
        <thead class="border-b border-slate-200 bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
          <tr>
            <th class="px-3 py-3">Kode aturan</th>
            <th class="px-3 py-3">Variabel</th>
            <th class="px-3 py-3">Kondisi</th>
            <th class="px-3 py-3 text-right">α</th>
            <th class="px-3 py-3">Konsekuen</th>
            <th class="px-3 py-3 text-right">z</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="rule in rules" :key="rule.rule_id">
            <td class="px-3 py-3 font-bold text-slate-700">{{ rule.rule_id }}</td>
            <td class="px-3 py-3">{{ rule.variable }}</td>
            <td class="px-3 py-3">{{ rule.condition }}</td>
            <td class="px-3 py-3 text-right tabular-nums">{{ fmt(rule.alpha) }}</td>
            <td class="px-3 py-3 capitalize">{{ rule.consequent }}</td>
            <td class="px-3 py-3 text-right tabular-nums">{{ fmt(rule.z) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else class="py-6 text-center text-sm text-slate-400">Tidak ada aturan aktif.</p>
  </BaseCard>
</template>
