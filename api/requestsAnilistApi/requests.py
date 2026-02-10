import httpx
from fastapi import HTTPException
import time
from .mapper import *
from repository.anilistImport import *

from .queries import (
    QUERY_USER_ID,
    QUERY_USER_GET_FAVORITES,
    QUERY_USER_GET_ENTRIES,

    QUERY_LIST_ANIME,
    QUERY_LIST_MANGA,

    QUERY_ALL_GENRE,
    QUERY_ALL_STAFF,
    QUERY_ALL_STUDIO,
    QUERY_ALL_TAG,
)

from metrics import (
    ANILIST_ERRORS,
)

ANILIST_API_URL = "https://graphql.anilist.co"
MEDIA_TYPE = ["MANGA", "ANIME"]
ANILIST_RATE_LIMIT = 30 #per min
last_request_timestamp = time.time()


async def anilist_post(query: str, variables: dict = {}):
    global last_request_timestamp
    if time.time() - last_request_timestamp < 60/ANILIST_RATE_LIMIT:
        time.sleep(60/ANILIST_RATE_LIMIT - (time.time() - last_request_timestamp))

    async with httpx.AsyncClient(timeout=20.0, transport = httpx.AsyncHTTPTransport(retries=2)) as client:
        #try the same request a second time while respect limit rate
        try:
            response = await client.post(
                ANILIST_API_URL,
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
        except:
            ANILIST_ERRORS.inc
            time.sleep(60/ANILIST_RATE_LIMIT)
            response = await client.post(
                ANILIST_API_URL,
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
        payload = response.json()
    last_request_timestamp = time.time()

    if payload.get("errors"):
        ANILIST_ERRORS.inc
        msg = payload["errors"][0].get("message", "AniList API error")
        raise HTTPException(status_code=404, detail=msg)

    return payload["data"]


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

async def fetch_user(username: str):
    user = await fetch_user_id(username)
    user["anime"] = await fetch_user_entries_list(user["id"], "anime")
    user["manga"] = await fetch_user_entries_list(user["id"], "manga")
    insert_media([user_to_entries(user)])
    return user

async def fetch_list(list_name, list_query, list_param, mapper, insert):
    i = 1
    while True:
        print("Fetch "+list_name+" data from Anilist "+str(i)+"/????")
        rep = await anilist_post(list_query, {"page": i} | list_param)
        print("Save "+list_name+" data from Anilist "+str(i)+"/????")
        if not insert(mapper(rep)) or not rep["Page"]["pageInfo"]["hasNextPage"]:
            break
        i += 1

    return rep


async def fetch_anime_list():
    return await fetch_list("anime", QUERY_LIST_ANIME, {"sort": "ID"}, lambda x: animes_to_entries(list_processing(x)), insert_media)

async def update_anime_list():
    return await fetch_list("anime", QUERY_LIST_ANIME, {"sort": "UPDATED_AT_DESC"}, lambda x: animes_to_entries(list_processing(x)), update_media)


async def fetch_manga_list():
    return await fetch_list("manga", QUERY_LIST_MANGA, {"sort": "ID"}, lambda x: manga_to_entries(list_processing(x)), insert_media)

async def update_manga_list():
    return await fetch_list("manga", QUERY_LIST_MANGA, {"sort": "UPDATED_AT_DESC"}, lambda x: manga_to_entries(list_processing(x)), update_media)


async def fetch_tags():
    print("Fetch tag data from Anilist...")
    rep = await anilist_post(QUERY_ALL_TAG)

    print("Save tag data...")
    add_all(tag_to_entries(rep["MediaTagCollection"]))

    return rep

async def update_tags():
    return await fetch_tags()


async def fetch_genres():
    print("Fetch genre data from Anilist...")
    rep = await anilist_post(QUERY_ALL_GENRE)

    print("Save genre data...")
    add_all(genre_to_entries(rep["GenreCollection"]))

    return rep

async def update_genres():
    return await fetch_genres()


async def fetch_staffs():
    return await fetch_list("staff", QUERY_ALL_STAFF, {"sort": "ID"}, lambda x: staff_to_entries(x["Page"]["staff"]), add_all)

async def update_staffs():
    return await fetch_list("staff", QUERY_ALL_STAFF, {"sort": "ID_DESC"}, lambda x: staff_to_entries(x["Page"]["staff"]), add_all)


async def fetch_studios():
    return await fetch_list("studio", QUERY_ALL_STUDIO, {"sort": "ID"}, lambda x: studio_to_entries(x["Page"]["studios"]), add_all)

async def update_studios():
    return await fetch_list("studio", QUERY_ALL_STUDIO, {"sort": "ID_DESC"}, lambda x: studio_to_entries(x["Page"]["studios"]), add_all)


async def fetch_all():
    purge_all()
    await fetch_genres()
    await fetch_tags()
    await fetch_staffs()
    await fetch_studios()

    await fetch_anime_list()
    await fetch_manga_list()


async def update_all():
    await update_genres()
    await update_tags()
    await update_staffs()
    await update_studios()

    await update_anime_list()
    await update_manga_list()