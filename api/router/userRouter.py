from fastapi import APIRouter
import random
from schemas.reco import RecommendationsIdsResponse, MediaType

#Prometheus metrics :
from metrics import USER_ID_REQUESTS, ANILIST_ERRORS 

from requestsAnilistApi.requests import (
    fetch_user_id,
    fetch_user_favorites_list,
    fetch_user_entries_list,

    fetch_anime_list,
)

router = APIRouter()

# fake anime ids (en attendant d'avoir un endpoint de recos)
FAKE_ANIME_IDS = [181841, 227, 2001, 174788, 9253, 130003]
FAKE_MANGA_IDS = [87170, 85412, 74489, 86082, 31133, 146983]

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

@router.get("/{username}/recommendations/{mediaType}", response_model=RecommendationsIdsResponse)
def get_reco_ids(username: str, mediaType: MediaType, limit: int = 12):
    pool = FAKE_ANIME_IDS if mediaType == "anime" else FAKE_MANGA_IDS

    if not pool:
        return RecommendationsIdsResponse(username=username, mediaType=mediaType, ids=[])
    
    k = min(limit, len(pool))
    ids = random.sample(pool, k)

    return RecommendationsIdsResponse(
        username=username,
        mediaType=mediaType,
        ids=ids,
    )

#endregion