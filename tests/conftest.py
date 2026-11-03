from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import Any

import httpx
import pytest

from phenostore import AsyncClient, Client

PATIENT = {
    "resourceType": "Patient",
    "id": "pat-123",
    "active": True,
    "name": [{"family": "García", "given": ["Ana"]}],
    "extension": [{"url": "https://example.com/custom", "valueString": "kept"}],
    "unknownField": {"nested": [1, None, False]},
}
BUNDLE = {
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "entry": [{"resource": PATIENT}],
    "custom": "preserved",
}


async def call(method: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    result = method(*args, **kwargs)
    return await result if inspect.isawaitable(result) else result


class Server:
    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []
        self.token_requests: list[httpx.Request] = []
        self.token_response = httpx.Response(
            200,
            json={
                "access_token": "token-1",
                "token_type": "Bearer",
                "expires_in": 3600,
                "scope": "",
            },
        )
        self.response = httpx.Response(200, json=PATIENT)

    def __call__(self, request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/oauth/token"):
            self.token_requests.append(request)
            response = self.token_response
        else:
            self.requests.append(request)
            response = self.response
        # HTTPX binds streams to the sending client. Do not reuse a response
        # across requests or between synchronous and asynchronous tests.
        return httpx.Response(
            response.status_code, headers=response.headers, content=response.content
        )


@pytest.fixture
def server() -> Server:
    return Server()


@pytest.fixture(params=[Client, AsyncClient], ids=["sync", "async"])
async def client(request: pytest.FixtureRequest, server: Server) -> Any:
    cls = request.param
    instance = cls(
        "https://example.test/prefix/",
        "client-id",
        "s&cret+value",
        "tenant",
        "store",
        scopes=["patient/*.read", "patient/*.write"],
        timeout=7.5,
        transport=httpx.MockTransport(server),
    )
    yield instance
    await call(instance.aclose if cls is AsyncClient else instance.close)
