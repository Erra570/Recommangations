from fastapi import APIRouter
from pydantic import BaseModel
from requestsAnilistApi import (
    fetch_user_id,
    fetch_user_anime_list,
    fetch_user_manga_list,
)

router = APIRouter()

#region CLASSES
class UserResponse(BaseModel):
    user_id: int
    username: str
#endregion

#region FastAPI requests
@router.get("/{username}")
async def get_user_id(username: str):
    user = await fetch_user_id(username)
    return {"user_id": user["id"], "username": user["name"]}


@router.get("/{username}/list/anime")
async def get_user_anime_list(username: str):
    return await fetch_user_anime_list(username)


@router.get("/{username}/list/manga")
async def get_user_manga_list(username: str):
    return await fetch_user_manga_list(username)
#endregion