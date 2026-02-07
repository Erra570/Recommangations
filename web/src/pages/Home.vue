<template>
  <div class="container">
    <h1>RecoMangaTions</h1>
    <form @submit.prevent="go">
      <label>Pseudo AniList</label>
      <input v-model.trim="username" placeholder="ex: jane doe" />
      <button :disabled="!username">Voir mes recommandations</button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { api } from "../api/client";

const router = useRouter();
const username = ref("");
const error = ref("");

async function go() {
  error.value = "";
  try {
    await api.getUser(username.value);
    router.push(`/reco/${encodeURIComponent(username.value)}`);
  } catch (e) {
    error.value = "Utilisateur introuvable ou API indisponible.";
  }
}
</script>

<style scoped>
.container { max-width: 720px; margin: 40px auto; padding: 0 16px; }
input { width: 100%; padding: 10px; margin: 8px 0 12px; }
button { padding: 10px 14px; }
.error { color: #c00; }
</style>
