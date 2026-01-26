import httpx
from fastapi import HTTPException

from .queries import (
    QUERY_USER_ID,
    QUERY_USER_LIST_ANIME,
    QUERY_USER_LIST_MANGA,
)

ANILIST_API_URL = "https://graphql.anilist.co"


async def anilist_post(query: str, variables: dict):
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            ANILIST_API_URL,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        payload = response.json()

    if payload.get("errors"):
        msg = payload["errors"][0].get("message", "AniList API error")
        raise HTTPException(status_code=404, detail=msg)

    return payload["data"]


async def fetch_user_id(username: str):
    data = await anilist_post(QUERY_USER_ID, {"username": username})
    user = data.get("User")
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user


async def fetch_user_anime_list(username: str):
    return await anilist_post(QUERY_USER_LIST_ANIME, {"username": username})


async def fetch_user_manga_list(username: str):
    return await anilist_post(QUERY_USER_LIST_MANGA, {"username": username})