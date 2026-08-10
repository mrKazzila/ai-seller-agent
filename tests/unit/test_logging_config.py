import logging
from typing import cast

import pytest

from ai_seller_agent.config.logging import LoggingConfig, LogLevel
from ai_seller_agent.config.settings import Settings


@pytest.mark.unit
def test_logging_config_from_settings() -> None:
    settings = Settings(
        log_level="DEBUG",
        log_renderer="console",
        enable_log_diagnostics=True,
        use_utc_timestamps=False,
    )

    config = LoggingConfig.from_settings(settings)

    assert config.level == "DEBUG"
    assert config.renderer == "console"
    assert config.enable_diagnostics is True
    assert config.use_utc_timestamps is False
    assert config.resolved_level() == logging.DEBUG


@pytest.mark.unit
def test_unknown_log_level_falls_back_to_info() -> None:
    config = LoggingConfig(level=cast(LogLevel, "unknown"))

    assert config.resolved_level() == logging.INFO
