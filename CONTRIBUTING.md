# Contributing to Canyon Bike Stock Monitor

Welcome! This project uses a strictly multi-agent, parallelized workflow. To ensure our goals are met and code stays clean, all contributors (human or AI) must adhere to these guidelines.

## Agent Roles

When an agent is dispatched to work on this repository, it should be assigned a specific persona. These roles ensure separation of concerns:

1.  **The Orchestrator**: Maintains the `ROADMAP.md`, manages branches, coordinates merges, handles `git rebase`, and bumps versions using `git-cliff`.
2.  **The Implementer**: Writes application code, unit tests, and commits using Conventional Commits. Does not touch architecture unless specified.
3.  **The Reviewer**: Acts as the gatekeeper for Pull Requests. Reviews code diffs against the ROADMAP and spec, enforcing SOLID principles and test coverage. Simulates the "Codex" pipeline review.
4.  **The Documenter**: Ensures `README.md`, inline code docs, and API specifications remain up to date with the evolving codebase.

## Workflow Rules

This project follows **GitHub Flow**.

1.  **Never Push Directly to `main`**: All work must happen on a short-lived feature branch. The branch naming strategy is simple: `branch-name` (e.g., `domain-protocols`, `canyon-retailer`). Do not use prefixes like `feat/` or `fix/`.
2.  **Conventional Commits**: Every commit MUST follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.
    *   *Good*: `feat: implement Canyon parser`
    *   *Bad*: `added parser`
3.  **Test-Driven Development**: Every new feature must be accompanied by a unit test. Mock external dependencies (like HTTP requests or SQLite connections).
4.  **Linting**: The codebase uses `ruff`. All Python code must be formatted and linted before opening a PR.
5.  **Pre-commit Hooks**: We use `pre-commit` to automate local quality checks. Run `pre-commit install` and `pre-commit install --hook-type commit-msg` to set them up. This validates conventional commits, detects secrets, and runs linting.
6.  **Rebasing & Merging**: Before a branch is merged into `main`, it must be rebased against the latest `main`. Pull Requests are the primary mechanism for review and merging.

## CI/CD Pipeline

The GitHub Actions pipeline `.github/workflows/ci.yml` will enforce these rules automatically:
-   **Linting**: Runs `ruff check .` and `ruff format --check .`
-   **Testing**: Runs `pytest`.
-   **CommitLint**: Validates commit messages.
-   **Release**: On merge to main, `git-cliff` will bump the semantic version (e.g., from v0.1.0 to v0.2.0) and generate the `CHANGELOG.md`.

Thank you for contributing!
