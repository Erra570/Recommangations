from fastapi import APIRouter

#Prometheus metrics :
from time import perf_counter
from metrics import ANIME_LIST_DURATION, USER_ID_REQUESTS 

from requestsAnilistApi.requests import (
    fetch_user_id,
    fetch_user_favorites_list,
    fetch_user_entries_list,

    fetch_anime_list,
    fetch_manga_list,    
)

router = APIRouter()

#region FastAPI requests
@router.get("/{username}")
async def get_user_id(username: str):    
    try:
        user = await fetch_user_id(username)
        USER_ID_REQUESTS.labels(status="success").inc()
        return {"user_id": user["id"], "username": user["name"]}
    except Exception as e:
        USER_ID_REQUESTS.labels(status="error").inc()

@router.get("/{username}/favorites")
async def get_user_favorites(username: str):
    user = await fetch_user_id(username)  
    return await fetch_user_favorites_list(user["id"])

@router.get("/{username}/entries/{mediaType}")
async def get_user_entries(username: str, mediaType: str):
    user = await fetch_user_id(username)  
    return await fetch_user_entries_list(user["id"], mediaType)


@router.get("/list/anime")
async def get_user_anime_list():
    start = perf_counter() 
    try:
        return await fetch_anime_list() 
    finally:
        time_tot = perf_counter() - start
        ANIME_LIST_DURATION.observe(time_tot)


@router.get("/list/manga")
async def get_user_manga_list():
    return await fetch_manga_list()
#endregion