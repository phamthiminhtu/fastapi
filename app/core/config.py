from pydantic_settings import BaseSettings
from typing import Union


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Application
    app_name: str = "Data Engineering API"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db"
    database_url_sync: str = "postgresql://postgres:postgres@localhost:5432/fastapi_db"
    db_echo: bool = False

    # CORS - can be a string (comma-separated) or list
    cors_origins: Union[str, list[str]] = "http://localhost:8000,http://127.0.0.1:8000"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30

    # Redis Cache
    redis_url: str = "redis://localhost:6379/0"
    cache_enabled: bool = True
    cache_ttl_seconds: int = 300  # 5 minutes

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def get_cors_origins(self) -> list[str]:
        """Get CORS origins as a list"""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins


settings = Settings()
