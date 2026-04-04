import json

import httpx
import pytest
import respx

from src.domain.enums import StockState
from src.domain.models import NotificationEvent
from src.infrastructure.notifiers.slack import SlackNotifier
from src.infrastructure.notifiers.telegram import TelegramNotifier


@pytest.mark.asyncio
async def test_telegram_notifier_send():
    bot_token = "fake-token"
    chat_id = "fake-chat"
    notifier = TelegramNotifier(bot_token, chat_id)

    event = NotificationEvent(
        target_id="test-bike",
        previous_state=StockState.UNAVAILABLE,
        current_state=StockState.IN_STOCK,
        message="Bike is in stock!",
        url="https://canyon.com/test",
    )

    async with respx.mock:
        route = respx.post(f"https://api.telegram.org/bot{bot_token}/sendMessage").mock(
            return_value=httpx.Response(200, json={"ok": True})
        )
        await notifier.send(event)
        assert route.called
        payload = json.loads(route.calls.last.request.content)
        assert payload["chat_id"] == chat_id


@pytest.mark.asyncio
async def test_slack_notifier_send():
    webhook_url = "https://hooks.slack.com/services/test"
    notifier = SlackNotifier(webhook_url)

    event = NotificationEvent(
        target_id="test-bike",
        previous_state=StockState.UNAVAILABLE,
        current_state=StockState.IN_STOCK,
        message="Bike is in stock!",
        url="https://canyon.com/test",
    )

    async with respx.mock:
        route = respx.post(webhook_url).mock(return_value=httpx.Response(200))
        await notifier.send(event)
        assert route.called
        payload = json.loads(route.calls.last.request.content)
        assert "test-bike" in payload["text"]
