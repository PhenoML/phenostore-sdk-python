"""HTTPX OAuth2 client credentials authentication for both execution modes."""

from __future__ import annotations

import asyncio
import math
import threading
import time
from collections.abc import AsyncGenerator, Generator, Sequence

import httpx

from .errors import AuthenticationError


class ClientCredentialsAuth(httpx.Auth):
    requires_response_body = True

    def __init__(
        self, token_url: str, client_id: str, client_secret: str, scopes: Sequence[str]
    ) -> None:
        self._token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._scopes = tuple(scopes)
        self._token = ""
        self._expires_at = 0.0
        self._sync_lock = threading.Lock()
        self._async_lock = asyncio.Lock()

    def _expired(self) -> bool:
        return not self._token or time.monotonic() >= self._expires_at

    def _token_request(self, request: httpx.Request) -> httpx.Request:
        data = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }
        if self._scopes:
            data["scope"] = " ".join(self._scopes)
        return httpx.Request(
            "POST",
            self._token_url,
            data=data,
            headers={"Accept": "application/json"},
            extensions={"timeout": request.extensions.get("timeout", {})},
        )

    def _receive_token(self, response: httpx.Response) -> None:
        if response.status_code != 200:
            raise AuthenticationError(response)
        try:
            data = response.json()
            token = data["access_token"]
            token_type = data["token_type"]
            lifetime = float(data["expires_in"])
            if (
                not isinstance(token, str)
                or not token
                or not token.isascii()
                or any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in token)
                or not isinstance(token_type, str)
                or token_type.lower() != "bearer"
                or not math.isfinite(lifetime)
                or lifetime <= 0
            ):
                raise ValueError("invalid token")
        except (ValueError, TypeError, KeyError, OverflowError):
            raise AuthenticationError(response, "invalid token response") from None
        self._token = token
        self._expires_at = time.monotonic() + lifetime - min(10, lifetime / 10)

    def sync_auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        with self._sync_lock:
            if self._expired():
                response = yield self._token_request(request)
                response.read()
                self._receive_token(response)
            request.headers["Authorization"] = f"Bearer {self._token}"
        yield request

    async def async_auth_flow(
        self, request: httpx.Request
    ) -> AsyncGenerator[httpx.Request, httpx.Response]:
        async with self._async_lock:
            if self._expired():
                response = yield self._token_request(request)
                await response.aread()
                self._receive_token(response)
            request.headers["Authorization"] = f"Bearer {self._token}"
        yield request
