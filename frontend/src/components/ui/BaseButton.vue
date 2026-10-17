<script setup>

defineProps({

    variant: {

        type: String,

        default: "primary"

    }

});

</script>

<template>

<button

    :class="[

        'px-5 py-3 rounded-xl font-semibold transition-all duration-300',

        variant === 'primary'

            ? 'bg-emerald-600 hover:bg-emerald-700 text-white shadow'

            : '',

        variant === 'secondary'

            ? 'bg-slate-100 hover:bg-slate-200 text-slate-700'

            : '',

        variant === 'danger'

            ? 'bg-red-500 hover:bg-red-600 text-white'

            : ''

    ]"

>

    <slot />

</button>

</template>
