from fastapi import APIRouter
from pydantic import BaseModel
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
    user = await fetch_user_id(username)
    return {"user_id": user["id"], "username": user["name"]}

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
    return await fetch_anime_list()


@router.get("/list/manga")
async def get_user_manga_list():
    return await fetch_manga_list()
#endregion