import pathlib

import httpx
import pytest
import respx

from domain.enums import StockState
from domain.models import MonitorTarget
from infrastructure.retailers.canyon.retailer import CanyonRetailer

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text()


@pytest.mark.asyncio
async def test_canyon_retailer_in_stock():
    html = load_fixture("in_stock.html")
    target = MonitorTarget(id="test", name="test", url="https://canyon.com/test")

    async with respx.mock:
        respx.get("https://canyon.com/test").mock(
            return_value=httpx.Response(200, text=html)
        )
        retailer = CanyonRetailer()
        obs = await retailer.check_stock(target)

        assert obs.state == StockState.IN_STOCK
        assert obs.is_buyable is True
        assert obs.price == "£2,999.00"
        assert obs.availability_text == "In stock"


@pytest.mark.asyncio
async def test_canyon_retailer_coming_soon():
    html = load_fixture("coming_soon.html")
    target = MonitorTarget(id="test", name="test", url="https://canyon.com/test")

    async with respx.mock:
        respx.get("https://canyon.com/test").mock(
            return_value=httpx.Response(200, text=html)
        )
        retailer = CanyonRetailer()
        obs = await retailer.check_stock(target)

        assert obs.state == StockState.COMING_SOON
        assert obs.is_buyable is False
        assert obs.availability_text == "Coming soon"


@pytest.mark.asyncio
async def test_canyon_retailer_notify_me():
    html = load_fixture("notify_me.html")
    target = MonitorTarget(id="test", name="test", url="https://canyon.com/test")

    async with respx.mock:
        respx.get("https://canyon.com/test").mock(
            return_value=httpx.Response(200, text=html)
        )
        retailer = CanyonRetailer()
        obs = await retailer.check_stock(target)

        assert obs.state == StockState.NOTIFY_ME
        assert obs.is_buyable is False
        assert obs.availability_text == "Notify me"


@pytest.mark.asyncio
async def test_canyon_retailer_fetch_failed():
    target = MonitorTarget(id="test", name="test", url="https://canyon.com/test")

    async with respx.mock:
        respx.get("https://canyon.com/test").mock(return_value=httpx.Response(404))
        retailer = CanyonRetailer()
        obs = await retailer.check_stock(target)

        assert obs.state == StockState.FETCH_FAILED
        assert obs.is_buyable is False
