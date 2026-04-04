from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .enums import StockState


class MonitorTarget(BaseModel):
    """Represents a product configuration to be monitored."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    url: str
    retailer: str = "canyon"
    enabled: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class StockObservation(BaseModel):
    """The result of a stock check for a specific target."""

    model_config = ConfigDict(frozen=True)

    target_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    state: StockState
    is_buyable: bool
    price: str | None = None
    availability_text: str | None = None
    config_match: bool = True


class NotificationEvent(BaseModel):
    """Represents a significant state transition that triggers a notification."""

    model_config = ConfigDict(frozen=True)

    target_id: str
    previous_state: StockState
    current_state: StockState
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    message: str
    url: str
