# phenostore-sdk-python

Python SDK for [Phenostore](https://phenoml.com), a FHIR-compatible data store by PhenoML Inc.
Requires Python 3.11 or later.

This follows the [Go SDK](https://github.com/PhenoML/phenostore-sdk-go) design: a generated OpenAPI client and models, wrapped with OAuth2 authentication, convenience methods, and FHIR error helpers.

## Installation

From a checkout (the package has not yet been published to PyPI):

```sh
pip install .
```

Import the SDK as `phenostore`.

## Python runtime support

We support CPython feature versions that still receive upstream bug fixes or security fixes, currently Python 3.11–3.15. CI tests every supported version. New stable versions are added after compatibility checks, and the supported range is reviewed when Python releases a new feature version or an existing version reaches end of life. See the [upstream support schedule](https://devguide.python.org/versions/).

Support for a version may be removed after upstream end of life, with advance notice and an explicit release-note entry. Python 3.11 remains supported until at least its upstream end of life in October 2027. Runtime requirements are declared in `requires-python`; we do not impose an upper version bound without a known incompatibility.

## Usage

```python
from phenostore import Client, OperationOutcomeError, is_not_found

with Client(
    "https://api.phenostore.example.com",
    "your-client-id",
    "your-client-secret",
    "my-tenant",
    "my-store",
) as client:
    try:
        patient = client.read_resource("Patient", "pat-123")
        print(patient)
    except OperationOutcomeError as error:
        if is_not_found(error):
            print("not found")
        else:
            raise

    created = client.create_resource(
        "Observation",
        {
            "resourceType": "Observation",
            "status": "final",
            "code": {"text": "Blood pressure"},
            "subject": {"reference": "Patient/pat-123"},
        },
    )
```

FHIR resources and bundles are plain dictionaries. Unknown fields and extensions are preserved; the wrapper does not validate resources against a FHIR model. Use `client.tenant` and `client.store` to access the configured tenant and store.

| Method | Behavior |
| --- | --- |
| `read_resource(resource_type, id)` | Read a resource |
| `create_resource(resource_type, body, *, if_none_exist=None)` | Create, including conditional create (200 or 201) |
| `update_resource(resource_type, id, body, *, if_match=None)` | Update or upsert (200 or 201) |
| `delete_resource(resource_type, id)` | Delete; returns `None` |
| `search_resources(resource_type, params=None)` | Search with arbitrary FHIR query parameters |
| `process_bundle(bundle)` | Execute a transaction or batch bundle |

```python
results = client.search_resources(
    "Observation",
    {
        "subject:Patient.name": "Smith",
        "date": ["ge2026-01-01", "lt2027-01-01"],
        "_include": ["Observation:subject", "Observation:encounter"],
        "_count": 50,
    },
)
# A sequence of (name, value) pairs also supports repeated parameters.
client.update_resource("Patient", "pat-123", patient, if_match='W/"1"')
client.create_resource("Patient", patient, if_none_exist="identifier=https://example.com|123")
```

There is no automatic pagination; use the returned Bundle links/cursors in subsequent searches.

## Asynchronous usage

`AsyncClient` has the same six convenience methods, all awaitable:

```python
from phenostore import AsyncClient


async def read_patient():
    async with AsyncClient(base_url, client_id, client_secret, tenant, store) as client:
        return await client.read_resource("Patient", "pat-123")
```

Use a synchronous client in a `with` block (or call `close()`), and an asynchronous client in an `async with` block (or await `aclose()`). Keep an async client within one event loop.

## Authentication and HTTP configuration

OAuth2 client credentials are sent in a form body to `<base_url>/oauth/token`, matching the Go SDK. Tokens are acquired lazily, reused, and refreshed shortly before expiry. Concurrent calls share token refresh within each execution mode. Token failures raise `AuthenticationError`; requests are not retried automatically.

Both clients accept `scopes=[...]`, `timeout=30.0` (seconds or `httpx.Timeout`), `verify=True` (or an `ssl.SSLContext` for custom TLS), and `transport=...` (an HTTPX sync or async transport). These settings apply to token exchange and API calls. Redirects are disabled. A base URL may contain a path prefix.

## Errors

Convenience methods raise `OperationOutcomeError` for non-2xx API responses, including non-JSON error bodies. It exposes `status_code`, raw `body` bytes, parsed `outcome` when available, and the original HTTPX `response` with headers. Its message includes the first FHIR issue when present. `is_not_found`, `is_gone`, `is_conflict` (HTTP 412), and `is_forbidden` also inspect chained exceptions.

Invalid JSON/object responses raise `InvalidResponseError`. HTTPX connection and timeout exceptions propagate unchanged.

## Full generated API

Use `client.inner` with generated endpoint functions for patch, history, bulk, validation, `$docref`, metadata, and system endpoints. This retains automatic authentication and HTTP configuration. Use sync functions with `Client.inner` and async functions with `AsyncClient.inner`.

```python
from phenostore.gen.api.fhir import get_resource_history
from phenostore.gen.models import ResourceType

response = get_resource_history.sync_detailed(
    client.tenant,
    client.store,
    ResourceType.PATIENT,
    "pat-123",
    client=client.inner,
)
print(response.status_code, response.headers, response.parsed)
```

Each endpoint provides `sync`, `sync_detailed`, `asyncio`, and `asyncio_detailed` variants where applicable. Detailed responses expose status, headers, raw bytes, and typed models. Models support `from_dict()` and `to_dict()`.

Generated functions follow the generator's error semantics: documented error responses are returned as parsed models, undocumented statuses raise `phenostore.gen.errors.UnexpectedStatus`, and malformed modeled responses may raise parsing errors. The convenience error helpers apply to convenience methods. Health, token, and SMART endpoints can also use a standalone `phenostore.gen.Client` without automatic authentication.

## Development and generation

Install [uv](https://docs.astral.sh/uv/) and run:

```sh
make install
make generate
make test lint check-generated build
```

`api/openapi.yaml` was initially imported verbatim from the Go SDK at commit `dc11a82650f4e75dbbd3f7e8cdc292193e3056c8` (the upstream API contract). Subsequent updates arrive through the regeneration workflow. Do not edit it here; change the Phenostore API upstream. `phenostore/gen/` is generated with [openapi-python-client](https://github.com/openapi-generators/openapi-python-client); never edit generated files by hand.

Generator dependencies are pinned separately in `tools/pyproject.toml` and `tools/uv.lock` and are not runtime dependencies. The generator temporarily removes duplicate request-body encodings for identical schemas to work around a multi-media-type bug in 0.29.1, retaining the first media type (FHIR JSON). It never changes the imported spec. Formatting is isolated from local settings. `make check-generated` regenerates in a temporary directory and compares every generated file without changing the checkout.

CI tests Python 3.11–3.15, checks formatting/types and regeneration, and builds a wheel and source distribution. CI and regeneration use the pinned `astral-sh/setup-uv` action to install a specific uv version and cache dependencies using both lockfiles, with separate caches for each Python version. The regeneration workflow accepts the same `spec-updated` repository dispatch payload as the Go SDK (`spec_b64`, `spec_sha`) and opens a PR after validation. Configure the upstream dispatcher to include this repository to enable automatic spec updates. A manual workflow run regenerates from the committed spec. PRs opened with `GITHUB_TOKEN` do not trigger normal PR workflows automatically; run CI manually on the PR branch, or configure a GitHub App token for PR creation.

To upgrade the generator, run `uv add --project tools openapi-python-client==<version>`, then `make generate test lint check-generated build`. Commit the tooling lockfile and generated changes together. Dependabot's tooling PRs may need this regeneration step before CI can pass.

Regeneration PRs are created and updated with `git` and the GitHub CLI (`gh`), using the automation-owned `sdk/regenerate` branch. Only the imported spec and generated client are committed. If regeneration produces no changes relative to `main`, an existing regeneration PR is closed. Branch updates use an explicit force-with-lease check, so a concurrent push causes the workflow to fail instead of overwriting it.

Release Please prepares version/changelog PRs after conventional commits reach `main`. Publishing is intentionally left to repository owners until a PyPI project and release credentials/trusted publisher are configured.

## License

[MIT](LICENSE)
