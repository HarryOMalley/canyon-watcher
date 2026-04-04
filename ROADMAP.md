# Canyon Bike Stock Monitor - Roadmap

**Goal:** Build a small, self-hostable service which monitors Canyon bike product pages and detects when stock becomes available. Reaching v1.0.0 upon full functional delivery.

**Workflow:**
- Feature Branching & PRs.
- Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`).
- CI/CD via GitHub Actions (Linting, Testing, CommitLint).
- Automated changelogs and versioning via `git-cliff`.
- AI-driven PR Code Reviews prior to merge.

---

## Phase 0: Project Foundation (The Orchestrator)

- [x] Initialize Git repository.
- [x] Create `README.md` (Project Goals) and `CONTRIBUTING.md` (Agent/Contributor Guidelines).
- [x] Create `pyproject.toml` (Dependencies, Linter configs like `ruff`).
- [x] Create `.github/workflows/ci.yml` (Lint, Test, Commit Linting, Versioning).
- [x] Initial commit to `main` branch.

## Phase 1: Core Domain & Protocols (The Implementer)

- [x] Create branch `domain-protocols`.
- [x] Define `StockState` Enum and `MonitorTarget` / `StockObservation` models.
- [x] Define Protocols (Interfaces): `Retailer`, `ObservationRepository`, `Notifier`.
- [x] Push, open PR, request `Reviewer Agent`.
- [x] Address review, merge to `main`, bump version (e.g., `v0.1.0`).

## Phase 2: Parallel Implementations (Multiple Implementer Agents)

This phase was executed via separate feature branches.

### Track A: Canyon Retailer
- [x] Create branch `canyon-retailer` (from `main`).
- [x] Implement `CanyonRetailer` (httpx & BS4).
- [x] Write unit tests and mock HTML fixtures.
- [x] Push, review, rebase, merge.

### Track B: SQLite Persistence
- [x] Create branch `sqlite-repo` (from `main`).
- [x] Implement `SQLiteObservationRepository`.
- [x] Write unit tests.
- [x] Push, review, rebase, merge.

### Track C: Notification Channels
- [x] Create branch `telegram-notifier` (from `main`).
- [x] Implement `TelegramNotifier` and `SlackNotifier`.
- [x] Write unit tests.
- [x] Push, review, rebase, merge.

## Phase 3: Orchestration & API (The Integrator)

- [x] Create branch `orchestration-api`.
- [x] Implement `CheckStockUseCase`.
- [x] Implement FastAPI endpoints & APScheduler loop.
- [x] Push, review, rebase, merge.

## Phase 4: Delivery (The Releaser)

- [x] Create branch `docker-delivery`.
- [x] Create `Dockerfile` and `docker-compose.yml`.
- [ ] Push, review, merge.
- [ ] Trigger final release to `v1.0.0`.
