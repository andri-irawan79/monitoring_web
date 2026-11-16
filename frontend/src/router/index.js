import { createRouter, createWebHistory } from "vue-router";

import DashboardView from "../views/DashboardView.vue";
import RecommendationView from "../views/RecommendationView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "login",
      component: LoginView,
      meta: { guestOnly: true }
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
      meta: { guestOnly: true }
    },
    {
      path: "/",
      name: "dashboard",
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: "/recommendation",
      name: "recommendation",
      component: RecommendationView,
      meta: { requiresAuth: true }
    }
  ]
});

router.beforeEach((to) => {
  const token = sessionStorage.getItem("access_token");

  if (to.meta.requiresAuth && !token) {
    return { name: "login", query: { redirect: to.fullPath } };
  }

  if (to.meta.guestOnly && token) {
    return { name: "dashboard" };
  }

  return true;
});

export default router;
