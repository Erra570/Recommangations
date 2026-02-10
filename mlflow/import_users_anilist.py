import os
import time
import argparse
import requests
from sqlalchemy import create_engine, text

# =========================
# CONFIG
# =========================
ANILIST_URL = "https://graphql.anilist.co"

QUERY_USERID = """
query ($userName: String) {
  User(name: $userName) {
    id
    name
  }
}
"""

QUERY_LIST = """
query ($userId: Int, $type: MediaType) {
  MediaListCollection(userId: $userId, type: $type) {
    lists {
      entries {
        status
        score(format: POINT_10)
        progress
        media {
          id
        }
      }
    }
  }
}
"""


# =========================
# UTILS
# =========================
def engine_from_env():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL manquant.\n"
            "Ex: export DATABASE_URL='postgresql+psycopg://api:api@localhost:5432/db_anilist'"
        )
    return create_engine(url, pool_pre_ping=True)


def gql(query: str, variables: dict, max_retries: int = 10):
    for attempt in range(max_retries):
        r = requests.post(
            ANILIST_URL,
            json={"query": query, "variables": variables},
            timeout=60,
        )

        if r.status_code == 429:
            retry_after = r.headers.get("Retry-After")
            wait = int(retry_after) if retry_after and retry_after.isdigit() else (5 + 5 * attempt)
            print(f"⚠️ AniList 429 → wait {wait}s")
            time.sleep(wait)
            continue

        if r.status_code >= 400:
            print("❌ AniList HTTP ERROR", r.status_code)
            print(r.text)
            raise RuntimeError("AniList request failed")

        payload = r.json()
        if "errors" in payload:
            raise RuntimeError(payload["errors"])
        return payload["data"]

    raise RuntimeError("AniList rate limit: trop de 429, réessaie plus tard")


# =========================
# ANILIST FETCH
# =========================
def get_user(username: str):
    data = gql(QUERY_USERID, {"userName": username})
    u = data.get("User")
    if not u:
        raise RuntimeError(f"user introuvable sur AniList: {username}")
    return int(u["id"]), u["name"]


def fetch_entries(user_id: int, media_type: str):
    data = gql(QUERY_LIST, {"userId": user_id, "type": media_type})
    coll = data.get("MediaListCollection")
    if not coll:
        return []

    out = []
    for lst in (coll.get("lists") or []):
        for e in (lst.get("entries") or []):
            mid = (e.get("media") or {}).get("id")
            if not mid:
                continue
            out.append({
                "id": int(mid),
                "status": e.get("status"),
                "score": float(e.get("score") or 0.0),
                "progress": int(e.get("progress") or 0),
            })
    return out


# =========================
# DB UPSERT
# =========================
def upsert_user(conn, username: str, anilist_id: int):
    conn.execute(text("""
        INSERT INTO user (username, id)
        VALUES (:u, :aid)
        ON CONFLICT (username)
        DO UPDATE SET id = EXCLUDED.id
    """), {"u": username, "aid": anilist_id})

    uid = conn.execute(
        text("SELECT id FROM user WHERE username = :u"),
        {"u": username},
    ).scalar()

    return int(uid)


def upsert_user_media(conn, uid: int, rows: list, media_type: str):
    if media_type == "ANIME":
        table = "user_anime"
        id_col = "anime_id"
        base_table = "anime"
    else:
        table = "user_manga"
        id_col = "manga_id"
        base_table = "manga"

    # 1) récupère tous les ids existants dans le catalogue pour éviter FK violation
    media_ids = [int(r["id"]) for r in rows]
    if not media_ids:
        return {"inserted": 0, "skipped_missing": 0}

    existing = conn.execute(
        text(f"SELECT id FROM {base_table} WHERE id = ANY(:ids)"),
        {"ids": media_ids},
    ).scalars().all()
    existing_set = set(int(x) for x in existing)

    inserted = 0
    skipped = 0

    for r in rows:
        mid = int(r["id"])
        if mid not in existing_set:
            skipped += 1
            continue

        conn.execute(text(f"""
            INSERT INTO {table} (user_id, {id_col}, status, score, progress, favourite)
            VALUES (:uid, :mid, :st, :sc, :pr, false)
            ON CONFLICT (user_id, {id_col})
            DO UPDATE SET
              status   = EXCLUDED.status,
              score    = EXCLUDED.score,
              progress = EXCLUDED.progress
        """), {
            "uid": uid,
            "mid": mid,
            "st": r.get("status"),
            "sc": float(r.get("score") or 0.0),
            "pr": int(r.get("progress") or 0),
        })
        inserted += 1

    return {"inserted": inserted, "skipped_missing": skipped}



# =========================
# MAIN
# =========================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--users", nargs="+", required=True)
    parser.add_argument("--sleep", type=float, default=1.0)
    args = parser.parse_args()

    engine = engine_from_env()

    ok, failed = 0, 0

    for username in args.users:
        username = username.strip()
        if not username:
            continue

        print(f"\n🚀 import: {username}")
        time.sleep(args.sleep)
        try:
            anilist_id, canonical = get_user(username)

            anime_entries = fetch_entries(anilist_id, "ANIME")
            time.sleep(args.sleep)
            manga_entries = fetch_entries(anilist_id, "MANGA")
            time.sleep(args.sleep)

            with engine.begin() as conn:
                uid = upsert_user(conn, canonical, anilist_id)
                upsert_user_media(conn, uid, anime_entries, "ANIME")
                upsert_user_media(conn, uid, manga_entries, "MANGA")

            print(
                f"✅ done {canonical} | anime={len(anime_entries)} | manga={len(manga_entries)}"
            )
            ok += 1

        except Exception as e:
            print(f"⚠️ skipped {username} → {e}")
            failed += 1
            continue

    print("\n======================")
    print(f"IMPORT FINISHED")
    print(f"success: {ok}")
    print(f"failed : {failed}")
    print("======================")


if __name__ == "__main__":
    main()
