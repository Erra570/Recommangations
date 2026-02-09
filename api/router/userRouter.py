from fastapi import APIRouter
import random
import os
import numpy as np
from sqlalchemy import create_engine, text
from fastapi import HTTPException
import logging

from model_store import get as get_model_and_vec
from requestsAnilistApi.requests import fetch_user_id
from schemas.reco import RecommendationsIdsResponse, MediaType

# Prometheus metrics :
from metrics import USER_ID_REQUESTS, ANILIST_ERRORS

from requestsAnilistApi.requests import (
    fetch_user_id,
    fetch_user_favorites_list,
    fetch_user_entries_list,
)

from model_store import get as get_model_and_vec

router = APIRouter()

# fake anime ids (pour tester avant qu'on iat le ML)
FAKE_ANIME_IDS = [227, 227, 227, 227, 227, 227]
FAKE_MANGA_IDS = [31133, 31133, 31133, 31133, 31133, 31133]

# DB
DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


# SQL helpers pour la reco
SQL_SEEN_ANIME = """
SELECT anime_id AS media_id
FROM user_anime
WHERE user_id = :user_id
"""

SQL_SEEN_MANGA = """
SELECT manga_id AS media_id
FROM user_manga
WHERE user_id = :user_id
"""

SQL_CANDIDATES_ANIME = """
SELECT
  a.id AS media_id,
  a.mean_score,
  a.favourites,
  COALESCE(array_agg(ag.genre_name) FILTER (WHERE ag.genre_name IS NOT NULL), '{}') AS genres
FROM anime a
LEFT JOIN anime_genre ag ON ag.anime_id = a.id
GROUP BY a.id, a.mean_score, a.favourites
ORDER BY a.favourites DESC NULLS LAST
LIMIT :n
"""

SQL_CANDIDATES_MANGA = """
SELECT
  m.id AS media_id,
  m.mean_score,
  m.favourites,
  COALESCE(array_agg(mg.genre_name) FILTER (WHERE mg.genre_name IS NOT NULL), '{}') AS genres
FROM manga m
LEFT JOIN manga_genre mg ON mg.manga_id = m.id
GROUP BY m.id, m.mean_score, m.favourites
ORDER BY m.favourites DESC NULLS LAST
LIMIT :n
"""


def build_feats(row, vec):
  # status par défaut (si absent du vec, c’est juste ignoré)
  feats = {
    "mean_score": float(row["mean_score"] or 0),
    "log_favourites": float(np.log1p(row["favourites"] or 0)),
    "progress": 0,
    "status_PLANNING": 1,
  }
  for g in row["genres"]:
    feats[f"genre_{g}"] = 1
  return feats

# Endpoints
@router.get("/{username}")
async def get_user_id(username: str):
    try:
        user = await fetch_user_id(username)
        USER_ID_REQUESTS.labels(status="success").inc()
        return {"user_id": user["id"], "username": user["name"]}
    except Exception as e:
        USER_ID_REQUESTS.labels(status="error").inc()
        ANILIST_ERRORS.labels(endpoint="fetch_user_id").inc()
        raise


@router.get("/{username}/favorites")
async def get_user_favorites(username: str):
    user = await fetch_user_id(username)
    return await fetch_user_favorites_list(user["id"])


@router.get("/{username}/entries/{mediaType}")
async def get_user_entries(username: str, mediaType: str):
    user = await fetch_user_id(username)
    return await fetch_user_entries_list(user["id"], mediaType)



@router.get("/{username}/recommendations/{mediaType}", response_model=RecommendationsIdsResponse)
async def get_reco_ids(username: str, mediaType: MediaType, limit: int = 12):
  # 1) AniList user
  try:
    user = await fetch_user_id(username)
    anilist_user_id = int(user["id"])
  except Exception as e:
    logging.logger.exception(f"[RECO] fetch_user_id failed for {username}: {e}")
    raise HTTPException(status_code=400, detail="Pseudo AniList invalide ou AniList indisponible")

  # 2) modèle + vec
  try:
    model, vec = get_model_and_vec(str(mediaType))
    logging.logger.info(f"[RECO] model ok media={mediaType} n_features={len(vec.feature_names_)}")
  except Exception as e:
    logging.logger.exception(f"[RECO] model_store.get failed media={mediaType}: {e}")
    raise HTTPException(status_code=500, detail=f"Modèle non chargé: {e}")

  # 3) DB candidats non vus
  try:
    with engine.connect() as c:
      if mediaType == "anime":
        cand_rows = c.execute(text(SQL_CANDIDATES_ANIME), {"user_id": anilist_user_id, "n": 2000}).mappings().all()
      else:
        cand_rows = c.execute(text(SQL_CANDIDATES_MANGA), {"user_id": anilist_user_id, "n": 2000}).mappings().all()
  except Exception as e:
    logging.logger.exception(f"[RECO] DB query failed: {e}")
    raise HTTPException(status_code=500, detail=f"Erreur DB: {e}")

  if not cand_rows:
    return RecommendationsIdsResponse(username=username, mediaType=mediaType, ids=[])

  # 4) score + topK
  X_dict = [build_feats(r, vec) for r in cand_rows]
  X = vec.transform(X_dict)
  proba = model.predict_proba(X)[:, 1]
  top_idx = np.argsort(-proba)[:limit]
  ids = [int(cand_rows[i]["media_id"]) for i in top_idx]

  return RecommendationsIdsResponse(username=username, mediaType=mediaType, ids=ids)