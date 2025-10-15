from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from datetime import datetime
from dependencies.auth import require_data_engineer, get_current_user
from models.schemas import (
    Pipeline, PipelineListResponse, PipelineActionResponse, 
    ErrorResponse, PipelineStatus
)

router = APIRouter(
    prefix="/api/v2/pipelines",
    tags=["Data Pipelines v2"],
    dependencies=[Depends(require_data_engineer)],
    responses={
        401: {"model": ErrorResponse, "description": "Authentication required"},
        403: {"model": ErrorResponse, "description": "Insufficient permissions"},
        404: {"model": ErrorResponse, "description": "Pipeline not found"}
    }
)

# Convert our data to match the models
def get_pipeline_data():
    return [
        Pipeline(
            id=1, 
            name="customer_etl", 
            status=PipelineStatus.RUNNING,
            created_at=datetime(2024, 1, 15, 10, 0, 0),
            last_run=datetime(2024, 1, 20, 14, 30, 0),
            success_rate=98.5,
            records_processed=150000,
            tags=["customer", "daily"]
        ),
        Pipeline(
            id=2, 
            name="sales_analytics", 
            status=PipelineStatus.STOPPED,
            created_at=datetime(2024, 1, 10, 9, 0, 0),
            last_run=datetime(2024, 1, 19, 23, 45, 0),
            success_rate=95.2,
            records_processed=89000,
            tags=["sales", "hourly"]
        ),
    ]

@router.get(
    "/",
    response_model=PipelineListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all pipelines",
    description="Retrieve all data pipelines with optional filtering"
)
def list_pipelines_v2(
    tag: Optional[str] = None,
    status_filter: Optional[PipelineStatus] = None,
    current_user: dict = Depends(get_current_user)
):
    """Enhanced pipeline list with filtering and structured response"""
    pipelines = get_pipeline_data()
    
    # Apply filters
    if tag:
        pipelines = [p for p in pipelines if tag in p.tags]
    
    if status_filter:
        pipelines = [p for p in pipelines if p.status == status_filter]
    
    return PipelineListResponse(
        pipelines=pipelines,
        total_count=len(pipelines),
        filters_applied={"tag": tag, "status": status_filter}
    )

@router.get(
    "/{pipeline_id}",
    response_model=Pipeline,
    responses={
        200: {"model": Pipeline, "description": "Pipeline details"},
        404: {"model": ErrorResponse, "description": "Pipeline not found"}
    },
    summary="Get pipeline by ID",
    description="Retrieve detailed information about a specific pipeline"
)
def get_pipeline_v2(
    pipeline_id: int, 
    current_user: dict = Depends(get_current_user)
):
    """Get detailed pipeline information"""
    pipelines = get_pipeline_data()
    pipeline = next((p for p in pipelines if p.id == pipeline_id), None)
    
    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline {pipeline_id} not found"
        )
    
    return pipeline

@router.post(
    "/{pipeline_id}/start",
    response_model=PipelineActionResponse,
    status_code=status.HTTP_200_OK,
    summary="Start pipeline",
    description="Start a specific pipeline with optional priority setting"
)
def start_pipeline_v2(
    pipeline_id: int,
    priority: str = "normal",
    current_user: dict = Depends(get_current_user)
):
    """Start pipeline with enhanced response"""
    # Check if pipeline exists
    pipelines = get_pipeline_data()
    pipeline = next((p for p in pipelines if p.id == pipeline_id), None)
    
    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline {pipeline_id} not found"
        )
    
    return PipelineActionResponse(
        message=f"Pipeline {pipeline_id} started with {priority} priority",
        pipeline_id=pipeline_id,
        status=PipelineStatus.RUNNING,
        performed_by=current_user["username"]
    )