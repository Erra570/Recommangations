from fastapi import APIRouter, FastAPI, HTTPException
import httpx
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator


#region CLASSES
class UserResponse(BaseModel):
    user_id: int
    username: str
#endregion

#region CONFIGS
ANILIST_API_URL = "https://graphql.anilist.co"

tags_metadata = [
    {
        "name": "Health",
        "description": "Health check endpoints",
    }
]

app = FastAPI(
    title="RecoMangaTion API",
    description="API for AniList application",
    version="0.1.0",
    openapi_tags=tags_metadata,
    redoc_url="/docs",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

router = APIRouter(prefix="/api")
#endregion


#region FastAPI ROUTES
@app.get("/")
async def read_root():
    return {"message": "Root."}


# Health root (utile pour docker-compose si le healthcheck tape /health)
@app.get("/health", tags=["Health"])
async def health_check_root():
    return {"status": "ok"}


# Health sous /api (cohérent avec le router)
@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}


@app.get("/user/{username}", response_model=UserResponse)
async def get_user_id(username: str):
    query = """
        query ($username: String) {
            User(name: $username) {
                id
                name
            }
        }
    """
    variables = {"username": username}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                ANILIST_API_URL,
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json", "Accept": "application/json"},
            )
            response.raise_for_status()
            payload = response.json()

        # AniList peut renvoyer "errors" même si HTTP 200
        if payload.get("errors"):
            msg = payload["errors"][0].get("message", "AniList API error")
            raise HTTPException(status_code=404, detail=msg)

        user = payload.get("data", {}).get("User")
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur AniList introuvable")

        return UserResponse(user_id=user["id"], username=user["name"])

    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Erreur lors de la communication avec AniList: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne: {str(e)}"
        )


# Exemple: récupérer la liste ANIME de l'utilisateur (données brutes)
@router.get("/user/{username}/list/anime")
async def get_user_anime_list(username: str):
    query = """
    query ($username: String) {
      MediaListCollection(userName: $username, type: ANIME) {
        lists {
          entries {
            status
            score
            media {
              id
              type
              format
              seasonYear
              popularity
              meanScore
              trending
              genres
              tags { name }
              title { romaji english }
            }
          }
        }
      }
    }
    """
    variables = {"username": username}

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                ANILIST_API_URL,
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json", "Accept": "application/json"},
            )
            response.raise_for_status()
            payload = response.json()

        if payload.get("errors"):
            msg = payload["errors"][0].get("message", "AniList API error")
            raise HTTPException(status_code=404, detail=msg)

        return payload

    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Erreur lors de la communication avec AniList: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne: {str(e)}"
        )


app.include_router(router)

# Prometheus metrics (ex: /metrics)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
#endregion