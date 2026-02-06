import { createRouter, createWebHashHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Reco from "../pages/Reco.vue";

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: "home", component: Home },
    { path: "/reco/:username", name: "reco", component: Reco, props: true },
  ],
});

export default router;