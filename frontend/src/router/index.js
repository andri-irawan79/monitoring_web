import { createRouter, createWebHistory } from "vue-router";

import DashboardView from "../views/DashboardView.vue";
import RecommendationView from "../views/RecommendationView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "dashboard",
      component: DashboardView,
    },
    {
      path: "/recommendation",
      name: "recommendation",
      component: RecommendationView,
    },
  ],
});

export default router;
