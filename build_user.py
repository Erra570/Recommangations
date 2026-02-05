import json
import time
import requests
import os

ANILIST_URL = "https://graphql.anilist.co"

Q_MEDIA_BY_IDS = """
query ($type: MediaType, $ids: [Int]) {
  Page(perPage: 50) {
    media(type: $type, id_in: $ids) {
      id
      format
      genres
      meanScore
      favourites
      isAdult
      countryOfOrigin
      episodes
      chapters
      tags { id rank }
      title { romaji english }
    }
  }
}
"""

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def post(query, variables):
    r = requests.post(ANILIST_URL, json={"query": query, "variables": variables}, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise RuntimeError(data["errors"][0].get("message", "AniList error"))
    return data["data"]

def chunks(lst, n=50):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def build_catalog(user_json_path, media_type, out_path):
    user_entries = read_json(user_json_path)
    ids = sorted({e["id"] for e in user_entries if isinstance(e.get("id"), int)})

    catalog = []
    for batch in chunks(ids, 50):
        data = post(Q_MEDIA_BY_IDS, {"type": media_type, "ids": batch})
        catalog.extend(data["Page"]["media"])
        time.sleep(0.8)  # petite pause anti rate-limit

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print("saved", out_path, "items", len(catalog))

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    build_catalog("data/userAnime.json", "ANIME", "data/userAnimeCatalog.json")
    build_catalog("data/userManga.json", "MANGA", "data/userMangaCatalog.json")

