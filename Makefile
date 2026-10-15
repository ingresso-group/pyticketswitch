VENV := venv
BIN := ./$(VENV)/bin
PYTHON ?= python3

.DEFAULT_GOAL := help
.PHONY: help init clean lint format format-check typecheck check test unit behave coverage docs publish

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

init:  ## Create the virtualenv and install dependencies
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements/test.txt
	$(BIN)/pip install -r requirements/docs.txt
	$(BIN)/pip install -e .

clean:  ## Remove the virtualenv and build/test artefacts
	rm -rf ./$(VENV) fixtures/cassettes *.egg-info .cache .coverage .coverage.* .pytest_cache .ruff_cache build dist
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +

lint:  ## Lint with ruff
	$(BIN)/ruff check pyticketswitch tests

format:  ## Auto-fix lint issues and format with ruff
	$(BIN)/ruff check --fix pyticketswitch tests
	$(BIN)/ruff format pyticketswitch tests

format-check:  ## Check formatting without changing files
	$(BIN)/ruff format --check pyticketswitch tests

typecheck:  ## Type check with pyright
	$(BIN)/pyright

check: lint format-check typecheck  ## Run all static checks

unit:  ## Run unit tests
	$(BIN)/python -m pytest tests

behave:  ## Run behave acceptance tests
	$(BIN)/behave --no-capture --no-color --format progress2 --tags=-skip

test: check unit behave  ## Static checks plus unit and acceptance tests

coverage:  ## Run unit and behave tests with a coverage report
	$(BIN)/coverage run -m pytest tests
	$(BIN)/coverage run -m behave --no-capture --no-color --format progress2 --junit --tags=-skip
	$(BIN)/coverage combine
	$(BIN)/coverage report --show-missing

docs:  ## Build the HTML docs
	cd docs && $(MAKE) html
	@echo "Build successful! View the docs homepage at docs/_build/html/index.html."

publish:  ## Build and upload a release to PyPI
	$(BIN)/pip install build twine
	$(BIN)/python -m build
	$(BIN)/twine upload dist/*
