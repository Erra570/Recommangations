from fastapi import APIRouter

#Prometheus metrics :
from metrics import USER_ID_REQUESTS 

from requestsAnilistApi.requests import (
    fetch_user_id,
    fetch_user_favorites_list,
    fetch_user_entries_list,

    fetch_anime_list,
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
#endregion