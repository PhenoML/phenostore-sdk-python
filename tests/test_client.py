from __future__ import annotations

import json
from urllib.parse import parse_qs

import httpx
import pytest

from phenostore import (
    Client,
    InvalidResponseError,
    OperationOutcomeError,
    is_conflict,
    is_forbidden,
    is_gone,
    is_not_found,
)

from .conftest import BUNDLE, PATIENT, call


async def test_lazy_auth_cache_scope_prefix_and_timeout(client, server):
    assert not server.token_requests
    for _ in range(2):
        assert await call(client.read_resource, "Patient", "pat-123") == PATIENT
    assert len(server.token_requests) == 1
    token_request = server.token_requests[0]
    assert str(token_request.url) == "https://example.test/prefix/oauth/token"
    assert token_request.headers["content-type"] == "application/x-www-form-urlencoded"
    assert "authorization" not in token_request.headers
    assert parse_qs(token_request.content.decode()) == {
        "grant_type": ["client_credentials"],
        "client_id": ["client-id"],
        "client_secret": ["s&cret+value"],
        "scope": ["patient/*.read patient/*.write"],
    }
    assert token_request.extensions["timeout"] == dict.fromkeys(
        ["connect", "read", "write", "pool"], 7.5
    )
    for request in server.requests:
        assert request.method == "GET"
        assert request.url.path == "/prefix/v1/tenants/tenant/stores/store/Patient/pat-123"
        assert request.headers["authorization"] == "Bearer token-1"
        assert request.headers["accept"] == "application/fhir+json"
        assert b"s&cret" not in request.content
        assert request.extensions["timeout"] == token_request.extensions["timeout"]
    assert client.tenant == "tenant" and client.store == "store"


@pytest.mark.parametrize("status", [200, 201])
async def test_create_and_upsert_with_conditionals(client, server, status):
    server.response = httpx.Response(status, json=PATIENT)
    for header in [None, "identifier=http://example.com|123"]:
        result = await call(client.create_resource, "Patient", PATIENT, if_none_exist=header)
        assert result == PATIENT
        request = server.requests[-1]
        assert request.method == "POST"
        assert request.headers.get("if-none-exist") == header
        assert request.headers["content-type"] == "application/fhir+json"
        assert json.loads(request.content) == PATIENT
    for header in [None, 'W/"1"']:
        result = await call(client.update_resource, "Patient", "pat-123", PATIENT, if_match=header)
        assert result == PATIENT
        request = server.requests[-1]
        assert request.method == "PUT"
        assert request.headers.get("if-match") == header
        assert json.loads(request.content) == PATIENT


async def test_delete_accepts_empty_204(client, server):
    server.response = httpx.Response(204)
    assert await call(client.delete_resource, "Patient", "pat-123") is None
    assert server.requests[-1].method == "DELETE"


async def test_arbitrary_repeated_search_parameters_and_bundle_preservation(client, server):
    server.response = httpx.Response(200, json=BUNDLE)
    params = {
        "name:contains": "García & Ana",
        "subject:Patient.name": "Smith",
        "date": ["ge2026-01-01", "lt2027-01-01"],
        "_count": 0,
        "_include": ["Observation:subject", "Observation:encounter"],
        "_revinclude": ["Provenance:target"],
        "_cursor": "abc+/=",
    }
    assert await call(client.search_resources, "Observation", params) == BUNDLE
    query = server.requests[-1].url.params
    assert query["name:contains"] == "García & Ana"
    assert query["subject:Patient.name"] == "Smith"
    assert query.get_list("date") == params["date"]
    assert query.get_list("_include") == params["_include"]
    assert query["_cursor"] == "abc+/="
    assert query["_count"] == "0"
    assert "_offset" not in query
    await call(client.search_resources, "Patient", [("given", "Ana"), ("given", "Maria")])
    assert server.requests[-1].url.params.get_list("given") == ["Ana", "Maria"]
    await call(client.search_resources, "Patient")
    assert not server.requests[-1].url.query


async def test_process_bundle(client, server):
    body = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [{"resource": PATIENT, "request": {"method": "POST", "url": "Patient"}}],
    }
    response = {**body, "type": "transaction-response"}
    server.response = httpx.Response(200, json=response)
    assert await call(client.process_bundle, body) == response
    request = server.requests[-1]
    assert request.method == "POST"
    assert request.url.path.endswith("/stores/store")
    assert json.loads(request.content) == body
    assert request.headers["content-type"] == "application/fhir+json"


async def test_path_segments_are_escaped(client, server):
    client.tenant = "tenant/with space"
    client.store = "store?#"
    await call(client.read_resource, "FutureResource", "id/with?query#fragment")
    assert server.requests[-1].url.raw_path == (
        b"/prefix/v1/tenants/tenant%2Fwith%20space/stores/store%3F%23/"
        b"FutureResource/id%2Fwith%3Fquery%23fragment"
    )


