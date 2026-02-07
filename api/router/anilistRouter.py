from fastapi import APIRouter
from time import perf_counter
from requestsAnilistApi.requests import (
    fetch_anime_list,
    fetch_manga_list,
    fetch_tags,
    fetch_genres,
    fetch_staffs,
    fetch_studios,
    fetch_all,

    update_anime_list,
    update_manga_list,
    update_tags,
    update_genres,
    update_staffs,
    update_studios,
    update_all,
)
from repository.anilistImport import (
    get_anime_short,
    get_anime,
    get_manga_short,
    get_manga,
)

#Prometheus metrics :
from metrics import (
    ANIME_LIST_DURATION, 
    DATABASE_UPDATE_ALL_LAST_DURATION,
    DATABASE_UPDATE_ALL_DURATION,
    DATABASE_UPDATE_ANIME_DURATION,
    DATABASE_UPDATE_MANGA_DURATION 
)

router = APIRouter()

#region FastAPI requests    
@router.get("/short/anime/{id}")
async def get_short_anime_with_id(id : int):
    return get_anime_short(id)

@router.get("/short/manga/{id}")
async def get_short_manga_with_id(id : int):
    return get_manga_short(id)

@router.get("/anime/{id}")
async def get_anime_with_id(id : int):
    return get_anime(id)

@router.get("/manga/{id}")
async def get_manga_with_id(id : int):
    return get_manga(id)

#region fetch and update db
@router.get("/fetch")
async def get_anime_list():
    await fetch_all()

@router.get("/fetch/anime")
async def get_anime_list():
    start = perf_counter() 
    try:
        return await fetch_anime_list() 
    finally:
        time_tot = perf_counter() - start
        ANIME_LIST_DURATION.observe(time_tot)


@router.get("/fetch/manga")
async def get_manga_list():
    return await fetch_manga_list()


@router.get("/fetch/tag")
async def get_tag_list():
    return await fetch_tags()


@router.get("/fetch/genre")
async def get_genres():
    return await fetch_genres()


@router.get("/fetch/staff")
async def get_staffs():
    return await fetch_staffs()

@router.get("/fetch/studio")
async def get_studios():
    return await fetch_studios()

@router.get("/update")
async def get_anime_list():
    start = perf_counter() 
    try:
        await update_all()
    finally:
        time_tot = perf_counter() - start
        DATABASE_UPDATE_ALL_DURATION.observe(time_tot)
        DATABASE_UPDATE_ALL_LAST_DURATION.set(time_tot)
    

@router.get("/update/anime")
async def put_anime_list():
    start = perf_counter() 
    try:
        return await update_anime_list()
    finally:
        time_tot = perf_counter() - start
        DATABASE_UPDATE_ANIME_DURATION.observe(time_tot)


@router.get("/update/manga")
async def get_manga_list():
    start = perf_counter() 
    try:
        return await update_manga_list()
    finally:
        time_tot = perf_counter() - start
        DATABASE_UPDATE_MANGA_DURATION.observe(time_tot)

@router.get("/update/tag")
async def get_tag_list():
    return await update_tags()


@router.get("/update/genre")
async def get_genres():
    return await update_genres()


@router.get("/update/staff")
async def get_staffs():
    return await update_staffs()

@router.get("/update/studio")
async def get_studios():
    return await update_studios()
#endregion