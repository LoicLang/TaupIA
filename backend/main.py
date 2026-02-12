"""
FastAPI backend pour Kholleur AI.

Point d'entree: uvicorn backend.main:app --reload
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.dependencies import init_services
from backend.auth import get_auth_dependencies
from backend.api.chapters import router as chapters_router
from backend.api.providers import router as providers_router
from backend.api.sessions import router as sessions_router
from backend.api.kholle import router as kholle_router
from backend.api.ocr import router as ocr_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise les services au demarrage."""
    init_services()
    yield


app = FastAPI(
    title="Kholleur AI API",
    description="API pour simuler des kholles de maths MPSI",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth (conditionnel : actif si CLERK_PUBLISHABLE_KEY est defini)
auth_deps = get_auth_dependencies()

# Routers publics (lecture seule)
app.include_router(chapters_router, prefix="/api")
app.include_router(providers_router, prefix="/api")

# Routers proteges (auth Clerk requise en production)
app.include_router(sessions_router, prefix="/api", dependencies=auth_deps)
app.include_router(kholle_router, prefix="/api", dependencies=auth_deps)
app.include_router(ocr_router, prefix="/api", dependencies=auth_deps)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
