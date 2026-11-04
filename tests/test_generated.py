"""Exercise generated functions through the authenticated wrapper transport."""

from __future__ import annotations

import datetime
import importlib
import pkgutil
from urllib.parse import parse_qs

import httpx
import pytest

import phenostore.gen
from phenostore import Client
from phenostore.gen import Client as GeneratedClient
from phenostore.gen.api.bulk import get_bulk_status, submit_bulk
from phenostore.gen.api.fhir import (
    conditional_delete_resource,
    get_docref,
    get_metadata,
    get_resource_history,
    get_smart_configuration,
    patch_resource,
    post_docref,
    read_resource,
    read_resource_version,
    search_resources,
    search_resources_post,
    validate_resource,
)
from phenostore.gen.api.o_auth import issue_token
from phenostore.gen.api.system import get_health
from phenostore.gen.errors import UnexpectedStatus
from phenostore.gen.models import (
    FhirResource,
    IssueTokenBody,
    IssueTokenBodyGrantType,
    JsonPatchItem,
    JsonPatchOp,
    PostDocrefBody,
    ResourceType,
    SearchResourcesPostBody,
    SearchTotalMode,
)

from .conftest import BUNDLE, PATIENT, call


async def generated(client, module, *args, **kwargs):
    method = module.sync_detailed if isinstance(client, Client) else module.asyncio_detailed
    return await call(method, *args, client=client.inner, **kwargs)


def test_every_generated_module_imports():
    for module in pkgutil.walk_packages(phenostore.gen.__path__, phenostore.gen.__name__ + "."):
        importlib.import_module(module.name)


async def test_generated_read_preserves_http_dates_and_raw_fields(client, server):
    headers = {"ETag": 'W/"1"', "Last-Modified": "Wed, 21 Oct 2015 07:28:00 GMT"}
    server.response = httpx.Response(200, json=PATIENT, headers=headers)
    response = await generated(client, read_resource, "tenant", "store", ResourceType.PATIENT, "id")
    assert response.status_code == 200
    assert response.headers["last-modified"] == headers["Last-Modified"]
    assert response.headers["etag"] == 'W/"1"'
    assert response.parsed.to_dict() == PATIENT


async def test_generated_patch(client, server):
    body = [JsonPatchItem(op=JsonPatchOp.REPLACE, path="/active", value=False)]
    response = await generated(
        client,
        patch_resource,
        "tenant",
        "store",
        ResourceType.PATIENT,
        "id",
        body=body,
        if_match='W/"1"',
    )
    assert response.parsed.to_dict() == PATIENT
    request = server.requests[-1]
    assert request.method == "PATCH"
    assert request.headers["content-type"] == "application/json-patch+json"
    assert request.headers["if-match"] == 'W/"1"'
    assert request.content == b'[{"op":"replace","path":"/active","value":false}]'


async def test_generated_history_and_vread(client, server):
    history = {**BUNDLE, "type": "history"}
    server.response = httpx.Response(200, json=history)
    response = await generated(
        client,
        get_resource_history,
        "tenant",
        "store",
        ResourceType.PATIENT,
        "id",
        field_count=10,
        field_offset=20,
    )
    assert response.parsed.to_dict() == history
    assert server.requests[-1].url.path.endswith("/Patient/id/_history")
    assert server.requests[-1].url.params["_count"] == "10"
    assert server.requests[-1].url.params["_offset"] == "20"
    server.response = httpx.Response(200, json=PATIENT)
    response = await generated(
        client, read_resource_version, "tenant", "store", ResourceType.PATIENT, "id", 2
    )
    assert response.parsed.to_dict() == PATIENT
    assert server.requests[-1].url.path.endswith("/Patient/id/_history/2")


async def test_generated_bulk_accepted_polling_and_synchronous_result(client, server):
    accepted = {"id": "op-1", "status": "pending", "total": 101}
    server.response = httpx.Response(202, json=accepted, headers={"Content-Location": "/poll/op-1"})
    response = await generated(
        client, submit_bulk, "tenant", "store", body=FhirResource.from_dict(BUNDLE)
    )
    assert response.status_code == 202
    assert response.headers["content-location"] == "/poll/op-1"
    assert response.parsed.to_dict() == accepted
    assert server.requests[-1].url.path.endswith("/$bulk")
    status = {
        "id": "op-1",
        "status": "processing",
        "total_count": 101,
        "processed_count": 50,
        "error_count": 0,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
    }
    server.response = httpx.Response(202, json=status)
    response = await generated(client, get_bulk_status, "tenant", "store", "op-1")
    assert response.parsed.status.value == "processing"
    assert server.requests[-1].url.path.endswith("/$bulk/op-1")
    server.response = httpx.Response(200, json={**BUNDLE, "type": "batch-response"})
    response = await generated(
        client, submit_bulk, "tenant", "store", body=FhirResource.from_dict(BUNDLE)
    )
    assert response.parsed.type_.value == "batch-response"


