from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime
from app.dependencies.auth import require_data_engineer, get_current_user
from app.core.database import get_db
from app.models.schemas import (
    Pipeline as PipelineSchema, PipelineListResponse, PipelineActionResponse,
    ErrorResponse, PipelineStatus
)
from app.models.db_models import Pipeline as PipelineModel

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

@router.get(
    "/",
    response_model=PipelineListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all pipelines",
    description="Retrieve all data pipelines with optional filtering"
)
async def list_pipelines_v2(
    tag: Optional[str] = None,
    status_filter: Optional[PipelineStatus] = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Enhanced pipeline list with filtering and structured response"""
    query = select(PipelineModel)

    # Apply filters
    if status_filter:
        query = query.where(PipelineModel.status == status_filter)

    result = await db.execute(query)
    pipelines = result.scalars().all()

    # Filter by tag (array operation)
    if tag:
        pipelines = [p for p in pipelines if p.tags and tag in p.tags]

    # Convert to schema
    pipeline_schemas = [PipelineSchema.model_validate(p) for p in pipelines]

    return PipelineListResponse(
        pipelines=pipeline_schemas,
        total_count=len(pipeline_schemas),
        filters_applied={"tag": tag, "status": status_filter}
    )

@router.get(
    "/{pipeline_id}",
    response_model=PipelineSchema,
    responses={
        200: {"model": PipelineSchema, "description": "Pipeline details"},
        404: {"model": ErrorResponse, "description": "Pipeline not found"}
    },
    summary="Get pipeline by ID",
    description="Retrieve detailed information about a specific pipeline"
)
async def get_pipeline_v2(
    pipeline_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed pipeline information"""
    query = select(PipelineModel).where(PipelineModel.id == pipeline_id)
    result = await db.execute(query)
    pipeline = result.scalar_one_or_none()

    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline {pipeline_id} not found"
        )

    return PipelineSchema.model_validate(pipeline)

@router.post(
    "/{pipeline_id}/start",
    response_model=PipelineActionResponse,
    status_code=status.HTTP_200_OK,
    summary="Start pipeline",
    description="Start a specific pipeline with optional priority setting"
)
async def start_pipeline_v2(
    pipeline_id: int,
    priority: str = "normal",
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Start pipeline with enhanced response"""
    # Check if pipeline exists
    query = select(PipelineModel).where(PipelineModel.id == pipeline_id)
    result = await db.execute(query)
    pipeline = result.scalar_one_or_none()

    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline {pipeline_id} not found"
        )

    # Update pipeline status
    pipeline.status = PipelineStatus.RUNNING
    pipeline.last_run = datetime.now()
    await db.commit()

    return PipelineActionResponse(
        message=f"Pipeline {pipeline_id} started with {priority} priority",
        pipeline_id=pipeline_id,
        status=PipelineStatus.RUNNING,
        performed_by=current_user["username"]
    )