from fastapi import APIRouter, Depends
from datetime import datetime
from app.dependencies.auth import get_current_user, require_admin
from app.models.schemas import HealthResponse, MetricsResponse, ErrorResponse

router = APIRouter(
    prefix="/api/v1/monitoring",
    tags=["Monitoring"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="System health status - public endpoint"
)
def health_check():
    """System health check with structured response"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0",
        uptime_seconds=3600
    )

@router.get(
    "/metrics",
    response_model=MetricsResponse,
    summary="System metrics",
    description="Get current system performance metrics"
)
def get_metrics(current_user: dict = Depends(get_current_user)):
    """System metrics with structured response"""
    return MetricsResponse