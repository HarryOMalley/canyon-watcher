from src.infrastructure.config import load_settings


def test_load_settings_defaults(tmp_path):
    config_path = tmp_path / "config.toml"
    # No file exists
    settings = load_settings(config_path)
    assert settings.app.poll_interval_seconds == 900
    assert len(settings.targets) == 0


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
