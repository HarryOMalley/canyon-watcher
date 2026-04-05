import tomllib
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from domain.models import MonitorTarget


class AppConfig(BaseModel):
    poll_interval_seconds: int = 900
    request_timeout_seconds: int = 20
    user_agent: str = "Mozilla/5.0 (CanyonStockMonitor/1.0)"


class TelegramConfig(BaseModel):
    enabled: bool = False
    bot_token: str | None = None
    chat_id: str | None = None


class SlackConfig(BaseModel):
    enabled: bool = False
    webhook_url: str | None = None


class NotificationConfig(BaseModel):
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    slack: SlackConfig = Field(default_factory=SlackConfig)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_ignore_extra=True,
        env_nested_delimiter="__",
    )

    app: AppConfig = Field(default_factory=AppConfig)
    targets: list[MonitorTarget] = Field(default_factory=list)
    notifications: NotificationConfig = Field(default_factory=NotificationConfig)
    sqlite_path: str = "data/monitor.db"


def load_settings(path: str | Path) -> Settings:
    """Load settings from a TOML file. Creates a default file if it doesn't exist."""
    p = Path(path)
    if not p.exists():
        settings = Settings()
        # Ensure parent directory exists
        p.parent.mkdir(parents=True, exist_ok=True)
        # We don't have a toml serializer easily available without extra deps,
        # but we can write a simple default or copy example if available.
        example = Path("config.toml.example")
        if example.exists():
            p.write_text(example.read_text())
        else:
            # Minimal default
            p.write_text("[app]\npoll_interval_seconds = 900\n")
        return settings

    with open(p, "rb") as f:
        data = tomllib.load(f)

    return Settings.model_validate(data)
