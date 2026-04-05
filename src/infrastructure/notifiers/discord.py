import httpx

from application.ports.notifier import Notifier
from domain.models import NotificationEvent


class DiscordNotifier(Notifier):
    """Sends notifications via Discord Webhook API."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def send(self, event: NotificationEvent) -> None:
        async with httpx.AsyncClient(timeout=10.0) as client:
            payload = {
                "content": self._format_message(event),
            }
            resp = await client.post(self.webhook_url, json=payload)
            resp.raise_for_status()

    def _format_message(self, event: NotificationEvent) -> str:
        return (
            f"🔔 **Stock Alert for {event.target_id}**\n\n"
            f"{event.message}\n\n"
            f"**Status:** `{event.previous_state.value}` ➡️ "
            f"`{event.current_state.value}`\n"
            f"[View Product](<{event.url}>)"
        )
