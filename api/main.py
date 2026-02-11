from fastapi import APIRouter, FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from router.userRouter import router as user_router 
from router.anilistRouter import router as anilist_router 
from fastapi.middleware.cors import CORSMiddleware
from model_store import load_models_from_disk
from model_store import get
import logging

logger = logging.getLogger("uvicorn")
app = FastAPI()
api_router = APIRouter(prefix="/api")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "https://erra570.github.io", "http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Health sous /api :
@api_router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}



#region - - - Basic Requests :
@app.get("/")
async def read_root():
    return {"message": "Root."}

# Health à la root (utile pour docker-compose si le healthcheck tape /health)
@app.get("/health", tags=["Health"])
async def health_check_root():
    return {"status": "ok"}
#endregion

#region - - - Events :
@app.on_event("startup")
def startup():
    load_models_from_disk()
    print()

@api_router.get("/reco/ping")
def reco_ping(media: str):
    model, vec = get(media)
    return {"ok": True, "media": media, "n_features": len(vec.feature_names_)}
#endregion

#region - - - Autres routers :
api_router.include_router(user_router, prefix="/user", tags=["UserRequests"])
api_router.include_router(anilist_router, prefix="/anilistContent", tags=["ContentRequests"])
app.include_router(api_router)
Instrumentator().instrument(app).expose(app, endpoint="/metrics") # Prometheus metrics (ex: /metrics)
#endregion