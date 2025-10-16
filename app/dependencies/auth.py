from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security = HTTPBearer()

# Mock users database
users_db = {
    "admin_token": {"username": "admin", "role": "admin"},
    "user_token": {"username": "user", "role": "user"},
    "engineer_token": {"username": "engineer", "role": "data_engineer"}
}

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract user from bearer token"""
    token = credentials.credentials
    
    if token not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return users_db[token]

async def require_admin(current_user: dict = Depends(get_current_user)):
    """Require admin role"""
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

async def require_data_engineer(current_user: dict = Depends(get_current_user)):
    """Require data engineer or admin role"""
    if current_user["role"] not in ["admin", "data_engineer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Data engineer access required"
        )
    return current_user