from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor

import httpx
import pytest

from phenostore import AsyncClient, AuthenticationError, Client

from .conftest import PATIENT, call


async def test_token_refresh(client, server, monkeypatch):
    now = [100.0]
    monkeypatch.setattr("phenostore._auth.time.monotonic", lambda: now[0])
    await call(client.read_resource, "Patient", "pat-123")
    now[0] += 3601
    server.token_response = httpx.Response(
        200,
        json={
            "access_token": "token-2",
            "token_type": "Bearer",
            "expires_in": 3600,
        },
    )
    await call(client.read_resource, "Patient", "pat-123")
    assert len(server.token_requests) == 2
    assert server.requests[-1].headers["authorization"] == "Bearer token-2"


@pytest.mark.parametrize(
    "response",
    [
        httpx.Response(401, json={"error": "invalid_client"}),
        httpx.Response(500, content=b"unavailable"),
        httpx.Response(200, content=b"not JSON"),
        httpx.Response(200, json=[]),
        *[
            httpx.Response(
                200, json={"access_token": token, "token_type": kind, "expires_in": expiry}
            )
            for token, kind, expiry in [
                ("", "Bearer", 3600),
                ("token", "MAC", 3600),
                ("token", "Bearer", -1),
                ("token", "Bearer", "NaN"),
                ("token", "Bearer", "Infinity"),
                ("token", "Bearer", "secret"),
                (None, "Bearer", 3600),
                ("bad\r\ntoken", "Bearer", 3600),
                ("token", None, 3600),
            ]
        ],
    ],
)
async def test_auth_failures_never_send_resource_request(client, server, response):
    server.token_response = response
    with pytest.raises(AuthenticationError) as caught:
        await call(client.read_resource, "Patient", "pat-123")
    assert caught.value.status_code == response.status_code
    assert caught.value.body == response.content
    assert "s&cret" not in str(caught.value)
    assert not server.requests


async def test_token_exchange_can_recover_after_failure(client, server):
    server.token_response = httpx.Response(401)
    with pytest.raises(AuthenticationError):
        await call(client.read_resource, "Patient", "pat-123")
    server.token_response = httpx.Response(
        200,
        json={
            "access_token": "valid",
            "token_type": "bearer",
            "expires_in": 3600,
        },
    )
    assert await call(client.read_resource, "Patient", "pat-123") == PATIENT
    assert len(server.token_requests) == 2


def test_concurrent_sync_requests_share_one_token(server):
    with Client(
        "https://example.test", "id", "secret", "t", "s", transport=httpx.MockTransport(server)
    ) as client:
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda _: client.read_resource("Patient", "id"), range(24)))
        assert results == [PATIENT] * 24
    assert len(server.token_requests) == 1
    assert client.inner.get_httpx_client().is_closed


async def test_concurrent_async_requests_share_one_token(server):
    async def handler(request):
        # Let simultaneous requests reach authentication while token exchange waits.
        await asyncio.sleep(0.001)
        return server(request)

    async with AsyncClient(
        "https://example.test", "id", "secret", "t", "s", transport=httpx.MockTransport(handler)
    ) as client:
        results = await asyncio.gather(*[client.read_resource("Patient", "id") for _ in range(24)])
        assert results == [PATIENT] * 24
    assert len(server.token_requests) == 1
    assert client.inner.get_async_httpx_client().is_closed


@pytest.mark.parametrize("during_token", [True, False])
async def test_transport_exceptions_propagate(client, server, during_token):
    def handler(request):
        if request.url.path.endswith("/oauth/token") and not during_token:
            return server(request)
        raise httpx.ReadTimeout("timed out", request=request)

    transport = httpx.MockTransport(handler)
    if isinstance(client, Client):
        client.inner.get_httpx_client()._transport = transport
    else:
        client.inner.get_async_httpx_client()._transport = transport
    with pytest.raises(httpx.ReadTimeout):
        await call(client.read_resource, "Patient", "pat-123")
