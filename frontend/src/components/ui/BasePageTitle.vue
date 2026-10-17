<script setup>

defineProps({

    title:String,

    subtitle:String

})

</script>

<template>

<div class="mb-8">

    <h1
        class="
            text-5xl
            font-bold
            text-slate-800
        "
    >

        {{ title }}

    </h1>

    <p
        class="
            mt-2
            text-slate-500
            text-lg
        "
    >

        {{ subtitle }}

    </p>

</div>

</template>
