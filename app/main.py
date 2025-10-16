from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import pipelines, monitoring, jobs, auth
from app.middleware.request_id import request_id_middleware
from app.middleware.timing import timing_middleware
from app.core.database import init_db, close_db
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("Initializing database...")
    await init_db()
    print("Database initialized successfully")
    yield
    # Shutdown
    print("Closing database connections...")
    await close_db()
    print("Database connections closed")


# API metadata
app = FastAPI(
    title=settings.app_name,
    description="API for managing data pipelines and monitoring",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include middleware
app.middleware("http")(request_id_middleware)
app.middleware("http")(timing_middleware)

# Include routers with proper organization
app.include_router(auth.router)
app.include_router(pipelines.router)
app.include_router(monitoring.router)
app.include_router(jobs.router)

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Data Engineering API",
        "docs": "/docs",
        "health": "/api/v1/monitoring/health"
    }