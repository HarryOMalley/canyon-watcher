from datetime import UTC, datetime, timedelta

import pytest

from src.domain.enums import StockState
from src.domain.models import StockObservation
from src.infrastructure.persistence.sqlite_repo import SQLiteObservationRepository


@pytest.fixture
def repo(tmp_path):
    db_path = tmp_path / "test.db"
    return SQLiteObservationRepository(db_path)


def test_sqlite_repo_save_and_get_latest(repo):
    obs = StockObservation(
        target_id="test-bike",
        timestamp=datetime.now(UTC),
        state=StockState.IN_STOCK,
        is_buyable=True,
        price="£2,999",
        availability_text="In stock",
    )

    repo.save(obs)
    latest = repo.get_latest("test-bike")

    assert latest is not None
    assert latest.target_id == obs.target_id
    assert latest.state == obs.state
    assert latest.is_buyable == obs.is_buyable
    assert latest.price == obs.price
    # Pydantic might lose some microsecond precision or use different ISO format
    # but datetime.fromisoformat should handle it.
    assert (
        abs((latest.timestamp - obs.timestamp).total_seconds()) < 1
    )  # Allow small diff due to string conversion


def test_sqlite_repo_get_latest_none(repo):
    assert repo.get_latest("non-existent") is None


def test_sqlite_repo_ordering(repo):
    now = datetime.now(UTC)
    obs1 = StockObservation(
        target_id="test-bike",
        timestamp=now - timedelta(minutes=10),
        state=StockState.UNAVAILABLE,
        is_buyable=False,
    )
    obs2 = StockObservation(
        target_id="test-bike",
        timestamp=now,
        state=StockState.IN_STOCK,
        is_buyable=True,
    )

    repo.save(obs1)
    repo.save(obs2)

    latest = repo.get_latest("test-bike")
    assert latest.state == StockState.IN_STOCK
