"""
Application settings using Pydantic Settings.
Loads configuration from environment variables.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # MongoDB
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "regional_gap_analyzer"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False

    # CORS
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
