<template>
  <div class="container">
    <div class="top">
      <h2>Recommandations ({{ mediaType }}) pour {{ username }}</h2>

      <div class="controls">
        <select v-model="mediaType" @change="loadAll" :disabled="loading">
          <option value="anime">anime</option>
          <option value="manga">manga</option>
        </select>

        <button @click="loadAll" :disabled="loading">Rafraîchir</button>
      </div>
    </div>

    <p v-if="loading">Chargement…</p>
    <p v-if="error" class="error">{{ error }}</p>


    <div v-if="!loading && items.length" class="grid">
      <MediaCard
        v-for="it in items"
        :key="it.id"
        :item="it"
        :titleMode="titleMode"
      />
    </div>

    <p v-if="!loading && !items.length && !error">Aucune recommandation.</p>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import MediaCard from "../components/Cards.vue";
import { api } from "../api/client";

const props = defineProps({
  username: { type: String, required: true },
});

const username = props.username;

const mediaType = ref("anime");
const titleMode = ref("romaji"); // "romaji" | "english"
const loading = ref(false);
const error = ref("");

const ids = ref([]);
const items = ref([]);
const recoPayload = ref(null);
const firstRawShort = ref(null);
const failedShorts = ref([]);

const apiBase = computed(() => import.meta.env.VITE_API_BASE_URL || "(vide)");


function normalizeShort(raw, mType, fallbackId) {
  if (!raw) return null;

  const id = raw.id ?? fallbackId;
  if (!id) return null;

  const titleRomaji = raw.title_romaji ?? raw.title ?? null;
  const titleEnglish = raw.title_english ?? raw.title ?? null;

  const coverImage = raw.cover_image ?? null;

  return {
    id,
    mediaType: mType,

    titleRomaji,
    titleEnglish,
    coverImage,

    siteUrl: `https://anilist.co/${mType}/${id}`,

    meanScore: raw.mean_score ?? null,
    episodes: raw.episodes ?? null,
  };
}

async function loadAll() {
  loading.value = true;
  error.value = "";
  ids.value = [];
  items.value = [];
  recoPayload.value = null;
  firstRawShort.value = null;
  failedShorts.value = [];

  try {

    const reco = await api.getRecoIds(username, mediaType.value, 12);
    recoPayload.value = reco;

    const list = Array.isArray(reco?.ids) ? reco.ids : [];
    ids.value = list;

    if (!list.length) {
      items.value = [];
      return;
    }


    const results = await Promise.all(
      list.map(async (id) => {
        try {
          const raw = await api.getShortById(mediaType.value, id);
          return { id, raw };
        } catch (e) {
          failedShorts.value.push({ id, error: e?.message || String(e) });
          return { id, raw: null };
        }
      })
    );

    const ok = results.filter((r) => r.raw);

    if (ok.length) {
      firstRawShort.value = ok[0].raw;
    }

    items.value = ok
      .map((r) => normalizeShort(r.raw, mediaType.value, r.id))
      .filter(Boolean);

  } catch (e) {
    console.error(e);
    error.value =
      `Impossible de charger les recommandations: ${e?.message || "erreur inconnue"}`;
  } finally {
    loading.value = false;
  }
}

onMounted(loadAll);
</script>

<style scoped>
.container { max-width: 1100px; margin: 30px auto; padding: 0 16px; }
.top { display:flex; align-items:center; justify-content:space-between; gap: 12px; flex-wrap: wrap; }
.controls { display:flex; gap: 10px; align-items:center; flex-wrap: wrap; }
.toggle { opacity: .95; }
.error { color: #c00; }

.grid {
  margin-top: 18px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;
}

</style>
