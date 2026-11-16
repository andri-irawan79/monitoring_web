<script setup>
import { computed } from "vue";

const props = defineProps({
  title: String,
  value: [String, Number],
  unit: String,
  icon: Object,
  status: { type: String, default: "Data simulasi" },
  color: { type: String, default: "emerald" }
});

const palettes = {
  emerald: { icon: "bg-emerald-50 text-emerald-700", dot: "bg-emerald-500", wash: "bg-emerald-100/50", line: "bg-emerald-500" },
  blue: { icon: "bg-blue-50 text-blue-700", dot: "bg-blue-500", wash: "bg-blue-100/50", line: "bg-blue-500" },
  amber: { icon: "bg-amber-50 text-amber-700", dot: "bg-amber-500", wash: "bg-amber-100/50", line: "bg-amber-500" },
  violet: { icon: "bg-violet-50 text-violet-700", dot: "bg-violet-500", wash: "bg-violet-100/50", line: "bg-violet-500" },
  orange: { icon: "bg-orange-50 text-orange-700", dot: "bg-orange-500", wash: "bg-orange-100/50", line: "bg-orange-500" },
  cyan: { icon: "bg-cyan-50 text-cyan-700", dot: "bg-cyan-500", wash: "bg-cyan-100/50", line: "bg-cyan-500" },
  sky: { icon: "bg-sky-50 text-sky-700", dot: "bg-sky-500", wash: "bg-sky-100/50", line: "bg-sky-500" },
  slate: { icon: "bg-slate-100 text-slate-600", dot: "bg-slate-400", wash: "bg-slate-100/70", line: "bg-slate-400" }
};
const palette = computed(() => palettes[props.color] || palettes.emerald);
</script>

<template>
  <article class="metric-card group relative h-full overflow-hidden rounded-2xl border border-slate-200/80 bg-white p-4 shadow-[0_3px_14px_-10px_rgba(15,23,42,.24)] transition-all duration-200 hover:-translate-y-1 hover:border-slate-300 hover:shadow-lg sm:p-5">
    <div class="pointer-events-none absolute -right-8 -top-8 h-28 w-28 rounded-full blur-2xl transition-opacity group-hover:opacity-90" :class="palette.wash"></div>
    <div class="relative flex items-start justify-between gap-3">
      <div class="min-w-0">
        <p class="text-sm font-semibold text-slate-500">{{ title }}</p>
        <p class="mt-3 break-words text-[1.8rem] font-bold leading-none tracking-tight text-slate-900 tabular-nums sm:text-3xl">{{ value ?? "-" }}</p>
        <p v-if="unit" class="mt-2 text-xs font-medium text-slate-400">{{ unit }}</p>
      </div>
      <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl transition-transform duration-200 group-hover:scale-105" :class="palette.icon">
        <component :is="icon" class="h-5 w-5" />
      </div>
    </div>
    <div class="relative mt-5 flex items-center justify-between border-t border-slate-100 pt-3">
      <span class="inline-flex items-center gap-2 text-[11px] font-semibold text-slate-500">
        <span class="h-1.5 w-1.5 rounded-full" :class="palette.dot"></span>{{ status }}
      </span>
      <span class="text-[10px] font-medium uppercase tracking-wider text-slate-300">Tersimpan</span>
    </div>
    <div class="absolute inset-x-0 bottom-0 h-[2px] opacity-0 transition-opacity group-hover:opacity-100" :class="palette.line"></div>
  </article>
</template>

<style scoped>
@media (prefers-reduced-motion: reduce) { .metric-card { transition:none; } .metric-card:hover { transform:none; } }
</style>