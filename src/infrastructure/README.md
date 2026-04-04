# Infrastructure Layer

Concrete implementations for external dependencies and technologies.

## Retailer Implementations

- **`CanyonRetailer`**: Handles fetching and parsing of Canyon product pages.
  - **Fetcher**: Uses `httpx` to fetch HTML.
  - **Parser**: Uses `BeautifulSoup4` to extract signals like price, stock text, and configuration matching.
  - **Classifier**: Rules to map signals to `StockState` (e.g., "In stock" -> `IN_STOCK`).

## Persistence

- **`SQLiteObservationRepository`**: Implements the `ObservationRepository` using SQLite.
  - Keeps a history of observations for trend analysis and debugging.
  - Stores deduplication keys for notifications.

## Notifiers

- **`TelegramNotifier`**: Sends notifications via the Telegram Bot API.
- **`SlackNotifier`**: Sends notifications via incoming webhooks.

## Configuration

- **`TOMLConfigLoader`**: Reads the `config.toml` file into Pydantic models for validation and type safety.