async def test_generated_validation_outcome_on_success(client, server):
    outcome = {
        "resourceType": "OperationOutcome",
        "issue": [{"severity": "error", "code": "invalid"}],
    }
    server.response = httpx.Response(200, json=outcome)
    response = await generated(
        client,
        validate_resource,
        "tenant",
        "store",
        ResourceType.PATIENT,
        body=FhirResource.from_dict(PATIENT),
    )
    assert response.parsed.to_dict() == outcome
    assert server.requests[-1].url.path.endswith("/Patient/$validate")


async def test_generated_get_and_post_docref(client, server):
    server.response = httpx.Response(200, json=BUNDLE)
    start = datetime.date(2026, 1, 1)
    response = await generated(
        client,
        get_docref,
        "tenant",
        "store",
        patient="Patient/pat-123",
        start=start,
        field_total=SearchTotalMode.ACCURATE,
    )
    assert response.parsed.to_dict() == BUNDLE
    request = server.requests[-1]
    assert request.url.path.endswith("/DocumentReference/$docref")
    assert request.url.params["patient"] == "Patient/pat-123"
    assert request.url.params["start"] == "2026-01-01"
    assert request.url.params["_total"] == "accurate"
    response = await generated(
        client,
        post_docref,
        "tenant",
        "store",
        body=PostDocrefBody(patient="Patient/pat-123", start=start),
    )
    assert response.parsed.to_dict() == BUNDLE
    request = server.requests[-1]
    assert request.method == "POST"
    assert request.headers["content-type"] == "application/x-www-form-urlencoded"
    assert parse_qs(request.content.decode())["patient"] == ["Patient/pat-123"]


async def test_generated_search_get_post_and_conditional_delete(client, server):
    server.response = httpx.Response(200, json=BUNDLE)
    response = await generated(
        client,
        search_resources,
        "tenant",
        "store",
        ResourceType.PATIENT,
        field_include=["Patient:organization", "Patient:general-practitioner"],
    )
    assert response.parsed.to_dict() == BUNDLE
    assert len(server.requests[-1].url.params.get_list("_include")) == 2
    body = SearchResourcesPostBody.from_dict(
        {"name:exact": "Ana", "_count": 5, "_include": ["Patient:organization", "Patient:link"]}
    )
    response = await generated(
        client, search_resources_post, "tenant", "store", ResourceType.PATIENT, body=body
    )
    assert response.parsed.to_dict() == BUNDLE
    params = parse_qs(server.requests[-1].content.decode())
    assert params["name:exact"] == ["Ana"]
    assert params["_include"] == ["Patient:organization", "Patient:link"]
    server.response = httpx.Response(204)
    response = await generated(
        client,
        conditional_delete_resource,
        "tenant",
        "store",
        ResourceType.PATIENT,
        identifier="http://example.com|123",
    )
    assert response.status_code == 204
    assert server.requests[-1].url.params["identifier"] == "http://example.com|123"


async def test_generated_metadata_smart_config_and_health(client, server):
    metadata = {"resourceType": "CapabilityStatement", "status": "active"}
    server.response = httpx.Response(200, json=metadata)
    response = await generated(client, get_metadata, "tenant", "store")
    assert response.parsed.to_dict() == metadata
    smart = {"token_endpoint": "https://example.test/oauth/token", "custom": "retained"}
    server.response = httpx.Response(200, json=smart)
    response = await generated(client, get_smart_configuration, "tenant", "store")
    assert response.parsed.to_dict() == smart
    server.response = httpx.Response(200, json={"status": "ok"})
    response = await generated(client, get_health)
    assert response.parsed.status.value == "ok"


def test_standalone_generated_client_token_and_public_health(server):
    with GeneratedClient(
        base_url="https://example.test", httpx_args={"transport": httpx.MockTransport(server)}
    ) as client:
        response = issue_token.sync_detailed(
            client=client,
            body=IssueTokenBody(
                grant_type=IssueTokenBodyGrantType.CLIENT_CREDENTIALS,
                client_id="id",
                client_secret="secret",
            ),
        )
        assert response.parsed.access_token == "token-1"
        assert len(server.token_requests) == 1
        assert "authorization" not in server.token_requests[0].headers
        server.response = httpx.Response(200, json={"status": "ok"})
        assert get_health.sync(client=client).status.value == "ok"
        assert "authorization" not in server.requests[-1].headers


async def test_generated_error_models_and_unexpected_status(client, server):
    outcome = {
        "resourceType": "OperationOutcome",
        "issue": [{"severity": "error", "code": "not-found"}],
    }
    server.response = httpx.Response(404, json=outcome)
    response = await generated(client, read_resource, "tenant", "store", ResourceType.PATIENT, "id")
    assert response.status_code == 404
    assert response.parsed.to_dict() == outcome
    server.response = httpx.Response(503, content=b"unavailable")
    with pytest.raises(UnexpectedStatus):
        await generated(client, read_resource, "tenant", "store", ResourceType.PATIENT, "id")
