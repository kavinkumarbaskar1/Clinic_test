"""Application configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings kept on the backend side of the application."""

    app_name: str = "Clinic Booking API"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    database_path: Path = Path("clinic_booking.sqlite3")
    show_api_docs: bool = False
    session_signing_key: SecretStr | None = None
    staff_identity_issuer: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="CLINIC_",
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached environment-backed settings."""
    return Settings()