@pytest.mark.parametrize(
    "status,helper",
    [
        (404, is_not_found),
        (410, is_gone),
        (412, is_conflict),
        (403, is_forbidden),
    ],
)
async def test_outcome_errors_and_helpers(client, server, status, helper):
    outcome = {
        "resourceType": "OperationOutcome",
        "issue": [{"severity": "error", "code": "processing", "diagnostics": "explanation"}],
    }
    server.response = httpx.Response(status, json=outcome, headers={"X-Request-ID": "req-1"})
    with pytest.raises(OperationOutcomeError, match=r"\[error/processing\] explanation") as caught:
        await call(client.read_resource, "Patient", "pat-123")
    error = caught.value
    assert error.status_code == status
    assert error.outcome == outcome
    assert json.loads(error.body) == outcome
    assert error.response.headers["x-request-id"] == "req-1"
    assert helper(error)
    assert not helper(None)
    wrapped = RuntimeError("wrapped")
    wrapped.__cause__ = error
    assert helper(wrapped)
    assert not helper(ValueError("unrelated"))


@pytest.mark.parametrize(
    "earlier_status,current_status",
    [(404, 403), (410, 404), (412, 410), (403, 412), (404, 500)],
)
async def test_status_helpers_stop_at_the_first_api_error(
    client, server, earlier_status, current_status
):
    server.response = httpx.Response(earlier_status)
    with pytest.raises(OperationOutcomeError) as caught:
        try:
            await call(client.read_resource, "Patient", "pat-123")
        except OperationOutcomeError:
            server.response = httpx.Response(current_status)
            await call(client.create_resource, "Patient", PATIENT)

    error = caught.value
    assert error.status_code == current_status
    assert isinstance(error.__context__, OperationOutcomeError)
    assert error.__context__.status_code == earlier_status
    for status, helper in [
        (404, is_not_found),
        (410, is_gone),
        (412, is_conflict),
        (403, is_forbidden),
    ]:
        assert helper(error) is (current_status == status)


@pytest.mark.parametrize(
    "body", [b"gateway error", b"[]", b"null", b'{"issue": {}}', b'{"issue": [null]}', b"\xff"]
)
async def test_non_fhir_error_bodies_are_retained(client, server, body):
    server.response = httpx.Response(503, content=body)
    with pytest.raises(OperationOutcomeError, match="HTTP 503") as caught:
        await call(client.read_resource, "Patient", "pat-123")
    assert caught.value.body == body


@pytest.mark.parametrize(
    "operation,args",
    [
        ("create_resource", ("Patient", PATIENT)),
        ("update_resource", ("Patient", "pat-123", PATIENT)),
        ("delete_resource", ("Patient", "pat-123")),
        ("search_resources", ("Patient",)),
        ("process_bundle", (BUNDLE,)),
    ],
)
async def test_each_operation_raises_api_errors(client, server, operation, args):
    server.response = httpx.Response(500, content=b"server error")
    with pytest.raises(OperationOutcomeError) as caught:
        await call(getattr(client, operation), *args)
    assert caught.value.status_code == 500


@pytest.mark.parametrize("body", [b"not json", b"[]", b"null", b"\xff"])
async def test_invalid_success_body(client, server, body):
    server.response = httpx.Response(200, content=body)
    with pytest.raises(InvalidResponseError):
        await call(client.read_resource, "Patient", "pat-123")


@pytest.mark.parametrize("status", [302, 401])
async def test_redirects_and_unauthorized_requests_are_not_retried(client, server, status):
    server.response = httpx.Response(status, headers={"Location": "https://elsewhere.test"})
    with pytest.raises(OperationOutcomeError):
        await call(client.read_resource, "Patient", "pat-123")
    assert len(server.requests) == len(server.token_requests) == 1


@pytest.mark.parametrize(
    "url",
    [
        "relative",
        "ftp://example.com",
        "https://user:pass@example.com",
        "https://example.com?x=1",
        "https://example.com#fragment",
    ],
)
def test_invalid_base_urls(url):
    with pytest.raises(ValueError):
        Client(url, "id", "secret", "tenant", "store")


def test_invalid_configuration():
    with pytest.raises(ValueError):
        Client("https://example.com", "", "secret", "tenant", "store")
    with pytest.raises(TypeError):
        Client("https://example.com", "id", "secret", "tenant", "store", scopes="scope")


def test_exception_helper_handles_cycles():
    error = RuntimeError()
    error.__cause__ = error
    assert not is_not_found(error)
