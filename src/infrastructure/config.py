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
    """Load settings from a TOML file."""
    p = Path(path)
    if not p.exists():
        return Settings()

    with open(p, "rb") as f:
        data = tomllib.load(f)

    return Settings.model_validate(data)
