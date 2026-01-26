import httpx
from fastapi import HTTPException
import json
import numpy as np
import os.path

from queries import (
    QUERY_USER_ID,
    QUERY_USER_GET_FAVORITES,
    QUERY_USER_GET_ENTRIES,


    QUERY_LIST_ANIME,
    QUERY_LIST_MANGA,
)

ANILIST_API_URL = "https://graphql.anilist.co"
MEDIA_TYPE = ["MANGA", "ANIME"]


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

def list_processing(list: dict):
    medias = list["Page"]["media"]
    rm_list = []
    i = -1
    for media in medias:
        i += 1
        if media["stats"]["scoreDistribution"] == None :
            rm_list.append(i)
        else :
            #date processing
            media["startDate"] = str(media["startDate"]["day"])+"-"+str(media["startDate"]["month"])+"-"+str(media["startDate"]["year"])

            # tag processing
            j = 0
            while j < len(media["tags"]):
                if media["tags"][j]["rank"] < 40:
                    media["tags"].pop(j)
                else:
                    j += 1
            
            # score processing
            nb = 0
            media["averageScore"] = 0
            media["scoreVariance"] = 0
            for score in media["stats"]["scoreDistribution"]:
                nb += score["amount"]
                media["averageScore"] += score["score"] * score["amount"]
            media["averageScore"] = (int) (media["averageScore"] / nb)
            
            for score in media["stats"]["scoreDistribution"]:
                media["scoreVariance"] += ((score["score"] - media["averageScore"]) ** 2) * score["amount"]
            media["scoreVariance"] = (int) (np.sqrt(media["scoreVariance"] / nb))

            # status processing
            media["current_completed"] = 0
            media["planned"] = 0
            media["dropped_paused"] = 0
            for statu in media["stats"]["statusDistribution"]:
                if statu["status"] in ["CURRENT", "COMPLETED"]:
                    media["current_completed"] += statu["amount"]
                elif statu["status"] == "PLANNING":
                    media["planned"] += statu["amount"]
                elif statu["status"] in ["DROPPED", "PAUSED"]:
                    media["dropped_paused"] += statu["amount"]
            media.pop("stats")

            #staff processing
            media["staffs"] = []
            for i in range(len(media["staff"]["edges"])):
                if media["staff"]["edges"][i]["role"] in ["Story", "Art", "Story & Art", "Original Story", "Original Creator", "Director"]:
                    media["staffs"].append(media["staff"]["nodes"][i]["id"])
            media.pop("staff")

            #studio processing
            media["studio_old"] = media["studios"]
            media["studios"] = []
            for studio in media["studio_old"]["nodes"]:
                media["studios"].append(studio["id"])
            media.pop("studio_old")

            #cover url 
            media["coverImage"] = media["coverImage"]["large"]

    if len(rm_list) > 0:
        for i in rm_list.reverse():
            medias.pop(i)

    return medias

# ----------------

async def fetch_user_id(username: str):
    data = await anilist_post(QUERY_USER_ID, {"username": username})
    user = data.get("User")
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user

async def fetch_user_favorites_list(userId: int):
    return await anilist_post(QUERY_USER_GET_FAVORITES, {"userId": userId})


async def fetch_user_entries_list(userId: int, mediaType: str):
    if mediaType not in MEDIA_TYPE:
        raise HTTPException(status_code=404, detail=f"Type {mediaType} inconnu. Liste des types : {MEDIA_TYPE}")
    return await anilist_post(QUERY_USER_GET_ENTRIES, {"userId": userId, "type": mediaType})


async def fetch_anime_list():
    if os.path.isfile("./../../data/tmp/anime.json"):
        try:
            with open("./../../data/tmp/anime.json", "r") as f:
                return json.load(f)
        except ValueError:
            print("anime.json currupted.")
        
    print("Fetch data from Anilist...")
    rep = await anilist_post(QUERY_LIST_ANIME, {"page": 0})
    print("Decode data from Anilist...")
    with open("./../../data/tmp/anime.json", "w") as f:
        json.dump(list_processing(rep), f, indent=2)
    return rep


async def fetch_manga_list():
    return await anilist_post(QUERY_LIST_MANGA, {"page": 0})