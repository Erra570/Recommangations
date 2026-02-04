import httpx
from fastapi import HTTPException
import json
import numpy as np
import os.path
import re
from .mapper import *
from repository.anilistImport import *
from datetime import datetime

from .queries import (
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

#region formatting
def list_processing(list: dict):
    #patern for match staff 
    pattern = re.compile("^[Story|Art|Story & Art|Original Story|Original Creator|Director].*$")

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
            media["meanScore"] = 0
            media["scoreVariance"] = 0
            for score in media["stats"]["scoreDistribution"]:
                nb += score["amount"]
                media["meanScore"] += score["score"] * score["amount"]
            media["meanScore"] = (int) (media["meanScore"] / nb)
            
            for score in media["stats"]["scoreDistribution"]:
                media["scoreVariance"] += ((score["score"] - media["meanScore"]) ** 2) * score["amount"]
            media["scoreVariance"] = (int) (np.sqrt(media["scoreVariance"] / nb))

            # status processing
            media["completedWatching"] = 0
            media["planning"] = 0
            media["droppedPaused"] = 0
            for statu in media["stats"]["statusDistribution"]:
                if statu["status"] in ["CURRENT", "COMPLETED"]:
                    media["completedWatching"] += statu["amount"]
                elif statu["status"] == "PLANNING":
                    media["planning"] += statu["amount"]
                elif statu["status"] in ["DROPPED", "PAUSED"]:
                    media["droppedPaused"] += statu["amount"]
            media.pop("stats")

            #staff processing
            media["staffs"] = []
            for i in range(len(media["staff"]["edges"])):
                if pattern.match(media["staff"]["edges"][i]["role"]):
                    staff = {"id": media["staff"]["nodes"][i]["id"], "role": media["staff"]["edges"][i]["role"]}
                    media["staffs"].append(staff)
            media.pop("staff")

            #studio processing
            if "studios" in media:
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

# listMedia est soit la liste des media MANGA, soit ANIME (pas les 2)
def list_processing_user_infos(listMedia: dict, listFav: dict, mediaType: str):
    formatted_list = []

    # Booléens des oeuvres mises en favories :
    tmp = listFav["User"]["favourites"][mediaType]["nodes"]
    fav_ids = {node["id"] for node in tmp}

    oeuvres = listMedia["MediaListCollection"]["lists"]      
    for list_by_entriesStatus in oeuvres:
        tmp_list = list_by_entriesStatus["entries"] # 1ère list des entries : COMPLETED, 2e : PAUSED, etc.

        for item in tmp_list:
            # Date :
            if item["updatedAt"] != 0 :
                tmp = datetime.fromtimestamp(item["updatedAt"])
                date = str(tmp.day)+"-"+str(tmp.month)+"-"+str(tmp.year)
            elif item["completedAt"]["month"] is None:
                date = str(item["completedAt"]["day"])+"-"+str(item["completedAt"]["month"])+"-"+str(item["completedAt"]["year"])
            else :
                date = str(item["startDate"]["day"])+"-"+str(item["startDate"]["month"])+"-"+str(item["startDate"]["year"])
            
            isFavorite = item["media"]["id"] in fav_ids
            # Other infos :
            formatted_entry = {
                "id": item["media"]["id"],
                "isFavorite": isFavorite, 
                "status": item["status"],
                "score": item["score"],
                "progress": item["progress"],
                "repeat": item["repeat"],
                "date": date
            }

            a=item["media"]["id"]
            # print(f"- - -Id : {a}")
            formatted_list.append(formatted_entry) 
    return formatted_list
#endregion

#region fetches
async def fetch_user_id(username: str):
    data = await anilist_post(QUERY_USER_ID, {"username": username})
    user = data.get("User")
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user

async def fetch_user_favorites_list(userId: int):
    return await anilist_post(QUERY_USER_GET_FAVORITES, {"userId": userId})

async def fetch_user_entries_list(userId: int, mediaType: str):
    mediaType = mediaType.upper()
    if mediaType not in MEDIA_TYPE:
        raise HTTPException(status_code=404, detail=f"Type {mediaType} inconnu. Liste des types : {MEDIA_TYPE}")
    
    # if os.path.isfile(f"./../../data/tmp/userInfos_{mediaType}.json"):
    #     try:
    #         with open(f"./../../data/tmp/userInfos_{mediaType}.json", "r") as f:
    #            return json.load(f)
    #     except ValueError:
    #         print(f"userInfos_{mediaType}.json corrupted.")

    print("Fetch user data from Anilist...")
    listMedia = await anilist_post(QUERY_USER_GET_ENTRIES, {"userId": userId, "type": mediaType})
    listFav = await anilist_post(QUERY_USER_GET_FAVORITES, {"userId": userId})

    print("Decode data from Anilist...")
    formatted = list_processing_user_infos(listMedia, listFav, mediaType.lower())
    
    # os.makedirs("./../../data/tmp", exist_ok=True)
    # with open(f"./../../data/tmp/userInfos_{mediaType}.json", "w") as f:
    #      json.dump(formatted, f, indent=2)
    return formatted

async def fetch_list(list_name, list_query):
    """if os.path.isfile("./../../data/tmp/"+list_name+".json"):
        try:
            with open("./../../data/tmp/"+list_name+".json", "r") as f:
                return json.load(f)
        except ValueError:
            print(list_name+".json currupted.")"""

    print("Fetch "+list_name+" data from Anilist...")
    i = 1
    rep = await anilist_post(list_query("ID"), {"page": 0})
    rep_all = np.array(list_processing(rep))
    while rep["Page"]["pageInfo"]["hasNextPage"] and i < 10:
        print("Fetch "+list_name+" data from Anilist "+str(i)+"/???")
        rep = await anilist_post(list_query("ID"), {"page": i})
        rep_all = np.concatenate((rep_all, np.array(list_processing(rep))))
        i += 1
    
    print("Save "+list_name+" data...")
    rep_all = rep_all.tolist()
    """with open("./../../data/tmp/"+list_name+".json", "w") as f:
        json.dump(rep_all, f, indent=2)"""
    insert_media(to_animes_entries(rep_all))
    return rep_all

async def fetch_anime_list():
    return await fetch_list("anime", QUERY_LIST_ANIME)


async def fetch_manga_list():
    return await fetch_list("manga", QUERY_LIST_MANGA)
