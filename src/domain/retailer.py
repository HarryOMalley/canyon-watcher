from typing import Protocol, runtime_checkable

from .models import MonitorTarget, StockObservation


@runtime_checkable
class Retailer(Protocol):
    """Protocol for retailer-specific fetching and parsing logic."""

    async def check_stock(self, target: MonitorTarget) -> StockObservation:
        """Fetch the product page and return a normalized observation."""
        ...
