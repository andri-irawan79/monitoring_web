<script setup>
import { ref, onMounted } from "vue";
import { CheckCircle2, CircleAlert, LoaderCircle, X } from "lucide-vue-next";

import RecommendationHeader from "../components/recommendation/RecommendationHeader.vue";
import MonitoringSummary from "../components/recommendation/MonitoringSummary.vue";
import RecommendationForm from "../components/recommendation/RecommendationForm.vue";
import RecommendationResultCard from "../components/recommendation/RecommendationResultCard.vue";
import RecommendationHistoryTable from "../components/recommendation/RecommendationHistoryTable.vue";
import FuzzyResultCard from "../components/recommendation/FuzzyResultCard.vue";
import RuleDominantCard from "../components/recommendation/RuleDominantCard.vue";
import ActiveRulesTable from "../components/recommendation/ActiveRulesTable.vue";
import DefuzzificationCard from "../components/recommendation/DefuzzificationCard.vue";
import RecommendationExplanationCard from "../components/recommendation/RecommendationExplanationCard.vue";

import { getLatestMonitoring } from "../services/monitoringService";
import { getFase } from "../services/masterService";
import {
    generateRecommendation,
    getLatestRecommendation,
    getRecommendationHistory
} from "../services/recommendationService";

const monitoring = ref(null);
const fases = ref([]);
const recommendation = ref(null);
const history = ref([]);
const selectedFase = ref(1);
const loading = ref(false);
const successMessage = ref("");
const errorMessage = ref("");
const fuzzyValues = ref(null);
const bestRule = ref(null);
const activeRules = ref([]);
const defuzzification = ref({});

const loadData = async () => {
    try {
        const [latestMonitoring, availablePhases, latestRecommendation, recommendationHistory] =
            await Promise.all([
                getLatestMonitoring(),
                getFase(),
                getLatestRecommendation(),
                getRecommendationHistory()
            ]);

        monitoring.value = latestMonitoring;
        fases.value = availablePhases;
        recommendation.value = latestRecommendation;
        history.value = recommendationHistory;
    } catch (error) {
        console.error("Gagal memuat halaman rekomendasi:", error);
        errorMessage.value =
            error.response?.data?.detail ||
            "Data halaman rekomendasi belum dapat dimuat. Periksa koneksi, lalu coba kembali.";
    }
};

const generate = async () => {
    if (loading.value) return;

    successMessage.value = "";
    errorMessage.value = "";

    if (!monitoring.value?.id) {
        errorMessage.value =
            "Data monitoring belum tersedia. Pastikan data simulasi sudah dikirim sebelum membuat rekomendasi.";
        return;
    }

    const startedAt = Date.now();
    loading.value = true;

    try {
        const response = await generateRecommendation(
            monitoring.value.id,
            selectedFase.value
        );

        fuzzyValues.value = response.fuzzy_values;
        bestRule.value = response.best_rule;
        activeRules.value = response.active_rules;
        defuzzification.value = response.defuzzification;

        const [latestRecommendation, recommendationHistory] = await Promise.all([
            getLatestRecommendation(),
            getRecommendationHistory()
        ]);

        recommendation.value = latestRecommendation;
        history.value = recommendationHistory;

        successMessage.value =
            "Rekomendasi berhasil dibuat dan disimpan ke riwayat.";
    } catch (error) {
        console.error("Gagal membuat rekomendasi:", error);
        errorMessage.value =
            error.response?.data?.detail ||
            "Rekomendasi belum berhasil dibuat. Periksa data monitoring dan koneksi, lalu coba kembali.";
    } finally {
        // Durasi minimum menjaga agar animasi proses terasa, bukan berkedip.
        const remaining = 1200 - (Date.now() - startedAt);
        if (remaining > 0) {
            await new Promise((resolve) => setTimeout(resolve, remaining));
        }
        loading.value = false;
    }
};

onMounted(loadData);
</script>

