from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class MatchingSettings(BaseModel):
    match_threshold: float = 0.82
    candidate_threshold: float = 0.50
    minimum_margin: float = 0.10
    candidates_limit: int = 5

    tfidf_weight: float = 0.60
    fuzzy_weight: float = 0.25
    feature_weight: float = 0.15


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AI_SELLER_",
        env_nested_delimiter="__",
    )

    app_name: str = "AI Seller Agent"
    app_version: str = "0.1.0"

    catalog_path: Path = PROJECT_ROOT / "data" / "catalog_excel.csv"

    matching: MatchingSettings = MatchingSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
