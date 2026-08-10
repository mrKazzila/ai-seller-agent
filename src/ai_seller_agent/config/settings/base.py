from typing import final

from pydantic import Field

from ai_seller_agent.config.settings._base_settings import BaseAppSettings
from ai_seller_agent.config.settings.app import AppSettings
from ai_seller_agent.config.settings.matching import MatchingSettings

__all__ = ("Settings",)


@final
class Settings(BaseAppSettings):
    app: AppSettings = Field(default_factory=AppSettings)
    matching: MatchingSettings = Field(default_factory=MatchingSettings)
