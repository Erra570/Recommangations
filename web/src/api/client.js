const API_BASE = import.meta.env.VITE_API_BASE_URL;

async function request(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  getRecoIds(username, mediaType = "anime", limit = 12) {
    return request(`/api/user/${encodeURIComponent(username)}/recommendations/${mediaType}?limit=${limit}`);
  },

  getShortById(mediaType, id) {
    return request(`/api/anilistContent/short/${mediaType}/${id}`);
  },
};
