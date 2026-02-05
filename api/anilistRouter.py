from fastapi import APIRouter
from pydantic import BaseModel
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

router = APIRouter()

#region FastAPI requests
@router.get("/fetch")
async def get_anime_list():
    await fetch_all()
    return "Fetch lauched correctly."

@router.get("/fetch/anime")
async def get_anime_list():
    return await fetch_anime_list()


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
    await update_all()
    return "Fetch lauched correctly."

@router.get("/update/anime")
async def put_anime_list():
    return await update_anime_list()


@router.get("/update/manga")
async def get_manga_list():
    return await update_manga_list()


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