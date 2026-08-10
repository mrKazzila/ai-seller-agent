from pathlib import Path

import pytest

from ai_seller_agent.config.settings import Settings


@pytest.mark.unit
def test_settings_load_default_env_file_from_working_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    env_directory = tmp_path / "env"
    env_directory.mkdir()
    (env_directory / ".env").write_text(
        "AI_SELLER_APP__PORT=9000\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    settings = Settings()

    assert settings.app.port == 9000


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
    assert settings.app.catalog_path == Path.cwd() / "fixtures/catalog.csv"
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
def test_default_catalog_path_uses_working_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    settings = Settings(_env_file=None)

    assert settings.app.catalog_path == tmp_path / "data/catalog_excel.csv"


@pytest.mark.unit
def test_absolute_catalog_path_is_unchanged(tmp_path: Path) -> None:
    catalog_path = tmp_path / "catalog.csv"

    settings = Settings(
        _env_file=None,
        app={"catalog_path": catalog_path},
    )

    assert settings.app.catalog_path == catalog_path


@pytest.mark.unit
def test_settings_load_reload_from_env_file(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "AI_SELLER_APP__RELOAD=true\n",
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.app.reload is True
