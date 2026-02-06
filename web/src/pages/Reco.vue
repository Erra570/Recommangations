<template>
  <div class="container">
    <div class="top">
      <h2>Recommandations pour {{ username }}</h2>
      <button @click="reload" :disabled="loading">Rafraîchir</button>
    </div>

    <p v-if="loading">Chargement…</p>
    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="!loading && recos.length" class="grid">
      <article v-for="m in recos" :key="m.id" class="card">
        <img v-if="m.coverImage" :src="m.coverImage" :alt="m.title" />
        <h3>{{ m.title }}</h3>
        <p class="meta">
          <span v-if="m.score">Score: {{ m.score }}</span>
          <span v-if="m.genres?.length"> • {{ m.genres.join(", ") }}</span>
        </p>
        <p v-if="m.description" class="desc" v-html="m.description"></p>
        <a v-if="m.siteUrl" :href="m.siteUrl" target="_blank" rel="noreferrer">Voir sur AniList</a>
      </article>
    </div>

    <p v-if="!loading && !recos.length && !error">Aucune recommandation.</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { api } from "../api/client";

const props = defineProps({
  username: { type: String, required: true },
});

const loading = ref(false);
const error = ref("");
const recos = ref([]);

async function load() {
  loading.value = true;
  error.value = "";
  recos.value = [];
  try {
    const data = await api.getRecommendations(props.username);
    // Attends-toi idéalement à un tableau normalisé côté backend
    recos.value = Array.isArray(data) ? data : (data.items || []);
  } catch (e) {
    error.value = "Impossible de récupérer les recommandations.";
  } finally {
    loading.value = false;
  }
}

function reload() {
  load();
}

onMounted(load);
</script>

<style scoped>
.container { max-width: 1100px; margin: 30px auto; padding: 0 16px; }
.top { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; margin-top: 16px; }
.card { border: 1px solid #ddd; border-radius: 10px; padding: 12px; }
.card img { width: 100%; height: 320px; object-fit: cover; border-radius: 8px; }
.meta { font-size: 0.9rem; opacity: 0.8; }
.desc { font-size: 0.9rem; opacity: 0.9; max-height: 6.5em; overflow: hidden; }
.error { color: #c00; }
</style>
