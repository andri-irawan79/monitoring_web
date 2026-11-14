<script setup>
defineProps({
    fases: {
        type: Array,
        default: () => []
    },
    selectedFase: {
        type: Number,
        required: true
    },
    loading: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits([
    "generate",
    "update:selectedFase"
]);
</script>

<template>
  <div class="h-[350px] bg-white rounded-xl shadow-sm p-6 mb-4">
    <div class="grid gap-6">
      <div>
        <label class="block text-sm font-medium">
          Objek Tanaman
        </label>
        <div
          class="w-full mt-2 border rounded-lg p-3 bg-gray-50 text-gray-700"
          aria-label="Objek tanaman tetap Durian Montong"
        >
          Durian Montong
        </div>
        <p class="mt-1 text-xs text-gray-500">
          Objek penelitian ditetapkan khusus untuk varietas Montong.
        </p>
      </div>

      <div>
        <label class="block text-sm font-medium" for="fase-pertumbuhan">
          Fase Pertumbuhan
        </label>
        <select
          id="fase-pertumbuhan"
          class="w-full mt-2 border rounded-lg p-3"
          :value="selectedFase"
          @change="emit('update:selectedFase', Number($event.target.value))"
        >
          <option
            v-for="fase in fases"
            :key="fase.id"
            :value="fase.id"
          >
            {{ fase.nama }}
          </option>
        </select>
      </div>
    </div>

    <div class="mt-6">
      <button
        type="button"
        @click="emit('generate')"
        :disabled="loading"
        class="bg-green-600 text-white rounded-xl px-8 py-3 hover:bg-green-700 disabled:opacity-60"
      >
        {{ loading ? "Menghitung..." : "Hitung Rekomendasi" }}
      </button>
    </div>
  </div>
</template>
