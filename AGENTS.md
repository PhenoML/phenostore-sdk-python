# Agent guidelines

- `api/openapi.yaml` is imported from upstream. Do not edit it by hand; update the API contract upstream.
- `phenostore/gen/` is generated. Change the generator configuration or tooling, then run `make generate`.
- Keep generator dependencies isolated in `tools/`; runtime dependencies belong in the root `pyproject.toml`.
- The handwritten wrapper intentionally uses the pinned generator's request builders so it can retain raw FHIR responses, normalize errors, and accept arbitrary search parameters. Run contract tests when upgrading the generator.
- Run `make test lint check-generated build` before completing SDK changes.
- Python 3.11 is the minimum supported version. Keep packaging, CI, and documentation aligned.

## Structure

- `phenostore/client.py`: synchronous and asynchronous convenience clients
- `phenostore/_auth.py`: HTTPX OAuth2 client credentials authentication
- `phenostore/errors.py`: API exceptions and status helpers
- `phenostore/gen/`: generated API client and models
- `tools/generate.py`: reproducible generation and freshness checks
- `tests/`: mocked HTTP contracts and local TLS integration tests
