import httpx

from application.ports.notifier import Notifier
from domain.models import NotificationEvent


class TelegramNotifier(Notifier):
    """Sends notifications via Telegram Bot API."""

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    async def send(self, event: NotificationEvent) -> None:
        async with httpx.AsyncClient(timeout=10.0) as client:
            payload = {
                "chat_id": self.chat_id,
                "text": self._format_message(event),
                "parse_mode": "Markdown",
            }
            resp = await client.post(self.url, json=payload)
            resp.raise_for_status()

    def _format_message(self, event: NotificationEvent) -> str:
        return (
            f"🔔 *Stock Alert for {event.target_id}*\n\n"
            f"{event.message}\n\n"
            f"*Status:* {event.previous_state.value} ➡️ {event.current_state.value}\n"
            f"[View Product]({event.url})"
        )
