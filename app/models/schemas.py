from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PipelineStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"
    PENDING = "pending"

class PipelineBase(BaseModel):
    name: str = Field(..., description="Pipeline name")
    status: PipelineStatus
    tags: List[str] = Field(default=[], description="Pipeline tags")

class Pipeline(PipelineBase):
    id: int = Field(..., description="Pipeline ID")
    created_at: datetime
    last_run: Optional[datetime] = None
    success_rate: float = Field(..., ge=0, le=100, description="Success rate percentage")
    records_processed: int = Field(..., ge=0)

class PipelineListResponse(BaseModel):
    pipelines: List[Pipeline]
    total_count: int
    filters_applied: Dict[str, Any] = {}
    api_version: str = "v2"

class PipelineActionResponse(BaseModel):
    message: str
    pipeline_id: int
    status: PipelineStatus
    timestamp: datetime = Field(default_factory=datetime.now)
    performed_by: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    api_version: str = "v2"

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    uptime_seconds: Optional[int] = None

class MetricsResponse(BaseModel):
    active_pipelines: int
    total_records_processed: int
    cpu_usage: float = Field(..., ge=0, le=100)
    memory_usage: float = Field(..., ge=0, le=100)
    requested_by: str