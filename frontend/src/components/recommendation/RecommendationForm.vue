<script setup>
import { LoaderCircle } from "lucide-vue-next";

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
    <section
        class="
            min-h-[350px]
            h-auto
            rounded-2xl
            border
            border-slate-200
            bg-white
            p-5
            sm:p-6
            shadow-sm
        "
    >
        <div class="mb-6">
            <h2 class="text-lg font-semibold text-slate-800">
                Parameter Rekomendasi
            </h2>
            <p class="mt-1 text-sm text-slate-500">
                Tentukan fase pertumbuhan untuk menghitung rekomendasi pemupukan.
            </p>
        </div>

        <div class="grid grid-cols-1 gap-5">
            <div>
                <label class="block text-sm font-medium text-slate-700">
                    Objek Tanaman
                </label>
                <div
                    class="
                        mt-2
                        flex
                        min-h-11
                        w-full
                        items-center
                        rounded-xl
                        border
                        border-slate-200
                        bg-slate-50
                        px-3
                        py-2.5
                        text-sm
                        text-slate-700
                    "
                    aria-label="Objek tanaman tetap Durian Montong"
                >
                    Durian Montong
                </div>
                <p class="mt-1.5 text-xs leading-relaxed text-slate-500">
                    Objek penelitian ditetapkan khusus untuk varietas Montong.
                </p>
            </div>

            <div>
                <label
                    class="block text-sm font-medium text-slate-700"
                    for="fase-pertumbuhan"
                >
                    Fase Pertumbuhan
                </label>
                <select
                    id="fase-pertumbuhan"
                    class="
                        mt-2
                        min-h-11
                        w-full
                        rounded-xl
                        border
                        border-slate-200
                        bg-white
                        px-3
                        py-2.5
                        text-sm
                        text-slate-700
                        outline-none
                        transition
                        focus:border-green-500
                        focus:ring-2
                        focus:ring-green-100
                    "
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

        <div class="mt-6 flex justify-stretch sm:justify-end">
            <button
                type="button"
                @click="emit('generate')"
                :disabled="loading || !fases.length"
                class="
                    inline-flex
                    min-h-11
                    w-full
                    items-center
                    justify-center
                    rounded-xl
                    bg-green-700
                    px-6
                    py-3
                    text-sm
                    font-semibold
                    text-white
                    shadow-sm
                    transition-colors
                    hover:bg-green-800
                    disabled:cursor-not-allowed
                    disabled:opacity-60
                    focus-visible:outline-none
                    focus-visible:ring-2
                    focus-visible:ring-green-500
                    focus-visible:ring-offset-2
                    sm:w-auto
                "
            >
                <LoaderCircle v-if="loading" class="h-4 w-4 animate-spin" />
                {{ loading ? "Sedang Menghitung..." : "Buat Rekomendasi" }}
            </button>
        </div>
    </section>
</template>
