<script setup>
defineProps({

    title: String,

    value: [String, Number],

    unit: String,

    icon: Object,

    status: {

        type: String,

        default: "Realtime"

    },

    color: {

        type: String,

        default: "green"

    }

});
</script>

<template>

<div
    class="
        group
        relative
        overflow-hidden
        w-full
        rounded-3xl
        bg-gradient-to-br
        from-white
        to-green-50
        border
        border-slate-200
        shadow-md
        hover:shadow-2xl
        hover:border-green-300
        hover:-translate-y-1
        transition-all
        duration-300
        p-6
        h-full
    "
>

<div
    class="
        absolute
        -top-10
        -right-10
        w-32
        h-32
        bg-green-100/40
        rounded-full
        blur-3xl
    "
></div>

    <div class="flex justify-between">

        <div>

            <p class="text-slate-500">

                {{ title }}

            </p>

            <h2 class="text-3xl font-bold mt-3">

                {{ value }}

            </h2>

            <p
                v-if="unit"
                class="text-slate-400 mt-1"
            >

                {{ unit }}

            </p>

            <div class="mt-4">
              <span
                  class="
                      inline-flex
                      items-center
                      gap-2
                      px-3
                      py-1.5
                      rounded-full
                      bg-green-100
                      text-green-700
                      text-xs
                      font-semibold
                  "
              >

                  <span class="w-2 h-2 rounded-full bg-green-500"></span>

                  Realtime

              </span>

          </div>

        </div>

        <div
             class="
                w-16
                h-16
                rounded-2xl
                bg-green-100
                flex
                items-center
                justify-center
                group-hover:scale-110
                transition-all
                duration-300
            "
        >

            <component
                :is="icon"
                class="w-7 h-7 text-green-700"
            />

        </div>

    </div>
    <div
        class="
            mt-4
            pt-3
            border-t
            border-slate-100
            flex
            justify-end
        "
      >

          <span
              class="
                  text-xs
                  font-medium
                  text-green-600
              "
          >

              Simulator Online

          </span>

      </div>

</div>
</template>
