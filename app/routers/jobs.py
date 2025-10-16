from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"],
    responses={503: {"description": "Service unavailable"}}
)

@router.get("/")
def get_jobs():
    return {"jobs": []}

@router.post("/")
def create_job():
    return {"message": "created"}