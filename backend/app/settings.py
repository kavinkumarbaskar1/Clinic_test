"""Environment-based application settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    app_name: str = "Clinic Booking API"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    model_config = SettingsConfigDict(
        env_prefix="CLINIC_",
        env_file=".env",
        extra="ignore",
    )


def get_settings() -> Settings:
    """Return application settings."""
    return Settings()