<template>
    <div>
        <RecommendationHeader />

        <Transition name="recommendation-message">
            <div
                v-if="successMessage"
                class="
                    mb-5
                    flex
                    items-start
                    gap-3
                    rounded-xl
                    border
                    border-green-200
                    bg-green-50
                    p-4
                    text-green-800
                    shadow-sm
                "
                role="status"
                aria-live="polite"
            >
                <CheckCircle2 class="mt-0.5 h-5 w-5 shrink-0 text-green-600" />
                <div class="min-w-0 flex-1">
                    <p class="text-sm font-semibold">Rekomendasi berhasil dibuat!</p>
                    <p class="mt-1 text-sm leading-relaxed text-green-700">
                        {{ successMessage }}
                    </p>
                </div>
                <button
                    type="button"
                    class="rounded-lg p-1 text-green-700 transition hover:bg-green-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-green-500"
                    aria-label="Tutup pesan keberhasilan"
                    @click="successMessage = ''"
                >
                    <X class="h-4 w-4" />
                </button>
            </div>
        </Transition>

        <Transition name="recommendation-message">
            <div
                v-if="errorMessage"
                class="
                    mb-5
                    flex
                    items-start
                    gap-3
                    rounded-xl
                    border
                    border-rose-200
                    bg-rose-50
                    p-4
                    text-rose-800
                    shadow-sm
                "
                role="alert"
                aria-live="assertive"
            >
                <CircleAlert class="mt-0.5 h-5 w-5 shrink-0 text-rose-600" />
                <p class="min-w-0 flex-1 text-sm leading-relaxed">
                    {{ errorMessage }}
                </p>
                <button
                    type="button"
                    class="rounded-lg p-1 text-rose-700 transition hover:bg-rose-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-500"
                    aria-label="Tutup pesan kesalahan"
                    @click="errorMessage = ''"
                >
                    <X class="h-4 w-4" />
                </button>
            </div>
        </Transition>

        <MonitoringSummary :monitoring="monitoring" />

        <div class="mt-6 grid grid-cols-1 gap-4 xl:mt-8 xl:grid-cols-2">
            <div class="min-w-0">
                <RecommendationForm
                    :fases="fases"
                    v-model:selectedFase="selectedFase"
                    :loading="loading"
                    @generate="generate"
                />
            </div>

            <div class="relative min-w-0">
                <RecommendationResultCard :recommendation="recommendation" />

                <Transition name="processing-panel">
                    <div
                        v-if="loading"
                        class="
                            absolute
                            inset-0
                            z-10
                            flex
                            items-center
                            justify-center
                            rounded-2xl
                            border
                            border-green-100
                            bg-white/95
                            px-5
                            py-8
                            text-center
                            shadow-sm
                            backdrop-blur-sm
                        "
                        role="status"
                        aria-live="polite"
                        aria-label="Sedang menghitung rekomendasi"
                    >
                        <div class="w-full max-w-sm">
                            <div class="relative mx-auto flex h-16 w-16 items-center justify-center">
                                <span class="absolute inset-0 rounded-full border-4 border-green-100" />
                                <span class="absolute inset-0 rounded-full border-4 border-transparent border-t-green-600 animate-spin" />
                                <LoaderCircle class="h-7 w-7 text-green-700" />
                            </div>

                            <p class="mt-5 text-xs font-semibold uppercase tracking-[0.16em] text-green-700">
                                Proses Fuzzy Tsukamoto
                            </p>
                            <h2 class="mt-2 text-lg font-bold text-slate-800">
                                Sedang menghitung rekomendasi
                            </h2>
                            <p class="mt-2 text-sm leading-6 text-slate-500">
                                Sistem sedang mengolah kondisi tanah dan fase pertumbuhan untuk menentukan rekomendasi pemupukan.
                            </p>

                            <div class="mt-5 h-1.5 overflow-hidden rounded-full bg-green-100">
                                <div class="recommendation-progress h-full rounded-full bg-green-600" />
                            </div>
                        </div>
                    </div>
                </Transition>
            </div>

            <div
                v-if="!loading && fuzzyValues && bestRule && recommendation && defuzzification"
                class="xl:col-span-2"
            >
                <RecommendationExplanationCard
                    :fuzzy="fuzzyValues"
                    :rule="bestRule"
                    :recommendation="recommendation"
                    :defuzzification="defuzzification"
                />
            </div>

            <div v-if="!loading" class="xl:col-span-2">
                <FuzzyResultCard :fuzzy="fuzzyValues" />
            </div>

            <div v-if="!loading" class="xl:col-span-2">
                <RuleDominantCard :rule="bestRule" />
            </div>

            <div v-if="!loading" class="xl:col-span-2">
                <ActiveRulesTable :rules="activeRules" />
            </div>

            <div v-if="!loading" class="xl:col-span-2">
                <DefuzzificationCard :result="defuzzification" />
            </div>

            <div v-if="!loading" class="xl:col-span-2">
                <RecommendationHistoryTable :recommendations="history" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.recommendation-message-enter-active,
.recommendation-message-leave-active,
.processing-panel-enter-active,
.processing-panel-leave-active {
    transition: opacity 200ms ease, transform 200ms ease;
}

.recommendation-message-enter-from,
.recommendation-message-leave-to,
.processing-panel-enter-from,
.processing-panel-leave-to {
    opacity: 0;
    transform: translateY(6px);
}

.recommendation-progress {
    width: 38%;
    animation: recommendation-progress 1.15s ease-in-out infinite;
}

@keyframes recommendation-progress {
    0% {
        transform: translateX(-110%);
    }
    100% {
        transform: translateX(270%);
    }
}

@media (prefers-reduced-motion: reduce) {
    .recommendation-message-enter-active,
    .recommendation-message-leave-active,
    .processing-panel-enter-active,
    .processing-panel-leave-active {
        transition: none;
    }

    .recommendation-progress {
        animation-duration: 2.5s;
    }
}
</style>
