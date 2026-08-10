from functools import lru_cache

from ai_seller_agent.config.settings.app import AppSettings
from ai_seller_agent.config.settings.base import Settings
from ai_seller_agent.config.settings.matching import MatchingSettings

__all__ = (
    "AppSettings",
    "MatchingSettings",
    "Settings",
    "get_settings",
)


@lru_cache
def get_settings() -> Settings:
    return Settings()
