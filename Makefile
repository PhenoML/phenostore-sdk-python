UV ?= uv

.PHONY: install generate check-generated test lint format build
install:
	$(UV) sync --locked

generate:
	$(UV) run --project tools --locked python tools/generate.py

check-generated:
	$(UV) run --project tools --locked python tools/generate.py --check

test:
	$(UV) run --locked pytest

lint:
	$(UV) run --locked ruff check .
	$(UV) run --locked ruff format --check .
	$(UV) run --locked mypy

format:
	$(UV) run --locked ruff check --fix .
	$(UV) run --locked ruff format .

build:
	$(UV) build
