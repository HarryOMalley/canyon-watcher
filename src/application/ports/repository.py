from typing import Protocol

from domain.models import StockObservation


class ObservationRepository(Protocol):
    """Protocol for persisting and retrieving stock observations."""

    def get_latest(self, target_id: str) -> StockObservation | None:
        """Retrieve the most recent observation for a target."""
        ...

    def save(self, observation: StockObservation) -> None:
        """Persist a new observation."""
        ...
