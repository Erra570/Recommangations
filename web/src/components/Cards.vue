<template>
  <a class="card" :href="item.siteUrl ?? anilistUrl" target="_blank" rel="noreferrer">
    <div class="imgWrap">
      <img
        class="cover"
        :src="item.coverImage"
        :alt="displayTitle"
        loading="lazy"
      />
      <div class="bottomOverlay">
        <div class="title" :title="displayTitle">{{ displayTitle }}</div>

        <div class="meta">
          <span v-if="item.meanScore != null" class="pill score">
            {{ Math.round(item.meanScore) }}
          </span>

          <span v-if="episodesOrChapters != null" class="pill count">
            {{ episodesOrChapters }}
          </span>
        </div>
      </div>
    </div>
  </a>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  item: { type: Object, required: true },
  titleMode: { type: String, default: "romaji" }, // "romaji" | "english"
});

const displayTitle = computed(() => {
  if (props.titleMode === "english") return props.item.titleEnglish || props.item.titleRomaji || "Sans titre";
  return props.item.titleRomaji || props.item.titleEnglish || "Sans titre";
});

const anilistUrl = computed(() => {
  const type = props.item.mediaType || "anime";
  return `https://anilist.co/${type}/${props.item.id}`;
});

const episodesOrChapters = computed(() => {
  return props.item.episodes ?? props.item.chapters ?? null;
});
</script>

<style scoped>
.card {
  display: block;
  text-decoration: none;
  color: inherit;
}

.imgWrap {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  aspect-ratio: 2 / 3;
  box-shadow: 0 8px 24px rgba(0,0,0,.35);
  transform: translateZ(0);
  transition: transform .15s ease, box-shadow .15s ease;
}

.card:hover .imgWrap {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0,0,0,.45);
}

.cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  filter: saturate(1.05);
}

.bottomOverlay {
  position: absolute;
  inset: auto 0 0 0;
  padding: 10px 10px 8px 10px;
  background: linear-gradient(to top, rgba(0,0,0,.85), rgba(0,0,0,.0));
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.title {
  font-size: 0.92rem;
  font-weight: 600;
  line-height: 1.1;
  color: #fff;
  text-shadow: 0 2px 8px rgba(0,0,0,.6);

  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pill {
  font-size: 0.78rem;
  font-weight: 700;
  padding: 3px 7px;
  border-radius: 8px;
  background: rgba(0,0,0,.55);
  color: #fff;
  backdrop-filter: blur(6px);
}
</style>
