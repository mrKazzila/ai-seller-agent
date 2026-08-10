from pathlib import Path

import pytest

from ai_seller_agent.config.settings import Settings
from ai_seller_agent.config.settings._base_settings import PROJECT_ROOT


@pytest.mark.unit
def test_settings_load_nested_values_from_env_file(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        (
            'AI_SELLER_APP__NAME="Configured Agent"\n'
            'AI_SELLER_APP__HOST="0.0.0.0"\n'
            "AI_SELLER_APP__PORT=9000\n"
            'AI_SELLER_APP__CATALOG_PATH="fixtures/catalog.csv"\n'
            "AI_SELLER_MATCHING__MATCH_THRESHOLD=0.91\n"
        ),
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.app.name == "Configured Agent"
    assert settings.app.host == "0.0.0.0"
    assert settings.app.port == 9000
    assert settings.app.catalog_path == PROJECT_ROOT / "fixtures/catalog.csv"
    assert settings.matching.match_threshold == 0.91


@pytest.mark.unit
def test_environment_takes_precedence_over_env_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("AI_SELLER_APP__PORT=9000\n", encoding="utf-8")
    monkeypatch.setenv("AI_SELLER_APP__PORT", "7000")

    settings = Settings(_env_file=env_file)

    assert settings.app.port == 7000


@pytest.mark.unit
def test_default_catalog_path_is_absolute() -> None:
    settings = Settings(_env_file=None)

    assert settings.app.catalog_path == (
        PROJECT_ROOT / "data" / "catalog_excel.csv"
    )
