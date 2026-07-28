"""
TalentMind AI - Application Settings
=====================================
Centralized configuration management using Pydantic Settings.
Loads from environment variables with type validation.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# ── Base directory of the project ────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class ApplicationSettings(BaseSettings):
    """
    Core application configuration.

    All values are loaded from environment variables.
    Provides type safety and validation via Pydantic.
    """

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────
    APP_NAME: str = Field(
        default="TalentMind AI",
        description="Application name"
    )
    APP_VERSION: str = Field(
        default="1.0.0",
        description="Application version"
    )
    APP_ENV: str = Field(
        default="development",
        description="Environment: development | staging | production"
    )
    APP_DEBUG: bool = Field(
        default=False,
        description="Debug mode flag"
    )
    APP_SECRET_KEY: str = Field(
        default="change-this-in-production-min-32-chars",
        description="Secret key for security operations"
    )

    # ── Google Gemini API ────────────────────────────────────
    GOOGLE_API_KEY: str = Field(
        default="",
        description="Google Gemini API key"
    )
    GEMINI_MODEL: str = Field(
        default="gemini-1.5-pro",
        description="Gemini model identifier"
    )
    GEMINI_MAX_TOKENS: int = Field(
        default=8192,
        description="Maximum tokens per API call"
    )
    GEMINI_TEMPERATURE: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Model temperature (0=deterministic, 1=creative)"
    )

    # ── Database ─────────────────────────────────────────────
    DATABASE_URL: str = Field(
        default="sqlite:///./data/talentmind.db",
        description="SQLAlchemy database URL"
    )
    DATABASE_ECHO: bool = Field(
        default=False,
        description="SQLAlchemy query logging"
    )

    # ── File Upload ──────────────────────────────────────────
    MAX_FILE_SIZE_MB: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum upload file size in MB"
    )
    ALLOWED_FILE_TYPES: str = Field(
        default="pdf,docx,txt",
        description="Comma-separated allowed file extensions"
    )
    UPLOAD_DIR: str = Field(
        default="data/uploads",
        description="Directory for uploaded files"
    )
    PROCESSED_DIR: str = Field(
        default="data/processed",
        description="Directory for processed files"
    )

    # ── Reports ──────────────────────────────────────────────
    REPORTS_DIR: str = Field(
        default="data/reports",
        description="Directory for generated reports"
    )
    VECTOR_DB_DIR: str = Field(
        default="data/vector_db",
        description="Directory for FAISS vector index"
    )

    # ── Logging ──────────────────────────────────────────────
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level"
    )
    LOG_FILE: str = Field(
        default="logs/talentmind.log",
        description="Log file path"
    )
    LOG_MAX_BYTES: int = Field(
        default=10_485_760,
        description="Max log file size before rotation"
    )
    LOG_BACKUP_COUNT: int = Field(
        default=5,
        description="Number of log backup files"
    )

    # ── Security ─────────────────────────────────────────────
    ALLOWED_HOSTS: str = Field(
        default="localhost,127.0.0.1",
        description="Comma-separated allowed hosts"
    )

    # ── Computed Properties ──────────────────────────────────
    @property
    def allowed_file_types_list(self) -> List[str]:
        """Returns allowed file types as a list."""
        return [
            ext.strip().lower()
            for ext in self.ALLOWED_FILE_TYPES.split(",")
        ]

    @property
    def max_file_size_bytes(self) -> int:
        """Returns max file size in bytes."""
        return self.MAX_FILE_SIZE_MB * 1024 * 1024

    @property
    def is_production(self) -> bool:
        """Returns True if running in production."""
        return self.APP_ENV.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Returns True if running in development."""
        return self.APP_ENV.lower() == "development"

    @property
    def upload_dir_path(self) -> Path:
        """Returns upload directory as Path object."""
        return BASE_DIR / self.UPLOAD_DIR

    @property
    def reports_dir_path(self) -> Path:
        """Returns reports directory as Path object."""
        return BASE_DIR / self.REPORTS_DIR

    @property
    def vector_db_dir_path(self) -> Path:
        """Returns vector DB directory as Path object."""
        return BASE_DIR / self.VECTOR_DB_DIR

    # ── Validators ───────────────────────────────────────────
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validates log level is a valid Python logging level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            raise ValueError(
                f"Invalid log level '{v}'. "
                f"Must be one of: {valid_levels}"
            )
        return v.upper()

    @field_validator("APP_ENV")
    @classmethod
    def validate_app_env(cls, v: str) -> str:
        """Validates environment name."""
        valid_envs = {"development", "staging", "production"}
        if v.lower() not in valid_envs:
            raise ValueError(
                f"Invalid environment '{v}'. "
                f"Must be one of: {valid_envs}"
            )
        return v.lower()

    def validate_google_api_key(self) -> bool:
        """
        Validates Google API key is set.
        Returns True if valid, False otherwise.
        """
        return bool(
            self.GOOGLE_API_KEY
            and len(self.GOOGLE_API_KEY) > 10
            and self.GOOGLE_API_KEY != "your-google-gemini-api-key-here"
        )

    def ensure_directories(self) -> None:
        """Creates required directories if they don't exist."""
        directories = [
            BASE_DIR / self.UPLOAD_DIR,
            BASE_DIR / self.PROCESSED_DIR,
            BASE_DIR / self.REPORTS_DIR,
            BASE_DIR / self.VECTOR_DB_DIR,
            BASE_DIR / "logs",
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> ApplicationSettings:
    """
    Returns cached application settings instance.

    Uses lru_cache to ensure singleton pattern —
    settings are loaded once and reused throughout
    the application lifecycle.

    Returns:
        ApplicationSettings: Validated settings instance
    """
    settings = ApplicationSettings()
    settings.ensure_directories()
    return settings


# ── Module-level settings instance ───────────────────────────
settings = get_settings()