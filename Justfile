set shell := ["bash", "-c"]

# Install all tools and dependencies
install:
    pip install --upgrade pip
    pip install -e ".[dev]"
    pre-commit install
    pre-commit install --hook-type commit-msg

# Run linting and formatting
lint:
    ruff check .
    ruff format .

# Run all tests
test:
    pytest tests/

# Validate commit messages (checks latest commit against main)
check-commits:
    @git rev-parse HEAD~1 > /dev/null 2>&1 && commitlint --from=HEAD~1 --to=HEAD --verbose || echo "Skipping commitlint on root commit"


# Run all CI checks locally
ci: lint test check-commits

# Run the application
run:
    python src/main.py

# Create a new version and changelog
release:
    git-cliff --bump -o CHANGELOG.md
