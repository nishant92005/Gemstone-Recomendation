import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

BACKEND_DIR = Path(__file__).resolve().parent
load_dotenv(BACKEND_DIR / ".env")

try:
    from backend.routes.auth import router as auth_router
    from backend.routes.consult import router as consult_router
    from backend.routes.geo import router as geo_router
except ModuleNotFoundError:
    from routes.auth import router as auth_router
    from routes.consult import router as consult_router
    from routes.geo import router as geo_router

app = FastAPI(title="Navaratna API")

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(geo_router)
app.include_router(consult_router)


@app.get("/")
async def root():
    return {
        "service": "Navaratna API",
        "status": "ok",
        "docs": "/docs",
        "frontend": frontend_url,
    }


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "navaratna-api"}
