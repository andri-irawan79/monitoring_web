<script setup>
import { useRoute } from "vue-router";
import AppLayout from "./components/layout/AppLayout.vue";

const route = useRoute();
</script>

<template>
  <AppLayout v-if="route.meta.requiresAuth">
    <RouterView />
  </AppLayout>
  <RouterView v-else />
</template>
