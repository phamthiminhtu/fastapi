from pydantic import BaseModel, Field
from pydantic import field_validator
from typing import Optional
from datetime import datetime

class Book(BaseModel):
    id: int
    title: str = Field(
        ..., 
        min_length=3, 
        description="Title must be longer than 3 characters",
    )
    author: str = Field(
        ..., 
        min_length=3, 
        description="Author must be longer than 3 characters",
    )
    price: float = Field(
        ..., 
        gt=0, 
        description="Price must be greater than 0",
    )
    is_available: bool = Field(
        default=True, 
        description="Is available must be a boolean"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
