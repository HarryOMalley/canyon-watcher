# Application Layer

Coordinates use cases and orchestrates domain logic. This layer defines the ports (interfaces) that infrastructure must implement.

## Use Cases

- **`CheckTargetStock`**: Performs the full flow (Load target -> Fetch -> Parse -> Classify -> Compare with previous -> Save result -> Notify if changed).
- **`SyncMonitorTargets`**: Synchronizes the list of active targets from the TOML config.

## Ports (Interfaces)

The application layer defines these ports to be implemented in the infrastructure layer:

- **`ObservationRepository`**: Persists and retrieves `StockObservation` objects.
- **`Notifier`**: Interface for sending notifications (Telegram, Slack, etc.).
- **`RetailerFactory`**: Returns the appropriate `Retailer` implementation (e.g., `CanyonRetailer`).
- **`ConfigLoader`**: Loads settings from the `config.toml`.
