.PHONY: default help clean-project init clean-env sync format lint type-check test test-unit test-functional test-integration test-all validate-branch

GREEN_LINE=@echo "\033[0;32m--------------------------------------------------\033[0m"

SOURCE_DIR = src/
TEST_DIR = tests/
PROJECT_VERSION := $(shell awk '/^\[project\]/ {flag=1; next} /^\[/{flag=0} flag && /^version/ {gsub(/"/, "", $$2); print $$2}' pyproject.toml)
PYTHON_VERSION := 3.12

default: help

help: ## Display this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-35s\033[0m %s\n", $$1, $$2}'

# ----------------------------
# Environment Management
# ----------------------------

init: ## Set up Python version, venv, and install dependencies
	@echo "🔧 Installing uv if missing..."
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "📦 Installing uv..."; \
		python3 -m pip install --user --upgrade uv; \
	else \
		echo "✅ uv is already installed"; \
	fi
	@echo "🐍 Setting up Python $(PYTHON_VERSION) environment..."
	uv python install $(PYTHON_VERSION)
	uv venv --python $(PYTHON_VERSION) .venv
	@echo "📦 Installing project dependencies..."
	uv sync --extra dev
	. .venv/bin/activate && uv pip install -e .
	@echo "🔗 Setting up pre-commit hooks..."
	@if [ -f .pre-commit-config.yaml ]; then \
		uv run pre-commit install; \
		echo "✅ Pre-commit hooks installed"; \
	else \
		echo "⚠️  No .pre-commit-config.yaml found, skipping pre-commit setup"; \
	fi
	@echo "🎉 Environment setup complete!"

clean-project: ## Clean Python caches and tooling artifacts
	@echo "Cleaning project caches..."
	find . -type d \( -name '.pytest_cache' -o -name '.ruff_cache' -o -name '.mypy_cache' -o -name '__pycache__' \) -exec rm -rf {} +
	$(GREEN_LINE)

clean-env: ## Remove the virtual environment folder
	@echo "Deleting virtual environment..."
	rm -rf .venv
	$(GREEN_LINE)

sync: ## Sync project dependencies
	@echo "Syncing project dependencies..."
	uv sync --extra dev
	$(GREEN_LINE)

# ----------------------------
# Code Quality
# ----------------------------

format: ## Format codebase using ruff
	@echo "Formatting code with ruff..."
	uv run ruff format
	$(GREEN_LINE)

lint: ## Lint code using ruff and autofix issues
	@echo "Running lint checks with ruff..."
	uv run ruff check . --fix
	$(GREEN_LINE)

type-check: ## Perform static type checks using mypy
	@echo "Running type checks with mypy..."
	uv run --extra dev mypy $(SOURCE_DIR)
	$(GREEN_LINE)

# ----------------------------
# Tests
# ----------------------------

test-unit: ## Run unit tests with pytest
	@echo "Running UNIT tests with pytest..."
	uv run python -m pytest -vv --verbose -s $(TEST_DIR)
	$(GREEN_LINE)

test-functional: ## Run functional tests with pytest
	@echo "Running FUNCTIONAL tests with pytest..."
	uv run python -m pytest -m functional -vv --verbose -s $(TEST_DIR)
	$(GREEN_LINE)

test-integration: ## Run integration tests with pytest
	@echo "Running INTEGRATION tests with pytest..."
	uv run python -m pytest -m integration -vv --verbose -s $(TEST_DIR)
	$(GREEN_LINE)

test: ## Run standard tests with coverage report (excludes integration)
	@echo "Running tests with pytest..."
	uv run python -m pytest -m "not integration" -vv -s $(TEST_DIR) \
		--cov=src \
		--cov-config=pyproject.toml \
		--cov-fail-under=80 \
		--cov-report=term-missing
	$(GREEN_LINE)

test-all: ## Run all tests including integration tests
	@echo "Running ALL tests with pytest..."
	uv run python -m pytest -vv -s $(TEST_DIR) \
		--cov=src \
		--cov-config=pyproject.toml \
		--cov-fail-under=80 \
		--cov-report=term-missing
	$(GREEN_LINE)

# ----------------------------
# Branch Validation
# ----------------------------

validate-branch: ## Run formatting, linting, type checks, and tests
	@echo "🔍 Running branch validation..."
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) test
	@echo "🎉 Branch validation successful - ready for PR!"
	$(GREEN_LINE)

