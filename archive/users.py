from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
def get_users():
    return {"users": ["alice", "bob", "charlie"]}

@router.post("/")
def create_user():
    return {"message": "User created successfully"}

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User {user_id}"}