# Domain Layer

The core business logic and entities. This layer is completely isolated from HTTP clients, databases, and third-party libraries.

## Core Entities

- **`MonitorTarget`**: Represents a product to be tracked (ID, Name, URL, Retailer Type).
- **`StockObservation`**: A single result from a check (State, Price, Timestamp, Buyable Flag).
- **`StockState`**: An Enum capturing normalized availability (e.g., `IN_STOCK`, `LOW_STOCK`, `COMING_SOON`).
- **`NotificationEvent`**: A change in state that triggers a notification (Previous State -> New State).

## Notification Transition Rules

To avoid spam, notifications are only sent when a transition is "interesting":

- **`UNAVAILABLE` -> `BUYABLE`** (Most important)
- **`COMING_SOON` -> `BUYABLE`**
- **`NOTIFY_ME` -> `BUYABLE`**
- **Any state -> `LOW_STOCK`**
- **`CONFIG_MISMATCH` -> `IN_STOCK`** (Once the bike is correctly back on sale)
- **`BLOCKED/FETCH_FAILED` -> `BUYABLE`** (Recovery)

"Buyable" is any state where `is_buyable` is `true` (e.g., `IN_STOCK`, `LOW_STOCK`).

## Retailer Abstraction

Each retailer must implement a `Retailer` interface:

1.  **`fetch()`**: Fetches raw data (usually HTML) from the product URL.
2.  **`parse()`**: Extracts signals from the raw data.
3.  **`classify()`**: Maps raw signals to the normalized `StockState`.

This ensures the `MonitorEngine` only speaks the language of `StockState`, and doesn't care if a bike is from Canyon or Specialized.
