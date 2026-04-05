import tomllib
from pathlib import Path
from typing import Self

from pydantic import BaseModel, Field, model_validator
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

    @model_validator(mode="after")
    def validate_telegram(self) -> Self:
        if self.enabled:
            if not self.bot_token or not self.chat_id:
                raise ValueError(
                    "bot_token and chat_id are required when telegram is enabled"
                )
        return self


class SlackConfig(BaseModel):
    enabled: bool = False
    webhook_url: str | None = None

    @model_validator(mode="after")
    def validate_slack(self) -> Self:
        if self.enabled and not self.webhook_url:
            raise ValueError("webhook_url is required when slack is enabled")
        return self


class DiscordConfig(BaseModel):
    enabled: bool = False
    webhook_url: str | None = None

    @model_validator(mode="after")
    def validate_discord(self) -> Self:
        if self.enabled and not self.webhook_url:
            raise ValueError("webhook_url is required when discord is enabled")
        return self


class NotificationConfig(BaseModel):
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    slack: SlackConfig = Field(default_factory=SlackConfig)
    discord: DiscordConfig = Field(default_factory=DiscordConfig)


class StorageConfig(BaseModel):
    sqlite_path: str = "data/monitor.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_ignore_extra=True,
        env_nested_delimiter="__",
    )

    app: AppConfig = Field(default_factory=AppConfig)
    targets: list[MonitorTarget] = Field(default_factory=list)
    notifications: NotificationConfig = Field(default_factory=NotificationConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)

    @property
    def sqlite_path(self) -> str:
        return self.storage.sqlite_path


def load_settings(path: str | Path) -> Settings:
    """Load settings from a TOML file. Creates a default file if it doesn't exist."""
    p = Path(path)
    if not p.exists():
        # Ensure parent directory exists
        p.parent.mkdir(parents=True, exist_ok=True)
        # We don't have a toml serializer easily available without extra deps,
        # but we can copy the example if available.
        example = Path("config.toml.example")
        if example.exists():
            p.write_text(example.read_text())
        else:
            # Minimal default
            p.write_text(
                "[app]\npoll_interval_seconds = 900\n\n"
                '[storage]\nsqlite_path = "data/monitor.db"\n'
            )

        # Reload after creating

        if not p.exists():
            return Settings()

    with open(p, "rb") as f:
        data = tomllib.load(f)

    return Settings.model_validate(data)
