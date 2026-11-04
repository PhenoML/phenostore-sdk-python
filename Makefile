UV ?= uv
GENERATOR_VERSION ?= latest
export GENERATOR_VERSION

.PHONY: install generate update-generator check-generated test lint format build
install:
	$(UV) sync --locked

generate:
	$(UV) run --project tools --locked python tools/generate.py

# Remove existing exact pins so uv can select and pin the requested releases.
# Keep generator/formatter pins and regenerated output in the same change.
update-generator:
	$(UV) remove --project tools --frozen openapi-python-client ruff
	@set -eu; \
	generator=openapi-python-client; \
	if [ "$$GENERATOR_VERSION" != latest ]; then \
		generator="openapi-python-client==$$GENERATOR_VERSION"; \
	fi; \
	$(UV) add --project tools --bounds exact --upgrade "$$generator" ruff
	$(MAKE) generate test lint check-generated build

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
