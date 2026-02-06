import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Recommendations from "../pages/Recommendations.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: "home", component: Home },
    { path: "/reco/:username", name: "reco", component: Reco, props: true },
  ],
});

export default router;
