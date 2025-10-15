from fastapi import FastAPI
from routers import pipelines, monitoring, jobs
from middleware.request_id import request_id_middleware
from middleware.timing import timing_middleware

# API metadata
app = FastAPI(
    title="Data Engineering API",
    description="API for managing data pipelines and monitoring",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include middleware
app.middleware("http")(request_id_middleware)
app.middleware("http")(timing_middleware)

# Include routers with proper organization
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