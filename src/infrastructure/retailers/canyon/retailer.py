import logging

import httpx

from src.application.ports.repository import Retailer
from src.domain.enums import StockState
from src.domain.models import MonitorTarget, StockObservation

logger = logging.getLogger(__name__)


class CanyonRetailer(Retailer):
    """Fetcher and parser for Canyon bike product pages."""

    def __init__(self, client: httpx.AsyncClient | None = None):
        self.client = client or httpx.AsyncClient(
            timeout=10.0,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
        )

    async def check_stock(self, target: MonitorTarget) -> StockObservation:
        """Fetch the product page and return a normalized observation."""
        # Implementation to be added in next steps
        return StockObservation(
            target_id=target.id,
            state=StockState.UNKNOWN,
            is_buyable=False,
        )
