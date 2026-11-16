<script setup>
import { ref, onMounted, onUnmounted, nextTick } from "vue";
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
    getRecommendationHistory,
    deleteRecommendation
} from "../services/recommendationService";

const monitoring = ref(null);
const fases = ref([]);
const recommendation = ref(null);
const history = ref([]);
const selectedFase = ref(1);
const loading = ref(false);
const pageLoading = ref(true);
const successMessage = ref("");
const successTitle = ref("Rekomendasi berhasil dibuat!");
const successTimer = ref(null);
const showDeleteConfirm = ref(false);
const showDeleteSuccessDialog = ref(false);
const selectedDeleteItem = ref(null);
const cancelDeleteButton = ref(null);
const errorTitle = ref("");
const errorMessage = ref("");
const historyWarning = ref("");
const deletingId = ref(null);
const fuzzyValues = ref(null);
const bestRule = ref(null);
const activeRules = ref([]);
const defuzzification = ref({});
const hasGeneratedAnalysis = ref(false);

const loadData = async () => {
    pageLoading.value = true;
    errorTitle.value = "";
    errorMessage.value = "";

    const results = await Promise.allSettled([
        getLatestMonitoring(),
        getFase(),
        getRecommendationHistory()
    ]);

    const failedSources = [];

    if (results[0].status === "fulfilled") {
        monitoring.value = results[0].value || null;
    } else {
        console.error("Gagal memuat monitoring:", results[0].reason);
        failedSources.push("data monitoring");
    }

    if (results[1].status === "fulfilled") {
        fases.value = Array.isArray(results[1].value) ? results[1].value : [];
    } else {
        console.error("Gagal memuat fase pertumbuhan:", results[1].reason);
        failedSources.push("fase pertumbuhan");
    }

    // Hasil utama sengaja dikosongkan setiap kali halaman dibuka.
    // Riwayat tetap dimuat terpisah agar pengguna dapat melihat rekomendasi sebelumnya.
    recommendation.value = null;
    fuzzyValues.value = null;
    bestRule.value = null;
    activeRules.value = [];
    defuzzification.value = {};
    hasGeneratedAnalysis.value = false;

    if (results[2].status === "fulfilled") {
        history.value = Array.isArray(results[2].value) ? results[2].value : [];
    } else {
        console.error("Gagal memuat riwayat rekomendasi:", results[2].reason);
        failedSources.push("riwayat rekomendasi");
    }

    if (failedSources.length) {
        errorTitle.value = "Sebagian data halaman belum berhasil dimuat";
        errorMessage.value =
            `Data berikut belum dapat dimuat: ${failedSources.join(", ")}. Periksa koneksi ke server, lalu muat ulang halaman.`;
    }

    pageLoading.value = false;
};

