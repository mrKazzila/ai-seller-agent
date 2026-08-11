import json
import logging

import pytest
import structlog

from ai_seller_agent.config.logging import LoggingConfig
from ai_seller_agent.infrastructure.observability import setup_logging


@pytest.mark.unit
@pytest.mark.usefixtures("restore_logging_state")
def test_json_renderer_handles_structlog_and_stdlib(
    capsys: pytest.CaptureFixture[str],
) -> None:
    setup_logging(
        LoggingConfig(
            renderer="json",
            enable_diagnostics=True,
            use_utc_timestamps=True,
        ),
    )

    structlog.get_logger("test.structured").info(
        "product_matched",
        product_id="sku-1",
    )
    logging.getLogger("test.foreign").warning("retry %s", "scheduled")
    structured, foreign = [
        json.loads(line) for line in capsys.readouterr().out.splitlines()
    ]

    assert structured["event"] == "product_matched"
    assert structured["product_id"] == "sku-1"
    assert structured["logger"] == "test.structured"
    assert structured["level"] == "info"
    assert structured["timestamp"].endswith("Z")
    assert {"module", "func_name", "lineno"} <= structured.keys()
    assert foreign["event"] == "retry scheduled"
    assert foreign["logger"] == "test.foreign"
    assert foreign["level"] == "warning"


@pytest.mark.unit
@pytest.mark.usefixtures("restore_logging_state")
def test_json_traceback_does_not_include_frame_locals(
    capsys: pytest.CaptureFixture[str],
) -> None:
    setup_logging(LoggingConfig(renderer="json"))
    logger = structlog.get_logger("test.exception")

    try:
        raise ValueError("broken")
    except ValueError:
        logger.exception("operation_failed")
    event = json.loads(capsys.readouterr().out)

    assert event["exception"][0]["exc_type"] == "ValueError"
    assert all(
        "locals" not in frame for frame in event["exception"][0]["frames"]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("restore_logging_state")
def test_level_filtering_and_noisy_logger_tuning(
    capsys: pytest.CaptureFixture[str],
) -> None:
    setup_logging(LoggingConfig(level="WARNING", renderer="console"))
    logger = structlog.get_logger("test.levels")

    logger.info("hidden_event")
    logger.warning("visible_event")
    output = capsys.readouterr().out

    assert "hidden_event" not in output
    assert "visible_event" in output
    assert logging.getLogger("httpx").level == logging.WARNING
