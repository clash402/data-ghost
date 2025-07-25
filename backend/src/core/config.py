"""Configuration settings for the Data Ghost backend."""

import os
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    app_name: str = "Data Ghost Backend"
    app_version: str = "0.1.0"
    debug: bool = Field(default=False, env="DEBUG")

    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", env="OPENAI_MODEL")

    # ElevenLabs Configuration
    elevenlabs_api_key: Optional[str] = Field(default=None, env="ELEVENLABS_API_KEY")

    # Database Configuration
    database_url: str = Field(default="sqlite:///./data_ghost.db", env="DATABASE_URL")

    # ChromaDB Configuration
    chroma_db_path: str = Field(default="./chroma_db", env="CHROMA_DB_PATH")

    # File Storage Configuration
    upload_dir: str = Field(default="./uploads", env="UPLOAD_DIR")
    max_file_size: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB

    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # CORS Configuration
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"], env="CORS_ORIGINS"
    )

    class Config:
        env_file = ".env.local"
        case_sensitive = False


# Global settings instance
settings = Settings()