const generate = async () => {
    if (loading.value) return;

    successMessage.value = "";
    errorTitle.value = "";
    errorMessage.value = "";
    historyWarning.value = "";

    // Kosongkan hasil sebelumnya agar tidak disalahartikan sebagai hasil
    // dari permintaan rekomendasi yang sedang/baru dilakukan.
    recommendation.value = null;
    fuzzyValues.value = null;
    bestRule.value = null;
    activeRules.value = [];
    defuzzification.value = {};
    hasGeneratedAnalysis.value = false;

    if (!monitoring.value?.id) {
        errorTitle.value = "Rekomendasi belum dapat dibuat";
        errorMessage.value =
            "Data monitoring belum tersedia. Kirim data simulasi terlebih dahulu, kemudian coba buat rekomendasi kembali.";
        return;
    }

    if (!selectedFase.value || !fases.value.length) {
        errorTitle.value = "Fase pertumbuhan belum dipilih";
        errorMessage.value =
            "Pilih salah satu fase pertumbuhan Durian Montong sebelum membuat rekomendasi.";
        return;
    }

    const startedAt = Date.now();
    let recommendationCreated = false;
    loading.value = true;

    try {
        const response = await generateRecommendation(
            monitoring.value.id,
            selectedFase.value
        );

        // API dapat mengembalikan HTTP 200 walaupun proses fuzzy gagal.
        // Karena itu, status bisnis dari response juga harus diperiksa.
        if (!response?.success || !response?.recommendation) {
            throw new Error(
                response?.message ||
                "Sistem tidak menghasilkan rekomendasi. Periksa data monitoring dan fase pertumbuhan."
            );
        }

        recommendation.value = response.recommendation;
        fuzzyValues.value = response.fuzzy_values || null;
        bestRule.value = response.best_rule || null;
        activeRules.value = Array.isArray(response.active_rules)
            ? response.active_rules
            : [];
        defuzzification.value = response.defuzzification || {};
        hasGeneratedAnalysis.value = true;

        recommendationCreated = true;

        // Kegagalan memuat ulang riwayat tidak boleh mengubah status
        // rekomendasi yang sudah berhasil disimpan menjadi gagal.
        try {
            const updatedHistory = await getRecommendationHistory();
            history.value = Array.isArray(updatedHistory) ? updatedHistory : [];
        } catch (refreshError) {
            console.error("Rekomendasi tersimpan, tetapi riwayat gagal diperbarui:", refreshError);
            historyWarning.value =
                "Rekomendasi sudah berhasil disimpan, tetapi riwayat belum dapat diperbarui. Muat ulang halaman untuk menyegarkan riwayat.";
        }
    } catch (error) {
        console.error("Gagal membuat rekomendasi:", error);
        errorTitle.value = "Rekomendasi gagal dibuat";
        errorMessage.value =
            error.response?.data?.detail ||
            error.response?.data?.message ||
            error.message ||
            "Terjadi kesalahan saat menghitung rekomendasi. Periksa data monitoring dan koneksi server, lalu coba kembali.";
    } finally {
        // Durasi minimum menjaga agar animasi proses terasa, bukan berkedip.
        const remaining = 1200 - (Date.now() - startedAt);
        if (remaining > 0) {
            await new Promise((resolve) => setTimeout(resolve, remaining));
        }
        loading.value = false;
    }

    // Notifikasi keberhasilan baru ditampilkan setelah animasi proses
    // benar-benar selesai dan overlay loading sudah ditutup.
    if (recommendationCreated) {
        successTitle.value = "Rekomendasi berhasil dibuat!";
        successMessage.value =
            "Rekomendasi berhasil dihitung dan disimpan. Hasil terbaru sudah ditampilkan.";
        if (successTimer.value) window.clearTimeout(successTimer.value);
        successTimer.value = window.setTimeout(() => { successMessage.value = ""; }, 4500);
    }
};


const requestDeleteRecommendation = async (item) => {
    if (!item?.id || deletingId.value !== null) return;
    selectedDeleteItem.value = item;
    showDeleteConfirm.value = true;
    await nextTick();
    cancelDeleteButton.value?.focus();
};

const closeDeleteConfirmation = () => {
    showDeleteConfirm.value = false;
    selectedDeleteItem.value = null;
};

const removeRecommendation = async () => {
    const item = selectedDeleteItem.value;
    if (!item?.id || deletingId.value !== null) return;
    showDeleteConfirm.value = false;

    deletingId.value = item.id;
    historyWarning.value = "";
    try {
        await deleteRecommendation(item.id);
        history.value = history.value.filter((row) => row.id !== item.id);

        if (recommendation.value?.id === item.id) {
            recommendation.value = null;
            fuzzyValues.value = null;
            bestRule.value = null;
            activeRules.value = [];
            defuzzification.value = {};
            hasGeneratedAnalysis.value = false;
        }

        successMessage.value = "";
        if (successTimer.value) window.clearTimeout(successTimer.value);
        showDeleteSuccessDialog.value = true;
    } catch (error) {
        console.error("Gagal menghapus rekomendasi:", error);
        errorTitle.value = "Rekomendasi gagal dihapus";
        errorMessage.value =
            error.response?.data?.detail ||
            error.response?.data?.message ||
            "Terjadi kesalahan saat menghapus rekomendasi. Silakan coba kembali.";
    } finally {
        deletingId.value = null;
        selectedDeleteItem.value = null;
    }
};

