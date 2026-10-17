<script setup>

defineProps({

    varietas:Array,

    fases:Array,

    selectedVarietas:Number,

    selectedFase:Number,

    loading:Boolean

})

const emit = defineEmits([

"generate",

"update:selectedVarietas",

"update:selectedFase"

])

</script>

<template>

<div
class="
h-[350px]
bg-white
rounded-xl
shadow-sm
p-6
mb-4
">

<div class="grid gap-6">

<div>

<label>

Varietas

</label>

<select

class="w-full mt-2 border rounded-lg p-3"

:value="selectedVarietas"

@change="emit('update:selectedVarietas', Number($event.target.value))"

>

<option

v-for="v in varietas"

:key="v.id"

:value="v.id"

>

{{ v.nama }}

</option>

</select>

</div>

<div>

<label>

Fase Pertumbuhan

</label>

<select

class="w-full mt-2 border rounded-lg p-3"

:value="selectedFase"

@change="emit('update:selectedFase', Number($event.target.value))"

>

<option

v-for="f in fases"

:key="f.id"

:value="f.id"

>

{{ f.nama }}

</option>

</select>

</div>

</div>

<div class="mt-6">

<button

@click="emit('generate')"

class="
bg-green-600
text-white
rounded-xl
px-8
py-3
hover:bg-green-700
"

>

{{ loading ? "Menghitung..." : "Hitung Rekomendasi" }}

</button>

</div>

</div>

</template>
