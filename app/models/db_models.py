from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum, ARRAY
from sqlalchemy.sql import func
from datetime import datetime
from app.core.database import Base
from app.models.schemas import PipelineStatus


class Pipeline(Base):
    """Pipeline database model"""
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    status = Column(SQLEnum(PipelineStatus), nullable=False, default=PipelineStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_run = Column(DateTime(timezone=True), nullable=True)
    success_rate = Column(Float, default=0.0)
    records_processed = Column(Integer, default=0)
    tags = Column(ARRAY(String), default=[])

    def __repr__(self):
        return f"<Pipeline(id={self.id}, name={self.name}, status={self.status})>"


class User(Base):
    """User database model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"


class Job(Base):
    """Job database model"""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, nullable=False, index=True)
    status = Column(String(50), nullable=False, default="pending")
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    records_processed = Column(Integer, default=0)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Job(id={self.id}, pipeline_id={self.pipeline_id}, status={self.status})>"
