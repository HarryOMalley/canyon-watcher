from typing import Sequence

from application.ports.notifier import Notifier
from application.ports.repository import ObservationRepository
from domain.enums import StockState
from domain.models import MonitorTarget, NotificationEvent, StockObservation
from domain.retailer import Retailer


class CheckStockUseCase:
    """Orchestrates the stock check process for a monitor target."""

    def __init__(
        self,
        retailer: Retailer,
        repository: ObservationRepository,
        notifiers: Sequence[Notifier],
    ):
        self.retailer = retailer
        self.repository = repository
        self.notifiers = notifiers

    async def execute(self, target: MonitorTarget) -> StockObservation:
        """Execute the stock check and send notifications if needed."""
        observation = await self.retailer.check_stock(target)
        previous_observation = self.repository.get_latest(target.id)

        if self._should_notify(previous_observation, observation):
            event = self._create_notification_event(
                target, previous_observation, observation
            )
            for notifier in self.notifiers:
                await notifier.send(event)

        self.repository.save(observation)
        return observation

    def _should_notify(
        self,
        previous: StockObservation | None,
        current: StockObservation,
    ) -> bool:
        """Determines if a state transition warrants a notification."""
        if not previous:
            # Notify on the very first successful buyable observation
            return current.is_buyable

        prev_state = previous.state
        curr_state = current.state

        # Transition to buyable from non-buyable/failed states
        if not previous.is_buyable and current.is_buyable:
            return True

        # Always notify if it becomes LOW_STOCK (unless it already was)
        if curr_state == StockState.LOW_STOCK and prev_state != StockState.LOW_STOCK:
            return True

        # Recovery from error/mismatch to in-stock
        if (
            prev_state
            in {StockState.CONFIG_MISMATCH, StockState.BLOCKED, StockState.FETCH_FAILED}
            and curr_state == StockState.IN_STOCK
        ):
            return True

        return False

    def _create_notification_event(
        self,
        target: MonitorTarget,
        previous: StockObservation | None,
        current: StockObservation,
    ) -> NotificationEvent:
        prev_state = previous.state if previous else StockState.UNKNOWN

        message = f"Stock status changed for {target.name}."
        if current.state == StockState.IN_STOCK:
            message = f"🚀 {target.name} is NOW IN STOCK!"
        elif current.state == StockState.LOW_STOCK:
            message = f"⚠️ {target.name} has LOW STOCK remaining!"
        elif current.is_buyable:
            message = f"✅ {target.name} is now buyable!"

        return NotificationEvent(
            target_id=target.id,
            previous_state=prev_state,
            current_state=current.state,
            message=message,
            url=target.url,
        )
