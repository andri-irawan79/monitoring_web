<script setup>
import { ref, onMounted } from "vue";

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

import {
    getLatestMonitoring
} from "../services/monitoringService";

import {
    getVarietas,
    getFase
} from "../services/masterService";

import {
    generateRecommendation,
    getLatestRecommendation,
    getRecommendationHistory
} from "../services/recommendationService";

const monitoring = ref(null);

const varietas = ref([]);

const fases = ref([]);

const recommendation = ref(null);

const history = ref([]);

const selectedVarietas = ref(1);

const selectedFase = ref(1);

const loading = ref(false);

const fuzzyValues = ref(null);

const bestRule = ref(null);

const activeRules = ref([]);
const defuzzification = ref({});

const loadData = async () => {

    monitoring.value =
        await getLatestMonitoring();

    varietas.value =
        await getVarietas();

    fases.value =
        await getFase();

    recommendation.value =
        await getLatestRecommendation();

    history.value =
        await getRecommendationHistory();

};

const generate = async () => {

    loading.value = true;

    try {

        const response =
            await generateRecommendation(

                monitoring.value.id,

                selectedVarietas.value,

                selectedFase.value

            );

            console.log("Response :", response);

            console.log("Fuzzy Values :", response.fuzzy_values);

            console.log("Best Rule :", response.best_rule);

            console.log("Defuzzifikasi :", response.defuzzification);

        fuzzyValues.value =
            response.fuzzy_values;

        recommendation.value =
            await getLatestRecommendation();

        history.value =
            await getRecommendationHistory();

        bestRule.value = response.best_rule;

        activeRules.value = response.active_rules;

        defuzzification.value = response.defuzzification;

    }

    finally {

        loading.value = false;

    }

};

onMounted(loadData);

</script>

<template>

<div>

    <RecommendationHeader/>

    <MonitoringSummary
        :monitoring="monitoring"
    />

    <div  class="
            grid
            grid-cols-1
            xl:grid-cols-2
            gap-4
            mt-8
        ">
        <div class="xl:col-span-1">
            <RecommendationForm

              :varietas="varietas"

              :fases="fases"

              v-model:selectedVarietas="selectedVarietas"

              v-model:selectedFase="selectedFase"

              :loading="loading"

              @generate="generate"

            />
        </div>
        <div class="xl:col-span-1">
          <RecommendationResultCard
              :recommendation="recommendation"
            />
        </div>

        <div class="xl:col-span-2">
           <RecommendationExplanationCard
              v-if="
                  fuzzyValues &&
                  bestRule &&
                  recommendation &&
                  defuzzification
              "
              :fuzzy="fuzzyValues"
              :rule="bestRule"
              :recommendation="recommendation"
              :defuzzification="defuzzification"
          />
        </div>

        <div class="xl:col-span-2">
          <FuzzyResultCard
              :fuzzy="fuzzyValues"
          />
        </div>
        <div class="xl:col-span-2">
           <RuleDominantCard
                :rule="bestRule"
            />
        </div>
        <div class="xl:col-span-2">
            <ActiveRulesTable
              :rules="activeRules"
            />
        </div>
        <div class="xl:col-span-2">
          <DefuzzificationCard
              :result="defuzzification"
          />
        </div>
        <div class="xl:col-span-2">
           <RecommendationHistoryTable
                :recommendations="history"
            />
        </div>
    </div>

</div>

</template>
