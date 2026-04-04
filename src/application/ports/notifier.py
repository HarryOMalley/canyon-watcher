from typing import Protocol

from src.domain.models import NotificationEvent


class Notifier(Protocol):
    """Protocol for sending notifications."""

    async def send(self, event: NotificationEvent) -> None:
        """Send a notification for a specific event."""
        ...