onMounted(async () => {\n    await loadData();\n    if (window.location.hash) {\n        await nextTick();\n        window.setTimeout(() => document.querySelector(window.location.hash)?.scrollIntoView({ behavior: "smooth", block: "start" }), 120);\n    }\n});
onUnmounted(() => {
    if (successTimer.value) window.clearTimeout(successTimer.value);
});
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
                    relative
                    overflow-hidden
                "
                role="status"
                aria-live="polite"
            >
                <CheckCircle2 class="mt-0.5 h-5 w-5 shrink-0 text-green-600" />
                <div class="min-w-0 flex-1">
                    <p class="text-sm font-semibold">{{ successTitle }}</p>
                    <p class="mt-1 text-sm leading-relaxed text-green-700">
                        {{ successMessage }}
                    </p>
                </div>
                <button
                    type="button"
                    class="rounded-lg p-1 text-green-700 transition hover:bg-green-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-green-500"
                    aria-label="Tutup pesan keberhasilan"
                    @click="successMessage = ''; if (successTimer) window.clearTimeout(successTimer)"
                >
                    <X class="h-4 w-4" />
                </button>
                <div class="success-toast-progress absolute inset-x-0 bottom-0 h-1 bg-green-200">
                    <div class="h-full w-full origin-left bg-green-600" />
                </div>
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
                <div class="min-w-0 flex-1">
                    <p class="text-sm font-semibold">{{ errorTitle || "Terjadi kesalahan" }}</p>
                    <p class="mt-1 text-sm leading-relaxed text-rose-700">
                        {{ errorMessage }}
                    </p>
                </div>
                <button
                    type="button"
                    class="rounded-lg p-1 text-rose-700 transition hover:bg-rose-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-500"
                    aria-label="Tutup pesan kesalahan"
                    @click="errorMessage = ''; errorTitle = ''"
                >
                    <X class="h-4 w-4" />
                </button>
            </div>
        </Transition>

        <Transition name="recommendation-message">
            <div
                v-if="historyWarning"
                class="mb-5 flex items-start gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-amber-800"
                role="status"
                aria-live="polite"
            >
                <CircleAlert class="mt-0.5 h-5 w-5 shrink-0 text-amber-600" />
                <p class="min-w-0 flex-1 text-sm leading-relaxed">{{ historyWarning }}</p>
                <button
                    type="button"
                    class="rounded-lg p-1 text-amber-700 transition hover:bg-amber-100"
                    aria-label="Tutup pemberitahuan riwayat"
                    @click="historyWarning = ''"
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
                    :initial-loading="pageLoading"
                    @generate="generate"
                />
            </div>

            <div class="relative min-w-0">
                <RecommendationResultCard
                    :recommendation="recommendation"
                    :initial-loading="pageLoading"
                />

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
                v-if="!loading && hasGeneratedAnalysis"
                class="xl:col-span-2"
            >
                <RecommendationExplanationCard
                    :fuzzy="fuzzyValues"
                    :rule="bestRule"
                    :recommendation="recommendation"
                    :defuzzification="defuzzification"
                />
            </div>

            <div v-if="!loading && hasGeneratedAnalysis" class="xl:col-span-2">
                <FuzzyResultCard :fuzzy="fuzzyValues" />
            </div>

            <div v-if="!loading && hasGeneratedAnalysis" class="xl:col-span-2">
                <RuleDominantCard :rule="bestRule" />
            </div>

            <div v-if="!loading && hasGeneratedAnalysis" class="xl:col-span-2">
                <ActiveRulesTable :rules="activeRules" />
            </div>

            <div v-if="!loading && hasGeneratedAnalysis" class="xl:col-span-2">
                <DefuzzificationCard :result="defuzzification" />
            </div>

            <div v-if="!loading" class="xl:col-span-2">
                <RecommendationHistoryTable :recommendations="history" :deleting-id="deletingId" @delete="requestDeleteRecommendation" />
            </div>
        </div>
    </div>

    <Teleport to="body">
        <div v-if="showDeleteConfirm" class="fixed inset-0 z-[100] flex items-center justify-center bg-slate-900/40 px-4 backdrop-blur-[2px]" role="presentation" @click.self="closeDeleteConfirmation" @keydown.esc.stop.prevent="closeDeleteConfirmation">
            <section class="w-full max-w-sm rounded-2xl bg-white p-6 shadow-2xl ring-1 ring-slate-900/5" role="dialog" aria-modal="true" aria-labelledby="delete-dialog-title" aria-describedby="delete-dialog-description" @click.stop>
                <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-rose-50 text-rose-600"><CircleAlert class="h-6 w-6" /></div>
                <div class="mt-4 text-center">
                    <h2 id="delete-dialog-title" class="text-lg font-semibold text-slate-800">Konfirmasi Hapus</h2>
                    <p id="delete-dialog-description" class="mt-2 text-sm leading-6 text-slate-500">Apakah Anda yakin ingin menghapus rekomendasi untuk fase <strong>{{ selectedDeleteItem?.fase || "-" }}</strong> dengan pupuk <strong>{{ selectedDeleteItem?.jenis_pupuk || "-" }}</strong>? Data yang dihapus tidak dapat dikembalikan.</p>
                </div>
                <div class="mt-6 flex items-center justify-end gap-3">
                    <button ref="cancelDeleteButton" type="button" @click="closeDeleteConfirmation" class="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-300 focus-visible:ring-offset-2">Batal</button>
                    <button type="button" @click="removeRecommendation" class="rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-rose-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-300 focus-visible:ring-offset-2">Hapus</button>
                </div>
            </section>
        </div>
    </Teleport>

    <Teleport to="body">
        <div
            v-if="showDeleteSuccessDialog"
            class="fixed inset-0 z-[110] flex items-center justify-center bg-slate-900/40 px-4 backdrop-blur-[2px]"
            role="presentation"
        >
            <section
                class="w-full max-w-sm rounded-2xl bg-white p-6 shadow-2xl ring-1 ring-slate-900/5"
                role="dialog"
                aria-modal="true"
                aria-labelledby="delete-success-title"
                aria-describedby="delete-success-description"
            >
                <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-50 text-green-600">
                    <CheckCircle2 class="h-6 w-6" />
                </div>
                <div class="mt-4 text-center">
                    <h2 id="delete-success-title" class="text-lg font-semibold text-slate-800">
                        Data berhasil dihapus
                    </h2>
                    <p id="delete-success-description" class="mt-2 text-sm leading-6 text-slate-500">
                        Data riwayat rekomendasi telah berhasil dihapus dari sistem.
                    </p>
                </div>
                <div class="mt-6 flex justify-center">
                    <button
                        type="button"
                        autofocus
                        @click="showDeleteSuccessDialog = false"
                        class="min-w-24 rounded-xl bg-green-600 px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-green-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-green-300 focus-visible:ring-offset-2"
                    >
                        OK
                    </button>
                </div>
            </section>
        </div>
    </Teleport>
</template>

<style scoped>
.recommendation-message-enter-active,
.recommendation-message-leave-active,
.processing-panel-enter-active,
.processing-panel-leave-active {
    transition: opacity 260ms ease, transform 260ms ease;
}

.recommendation-message-enter-from,
.recommendation-message-leave-to {
    opacity: 0;
    transform: translateX(28px);
}

.processing-panel-enter-from,
.processing-panel-leave-to {
    opacity: 0;
    transform: translateY(6px);
}

.success-toast-progress > div {
    animation: success-toast-countdown 4.5s linear forwards;
}

@keyframes success-toast-countdown {
    from { transform: scaleX(1); }
    to { transform: scaleX(0); }
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

    .recommendation-message-enter-from,
    .recommendation-message-leave-to,
    .processing-panel-enter-from,
    .processing-panel-leave-to {
        transform: none;
    }

    .recommendation-progress {
        animation-duration: 2.5s;
    }
}
@media (prefers-reduced-motion: reduce) { .recommendation-page { scroll-behavior: auto; } }\n</style>
