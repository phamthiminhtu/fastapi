from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.core.database import get_db
from app.core.security import decode_access_token
from app.core.cache import get_cached_user, cache_user
from app.models.db_models import User

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Extract and validate user from JWT bearer token with caching

    Flow:
    1. Decode JWT token
    2. Check cache for user data
    3. If cache miss, query database
    4. Cache the user data
    5. Return user object

    Args:
        credentials: HTTP Bearer token from Authorization header
        db: Database session

    Returns:
        User object from database/cache

    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials

    # Decode JWT token (no DB, just cryptographic verification)
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract username from token payload
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Try to get user from cache first
    cached_user_data = get_cached_user(username)
    if cached_user_data:
        # Cache hit! Reconstruct User object from cached data
        user = User(
            id=cached_user_data["id"],
            username=cached_user_data["username"],
            email=cached_user_data["email"],
            hashed_password=cached_user_data["hashed_password"],
            role=cached_user_data["role"],
            is_active=cached_user_data["is_active"],
            created_at=cached_user_data["created_at"]
        )
    else:
        # Cache miss - query database
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Cache the user data for next time
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": str(user.created_at)
        }
        cache_user(username, user_data)

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account"
        )

    return user

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Require admin role

    Args:
        current_user: Current authenticated user

    Returns:
        User object if admin

    Raises:
        HTTPException: If user is not admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def require_data_engineer(current_user: User = Depends(get_current_user)) -> User:
    """
    Require data engineer or admin role

    Args:
        current_user: Current authenticated user

    Returns:
        User object if data engineer or admin

    Raises:
        HTTPException: If user doesn't have required role
    """
    if current_user.role not in ["admin", "data_engineer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Data engineer access required"
        )
    return current_user