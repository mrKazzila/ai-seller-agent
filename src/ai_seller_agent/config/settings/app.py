from pathlib import Path

from pydantic import BaseModel, field_validator

from ai_seller_agent.config.logging import LogLevel, LogRenderer
from ai_seller_agent.config.settings._base_settings import PROJECT_ROOT

__all__ = ("AppSettings",)


class AppSettings(BaseModel):
    """Application settings."""

    name: str = "AI Seller Agent"
    version: str = "0.1.0"
    host: str = "127.0.0.1"
    port: int = 8000

    log_level: LogLevel = "INFO"
    log_renderer: LogRenderer = "json"
    enable_log_diagnostics: bool = False
    use_utc_timestamps: bool = True

    catalog_path: Path = PROJECT_ROOT / "data" / "catalog_excel.csv"

    @field_validator("catalog_path", mode="after")
    @classmethod
    def resolve_catalog_path(cls, value: Path) -> Path:
        if value.is_absolute():
            return value
        return PROJECT_ROOT / value
