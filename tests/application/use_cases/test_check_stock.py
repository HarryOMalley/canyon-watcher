from unittest.mock import AsyncMock, MagicMock

import pytest

from application.use_cases.check_stock import CheckStockUseCase
from domain.enums import StockState
from domain.models import MonitorTarget, StockObservation


@pytest.fixture
def mock_retailer():
    return MagicMock()


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def mock_notifier():
    notifier = MagicMock()
    notifier.send = AsyncMock()
    return notifier


@pytest.fixture
def target():
    return MonitorTarget(
        id="test-bike", name="Test Bike", url="https://canyon.com/test"
    )


@pytest.mark.asyncio
async def test_check_stock_notifies_when_becomes_buyable(
    mock_retailer, mock_repository, mock_notifier, target
):
    # Arrange
    obs = StockObservation(
        target_id="test-bike", state=StockState.IN_STOCK, is_buyable=True
    )
    mock_retailer.check_stock = AsyncMock(return_value=obs)
    mock_repository.get_latest.return_value = StockObservation(
        target_id="test-bike", state=StockState.UNAVAILABLE, is_buyable=False
    )

    use_case = CheckStockUseCase(mock_retailer, mock_repository, [mock_notifier])

    # Act
    await use_case.execute(target)

    # Assert
    assert mock_notifier.send.called
    assert mock_repository.save.called


@pytest.mark.asyncio
async def test_check_stock_does_not_notify_when_unchanged(
    mock_retailer, mock_repository, mock_notifier, target
):
    # Arrange
    obs = StockObservation(
        target_id="test-bike", state=StockState.IN_STOCK, is_buyable=True
    )
    mock_retailer.check_stock = AsyncMock(return_value=obs)
    mock_repository.get_latest.return_value = obs

    use_case = CheckStockUseCase(mock_retailer, mock_repository, [mock_notifier])

    # Act
    await use_case.execute(target)

    # Assert
    assert not mock_notifier.send.called
    assert mock_repository.save.called


@pytest.mark.asyncio
async def test_check_stock_notifies_on_first_buyable(
    mock_retailer, mock_repository, mock_notifier, target
):
    # Arrange
    obs = StockObservation(
        target_id="test-bike", state=StockState.IN_STOCK, is_buyable=True
    )
    mock_retailer.check_stock = AsyncMock(return_value=obs)
    mock_repository.get_latest.return_value = None

    use_case = CheckStockUseCase(mock_retailer, mock_repository, [mock_notifier])

    # Act
    await use_case.execute(target)

    # Assert
    assert mock_notifier.send.called
