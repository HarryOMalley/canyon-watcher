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

- [ ] Initialize Git repository.
- [ ] Create `README.md` (Project Goals) and `CONTRIBUTING.md` (Agent/Contributor Guidelines).
- [ ] Create `pyproject.toml` (Dependencies, Linter configs like `ruff`).
- [ ] Create `.github/workflows/ci.yml` (Lint, Test, Commit Linting, Versioning).
- [ ] Initial commit to `main` branch.

## Phase 1: Core Domain & Protocols (The Implementer)

- [ ] Create branch `domain-protocols`.
- [ ] Define `StockState` Enum and `MonitorTarget` / `StockObservation` models.
- [ ] Define Protocols (Interfaces): `Retailer`, `ObservationRepository`, `Notifier`.
- [ ] Push, open PR, request `Reviewer Agent`.
- [ ] Address review, merge to `main`, bump version (e.g., `v0.1.0`).

## Phase 2: Parallel Implementations (Multiple Implementer Agents)

This phase will be executed via separate feature branches. As each merges, subsequent branches must rebase against `main`.

### Track A: Canyon Retailer
- [ ] Create branch `canyon-retailer` (from `main`).
- [ ] Implement `CanyonFetcher` (httpx) & `CanyonParser` (BS4/html logic).
- [ ] Write unit tests and mock HTML fixtures.
- [ ] Push, review, rebase, merge.

### Track B: SQLite Persistence
- [ ] Create branch `sqlite-repo` (from `main`).
- [ ] Implement `SQLiteObservationRepository` (init, save, get_latest).
- [ ] Write unit tests.
- [ ] Push, review, rebase, merge.

### Track C: Notification Channels
- [ ] Create branch `telegram-notifier` (from `main`).
- [ ] Implement `TelegramNotifier` and `SlackNotifier`.
- [ ] Write unit tests.
- [ ] Push, review, rebase, merge.

## Phase 3: Orchestration & API (The Integrator)

- [ ] Create branch `orchestration-api`.
- [ ] Implement `CheckStockUseCase` (coordinates Fetcher -> Repo -> Notifier).
- [ ] Implement FastAPI endpoints (`/health/live`, `/metrics`, etc.) & APScheduler loop.
- [ ] Push, review, rebase, merge.

## Phase 4: Delivery (The Releaser)

- [ ] Create branch `docker-delivery`.
- [ ] Create `Dockerfile` and `docker-compose.yml`.
- [ ] Push, review, merge.
- [ ] Trigger final release to `v1.0.0`.
