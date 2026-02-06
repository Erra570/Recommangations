const API_BASE = import.meta.env.VITE_API_BASE_URL;

async function request(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API error ${res.status}: ${text || res.statusText}`);
  }
  return res.json();
}

export const api = {
  getUser: (username) => request(`/api/user/${encodeURIComponent(username)}`),
  getUserFavorites: (username) => request(`/api/user/${encodeURIComponent(username)}/favorites`),
  getUserEntries: (username, mediaType) =>
    request(`/api/user/${encodeURIComponent(username)}/entries/${encodeURIComponent(mediaType)}`),

  // Pour quand on aura un endpoint recommandation faut juste pas que j'oublie en gros
  // getRecommendations: (username) =>
  //  request(`/api/user/${encodeURIComponent(username)}/recommendations`),
};