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

router = APIRouter(
    prefix="/api",
)
#endregion

#region FastAPI REQUETES :
@app.get("/")
async def read_root():
    return {"message": "Root."}

@router.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
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
    try:
        # .....








        response =""
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

#endregion


app.include_router(router)