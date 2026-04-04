import logging

import httpx
from bs4 import BeautifulSoup

from src.domain.enums import StockState
from src.domain.models import MonitorTarget, StockObservation
from src.domain.retailer import Retailer

logger = logging.getLogger(__name__)


class CanyonRetailer(Retailer):
    """Fetcher and parser for Canyon bike product pages."""

    def __init__(self, client: httpx.AsyncClient | None = None):
        self._client = client

    async def check_stock(self, target: MonitorTarget) -> StockObservation:
        """Fetch the product page and return a normalized observation."""
        try:
            html = await self._fetch(target.url)
            return self._parse(html, target)
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch {target.url}: {e}")
            return StockObservation(
                target_id=target.id,
                state=StockState.FETCH_FAILED,
                is_buyable=False,
                availability_text=str(e),
            )
        except Exception as e:
            logger.exception(f"Unexpected error checking {target.id}: {e}")
            return StockObservation(
                target_id=target.id,
                state=StockState.PARSE_FAILED,
                is_buyable=False,
                availability_text=str(e),
            )

    async def _fetch(self, url: str) -> str:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        if self._client:
            resp = await self._client.get(url, headers=headers, follow_redirects=True)
            resp.raise_for_status()
            return resp.text

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, headers=headers, follow_redirects=True)
            resp.raise_for_status()
            return resp.text

    def _parse(self, html: str, target: MonitorTarget) -> StockObservation:
        soup = BeautifulSoup(html, "html.parser")

        # Basic signal extraction (simplified for initial implementation)
        price = self._extract_price(soup)
        availability_text = self._extract_availability_text(soup)
        is_buyable_signal = self._detect_buyable(soup)

        state = self._classify(soup, availability_text, is_buyable_signal)

        return StockObservation(
            target_id=target.id,
            state=state,
            is_buyable=state in {StockState.IN_STOCK, StockState.LOW_STOCK},
            price=price,
            availability_text=availability_text,
        )

    def _extract_price(self, soup: BeautifulSoup) -> str | None:
        price_tag = soup.find(class_="product-price")
        return price_tag.get_text(strip=True) if price_tag else None

    def _extract_availability_text(self, soup: BeautifulSoup) -> str | None:
        avail_tag = soup.find(class_="availability-text")
        return avail_tag.get_text(strip=True) if avail_tag else None

    def _detect_buyable(self, soup: BeautifulSoup) -> bool:
        return soup.find(class_="add-to-cart") is not None

    def _classify(
        self, soup: BeautifulSoup, availability_text: str | None, is_buyable: bool
    ) -> StockState:
        if is_buyable:
            return StockState.IN_STOCK

        if availability_text:
            text = availability_text.lower()
            if "coming soon" in text:
                return StockState.COMING_SOON
            if "notify me" in text:
                return StockState.NOTIFY_ME
            if "low stock" in text:
                return StockState.LOW_STOCK

        if soup.find(class_="notify-me"):
            return StockState.NOTIFY_ME

        return StockState.UNAVAILABLE
