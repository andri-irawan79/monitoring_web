<template>
  <header class="recommendation-hero relative mb-6 overflow-hidden rounded-[1.6rem] border border-emerald-900/10 px-6 py-7 text-white shadow-[0_16px_40px_-24px_rgba(15,65,48,.55)] sm:px-8 sm:py-9">
    <div class="pointer-events-none absolute -right-12 -top-24 h-72 w-72 rounded-full bg-emerald-300/10 blur-2xl"></div>
    <div class="pointer-events-none absolute bottom-[-9rem] right-[25%] h-64 w-64 rounded-full bg-lime-200/10 blur-3xl"></div>
    <div class="relative max-w-3xl">
      <div class="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-[11px] font-bold uppercase tracking-[0.16em] text-emerald-100"><span class="h-1.5 w-1.5 rounded-full bg-lime-300"></span>Sistem Pendukung Keputusan</div>
      <h1 class="mt-5 text-2xl font-bold leading-tight tracking-tight sm:text-3xl lg:text-4xl">Rekomendasi Pemupukan</h1>
      <p class="mt-3 max-w-2xl text-sm leading-7 text-emerald-50/80 sm:text-base">Tentukan fase pertumbuhan Durian Montong untuk memperoleh rekomendasi jenis dan dosis pupuk berdasarkan metode Fuzzy Tsukamoto.</p>
      <div class="mt-5 flex flex-wrap items-center gap-2 text-xs text-emerald-100/75"><span class="rounded-full border border-white/15 bg-white/10 px-3 py-1.5">Durian Montong</span><span class="rounded-full border border-white/15 bg-white/10 px-3 py-1.5">Fuzzy Tsukamoto</span><span class="rounded-full border border-white/15 bg-white/10 px-3 py-1.5">5 fase pertumbuhan</span></div>
    </div>
  </header>
</template>

<style scoped>
.recommendation-hero { background:linear-gradient(118deg,#123d31 0%,#155342 58%,#17634c 100%); }
</style>