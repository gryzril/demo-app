from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from app.init_db import ensure_schema

from app.controllers.user_controller import router as user_router  # Import controllers
from app.controllers.task_controller import router as task_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_schema()
    yield

app = FastAPI(
    title="Tasks API",
    version="0.1.0",
    description="CRUD tasks with labels and auth.",
    docs_url="/swagger",      # Swagger UI
    redoc_url=None,           # disable ReDoc
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Bootstrap controllers
app.include_router(user_router)
app.include_router(task_router)

# Misc endpoints
@app.get("/healthz", tags=["System"])
def healthz():
    return {"status": "ok"}

@app.get("/me", 
            summary="Who am I?", 
            description="Get your current user information", 
            tags=["Auth"])
def me():
    return {"email": "demo@example.com"}

