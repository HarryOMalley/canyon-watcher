# Interface Layer

Entrypoints for the system.

## Web Server (FastAPI)

- Provides a REST API for monitoring current status and history.
- Health endpoints: `/health/live`, `/health/ready`.
- Observability: `/metrics` (Prometheus).

## Scheduler (APScheduler)

- Triggers the stock check use cases every X minutes.
- Uses the configured `poll_interval_seconds` from `config.toml`.

## Containerization

The interface layer is also responsible for running inside a Docker container, with structured JSON logging (e.g., `structlog`) to standard out for Kubernetes logs.
