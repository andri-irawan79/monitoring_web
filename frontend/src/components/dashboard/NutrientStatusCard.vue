<script setup>
// import { computed } from "vue";
import BaseCard from "../ui/BaseCard.vue";

defineProps({
  monitoring: {
    type: Object,
    default: null
  }
});

function getStatus(type, value) {
  switch (type) {

    case "nitrogen":
      if (value < 40)
        return { text: "Rendah", color: "bg-red-100 text-red-700" };
      if (value <= 70)
        return { text: "Normal", color: "bg-green-100 text-green-700" };
      return { text: "Tinggi", color: "bg-yellow-100 text-yellow-700" };

    case "phosphorus":
      if (value < 30)
        return { text: "Rendah", color: "bg-red-100 text-red-700" };
      if (value <= 60)
        return { text: "Normal", color: "bg-green-100 text-green-700" };
      return { text: "Tinggi", color: "bg-yellow-100 text-yellow-700" };

    case "potassium":
      if (value < 30)
        return { text: "Rendah", color: "bg-red-100 text-red-700" };
      if (value <= 50)
        return { text: "Normal", color: "bg-green-100 text-green-700" };
      return { text: "Tinggi", color: "bg-yellow-100 text-yellow-700" };

    case "ph":
      if (value < 5.5)
        return { text: "Asam", color: "bg-red-100 text-red-700" };
      if (value <= 7)
        return { text: "Optimal", color: "bg-green-100 text-green-700" };
      return { text: "Basa", color: "bg-yellow-100 text-yellow-700" };
  }

  return {
    text: "-",
    color: "bg-slate-100 text-slate-700"
  };
}

// const overallStatus = computed(() => {

//   if (!props.monitoring)
//     return null;

//   const m = props.monitoring;

//   if (
//     m.nitrogen < 40 ||
//     m.phosphorus < 30 ||
//     m.potassium < 30 ||
//     m.ph < 5.5
//   ) {
//     return {
//       text: "Perlu Pemupukan",
//       color: "text-red-600"
//     };
//   }

//   return {
//     text: "Kondisi Nutrisi Baik",
//     color: "text-green-600"
//   };
// });
</script>

<template>

<BaseCard>

    <h2 class="text-xl font-bold mb-6">
        Status Nutrisi
    </h2>

    <div
        v-if="monitoring"
        class="space-y-4"
    >

        <div
            class="flex justify-between items-center"
        >
            <span>Nitrogen</span>

            <span
                class="px-3 py-1 rounded-full text-sm"
                :class="getStatus('nitrogen', monitoring.nitrogen).color"
            >
                {{ getStatus("nitrogen", monitoring.nitrogen).text }}
            </span>

        </div>

        <div class="flex justify-between items-center">

            <span>Fosfor</span>

            <span
                class="px-3 py-1 rounded-full text-sm"
                :class="getStatus('phosphorus', monitoring.phosphorus).color"
            >
                {{ getStatus("phosphorus", monitoring.phosphorus).text }}
            </span>

        </div>

        <div class="flex justify-between items-center">

            <span>Kalium</span>

            <span
                class="px-3 py-1 rounded-full text-sm"
                :class="getStatus('potassium', monitoring.potassium).color"
            >
                {{ getStatus("potassium", monitoring.potassium).text }}
            </span>

        </div>

        <div class="flex justify-between items-center">

            <span>pH</span>

            <span
                class="px-3 py-1 rounded-full text-sm"
                :class="getStatus('ph', monitoring.ph).color"
            >
                {{ getStatus("ph", monitoring.ph).text }}
            </span>

        </div>

        <!-- <hr class="my-5"> -->

        <!-- <div>

            <p class="text-slate-500 text-sm">
                Kesimpulan
            </p>

            <h3
                class="font-semibold text-lg mt-2"
                :class="overallStatus.color"
            >
                {{ overallStatus.text }}
            </h3>

        </div> -->

    </div>

</BaseCard>

</template>
