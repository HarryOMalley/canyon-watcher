import pytest

from infrastructure.config import load_settings


def test_load_settings_defaults(tmp_path):
    config_path = tmp_path / "config.toml"
    # No file exists.
    # We expect it to be created.
    settings = load_settings(config_path)
    assert settings.app.poll_interval_seconds == 900
    # If config.toml.example exists, it will have targets.
    # Otherwise it will be empty.
    assert config_path.exists()


def test_load_settings_from_file(tmp_path):
    config_path = tmp_path / "config.toml"
    config_path.write_text("""
[app]
poll_interval_seconds = 60

[[targets]]
id = "test-bike"
name = "Test Bike"
url = "https://canyon.com/test"

[notifications.telegram]
enabled = true
bot_token = "token"
chat_id = "chat"
""")
    settings = load_settings(config_path)
    assert settings.app.poll_interval_seconds == 60
    assert len(settings.targets) == 1
    assert settings.targets[0].id == "test-bike"
    assert settings.notifications.telegram.enabled is True
    assert settings.notifications.telegram.bot_token == "token"


def test_load_settings_validation_error(tmp_path):
    config_path = tmp_path / "config.toml"
    # Telegram enabled but missing tokens
    config_path.write_text("""
[notifications.telegram]
enabled = true
""")
    from pydantic import ValidationError

    with pytest.raises(ValidationError) as excinfo:
        load_settings(config_path)

    assert "bot_token and chat_id are required" in str(excinfo.value)


def test_load_settings_storage_section(tmp_path):
    config_path = tmp_path / "config.toml"
    config_path.write_text("""
[storage]
sqlite_path = "custom/path.db"
""")
    settings = load_settings(config_path)
    assert settings.sqlite_path == "custom/path.db"
    assert settings.storage.sqlite_path == "custom/path.db"
