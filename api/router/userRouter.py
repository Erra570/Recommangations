from fastapi import APIRouter
import os
import numpy as np
from sqlalchemy import create_engine, text
from fastapi import HTTPException
import logging

from model_store import get as get_model_and_vec
from requestsAnilistApi.requests import fetch_user_id
from repository.userRepository import *
from schemas.reco import RecommendationsIdsResponse, MediaType

# Prometheus metrics :
from metrics import USER_ID_REQUESTS, ANILIST_ERRORS

from requestsAnilistApi.requests import (
    fetch_user_id,
    fetch_user_favorites_list,
    fetch_user_entries_list,
    fetch_user,
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
		m.id,
		m.mean_score,
		m.variance_score,
		m.favourites,
		m.format,
		m.country_of_origin,
		extract(epoch from start_date) start,
		COALESCE(array_agg(DISTINCT g.genre_name), '{}') AS genres,
		COALESCE(array_agg(DISTINCT t.tag_id), '{}') AS tags,
		COALESCE(array_agg(DISTINCT s.staff_id), '{}') AS staffs
	FROM anime m 
	LEFT JOIN user_anime u  ON u.anime_id = m.id AND u.user_id = :user_id
	LEFT JOIN anime_genre g ON g.anime_id = m.id
	LEFT JOIN anime_tag t   ON t.anime_id = m.id
	LEFT JOIN anime_staff s ON s.anime_id = m.id
    WHERE u.user_id IS NULL
	GROUP BY
		m.id,
		m.mean_score,
		m.variance_score,
		m.favourites,
		m.format,
		m.country_of_origin,
		start
"""

SQL_CANDIDATES_MANGA = """
    SELECT
    m.id,
    m.mean_score,
    m.variance_score,
    m.favourites,
    m.format,
    m.country_of_origin,
    extract(epoch from start_date) start,
    COALESCE(array_agg(DISTINCT g.genre_name), '{}') AS genres,
    COALESCE(array_agg(DISTINCT t.tag_id), '{}') AS tags,
    COALESCE(array_agg(DISTINCT s.staff_id), '{}') AS staffs
    FROM manga m 
    LEFT JOIN user_manga u  ON u.manga_id = m.id AND u.user_id = :user_id
    LEFT JOIN manga_genre g ON g.manga_id = m.id
    LEFT JOIN manga_tag t   ON t.manga_id = m.id
    LEFT JOIN manga_staff s ON s.manga_id = m.id
    WHERE u.user_id IS NULL
    GROUP BY
    m.id,
    m.mean_score,
    m.variance_score,
    m.format,
    m.country_of_origin,
    m.favourites,
    start
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


@router.get("/fetch/{username}")
async def get_user_entries(username: str):
    return await fetch_user(username)


@router.get("/stat/{username}/{mediaType}")
async def get_user_entries(username: str, mediaType: MediaType):
    user = await fetch_user(username)
    return get_user_stat(user["id"], mediaType)


@router.get("/{username}/recommendations/{mediaType}", response_model=RecommendationsIdsResponse)
async def get_reco_ids(username: str, mediaType: MediaType, limit: int = 12):
  # 1) AniList user
  try:
    user = await fetch_user_id(username)
    anilist_user_id = int(user["id"])
  except Exception as e:
    logging.exception(f"[RECO] fetch_user_id failed for {username}: {e}")
    raise HTTPException(status_code=400, detail="Pseudo AniList invalide ou AniList indisponible")

  # 2) modèle + vec
  try:
    model, vec = get_model_and_vec(str(mediaType))
    logging.info(f"[RECO] model ok media={mediaType} n_features={len(vec.feature_names_)}")
  except Exception as e:
    logging.exception(f"[RECO] model_store.get failed media={mediaType}: {e}")
    raise HTTPException(status_code=500, detail=f"Modèle non chargé: {e}")

  # 3) DB candidats non vus
  try:
    with engine.connect() as c:
      if mediaType == "anime":
        medias = c.execute(text(SQL_CANDIDATES_ANIME), {"user_id": anilist_user_id}).mappings().all()
      else:
        medias = c.execute(text(SQL_CANDIDATES_MANGA), {"user_id": anilist_user_id}).mappings().all()
  except Exception as e:
    logging.exception(f"[RECO] DB query failed: {e}")
    raise HTTPException(status_code=500, detail=f"Erreur DB: {e}")

  if not medias:
    return RecommendationsIdsResponse(username=username, mediaType=mediaType, ids=[])

  # 4) score + topK
  user = get_user_stat(anilist_user_id, mediaType)
  X_dict = []
  for media in medias:
      feats = {
          "delta_mean_score": float(media["mean_score"] or 0) - float(user["mean_mean_score"] or 0),
          "delta_variance_score": float(media["variance_score"] or 0) - float(user["mean_variance_score"] or 0),
          "delta_favourites": float(media["favourites"] or 0) - float(user["mean_favourites"] or 0),
          #"delta_mean_start_date": float(user["mean_start"] or 0) - float(media["start"] or 0),
          "nb_fiting_genres": sum([1 for g in (media.get("genres") or []) if g in user["genre"]]),
          "nb_fiting_tags": sum([1 for g in (media.get("tags") or []) if g in user["tag"]]),
          "country_of_origin_fiting": user[media["country_of_origin"]] if media["country_of_origin"] in user else 0,
          "format_fiting": user[media["format"]] if media["format"] in user else 0#,"nb_fiting_staffs": sum([1 for g in (media.get("staffs") or []) if g in user["staff"]])
      }

      X_dict.append(feats)
    
  X = vec.transform(X_dict)
  proba = model.predict_proba(X)[:, 1]
  top_idx = np.argsort(-proba)[:limit]
  ids = [int(medias[i]["id"]) for i in top_idx]

  return RecommendationsIdsResponse(username=username, mediaType=mediaType, ids=ids)