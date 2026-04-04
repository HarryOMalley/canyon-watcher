import httpx

from application.ports.notifier import Notifier
from domain.models import NotificationEvent


class SlackNotifier(Notifier):
    """Sends notifications via Slack Webhooks."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def send(self, event: NotificationEvent) -> None:
        async with httpx.AsyncClient(timeout=10.0) as client:
            payload = {
                "text": f"Stock Alert: {event.target_id}",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": (
                                f"🔔 *Stock Alert for {event.target_id}*\n\n"
                                f"{event.message}"
                            ),
                        },
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": (
                                    f"*Previous State:*\n{event.previous_state.value}"
                                ),
                            },
                            {
                                "type": "mrkdwn",
                                "text": (
                                    f"*Current State:*\n{event.current_state.value}"
                                ),
                            },
                        ],
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "View Product"},
                                "url": event.url,
                            }
                        ],
                    },
                ],
            }
            resp = await client.post(self.webhook_url, json=payload)
            resp.raise_for_status()
