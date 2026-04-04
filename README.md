# Canyon Bike Stock Monitor

A lightweight, self-hostable service for monitoring Canyon bike stock availability. Built with SOLID principles, abstract retailer logic, and Kubernetes-readiness.

## Project Structure

- `src/domain/`: Core business logic, entities, and `Retailer` abstractions.
- `src/application/`: Orchestrates use cases and maps domain logic to ports.
- `src/infrastructure/`: Concrete implementations (HTTP fetchers, HTML parsers, SQLite, Notifiers).
- `src/interface/`: Entrypoints like the FastAPI web server and APScheduler loop.

## Design Principles

- **Abstract Retailers**: The monitor is retailer-agnostic. New retailers (e.g., Specialized, Rose) can be added as modules without touching the core engine.
- **SQLite Persistence**: Stores a history of observations for trend analysis and notification deduplication.
- **TOML Configuration**: Uses a declarative `config.toml` as the immutable source of truth for monitor targets.
- **Observability**: Built-in Prometheus metrics and structured JSON logging.

## Core Flow

1. **Load**: ConfigLoader reads `config.toml` targets.
2. **Schedule**: APScheduler triggers a stock check every X minutes.
3. **Fetch & Parse**: The appropriate Retailer (e.g., Canyon) fetches the page and parses signals.
4. **Classify**: Raw signals are mapped to a normalized `StockState`.
5. **Detect**: The engine compares the new state with the previous state from SQLite.
6. **Notify**: If a "buyable" transition is detected, notifications are sent via Telegram or Slack.
