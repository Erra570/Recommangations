from fastapi import APIRouter, FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.staticfiles import StaticFiles
from userRouter import router as user_router 



app = FastAPI()
api_router = APIRouter(prefix="/api")

#on cherche le dossier web qui est dans le dossier api/
app.mount("/ui", StaticFiles(directory="web", html=True), name="web")

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



#region - - - Autres routers :
api_router.include_router(user_router, prefix="/user", tags=["UserRequests"])
app.include_router(api_router)
Instrumentator().instrument(app).expose(app, endpoint="/metrics") # Prometheus metrics (ex: /metrics)
#endregion