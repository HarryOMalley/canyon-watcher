from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from src.domain.enums import StockState
from src.domain.models import MonitorTarget, StockObservation


def test_monitor_target_creation():
    target = MonitorTarget(
        id="test-id",
        name="Test Bike",
        url="https://example.com/bike",
        metadata={"size": "M"},
    )
    assert target.id == "test-id"
    assert target.retailer == "canyon"
    assert target.metadata["size"] == "M"


def test_monitor_target_frozen():
    target = MonitorTarget(id="test", name="test", url="test")
    with pytest.raises(ValidationError):
        target.id = "new-id"  # type: ignore


def test_stock_observation_creation():
    now = datetime.now(UTC)
    obs = StockObservation(
        target_id="test-id",
        timestamp=now,
        state=StockState.IN_STOCK,
        is_buyable=True,
        price="£2,999",
    )
    assert obs.target_id == "test-id"
    assert obs.state == StockState.IN_STOCK
    assert obs.is_buyable is True
    assert obs.price == "£2,999"
