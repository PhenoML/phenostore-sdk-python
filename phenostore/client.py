"""Small convenience layer over generated request builders and HTTPX."""

from __future__ import annotations

import ssl
from collections.abc import Mapping, Sequence
from typing import Any, Self, cast

import httpx

from ._auth import ClientCredentialsAuth
from .errors import OperationOutcomeError, _json_object
from .gen.api.fhir import (
    create_resource,
    delete_resource,
    process_bundle,
    read_resource,
    search_resources,
    update_resource,
)
from .gen.client import Client as GeneratedClient
from .gen.models import FhirResource, ResourceType
from .gen.types import UNSET

JSON = dict[str, Any]
SearchParams = Mapping[str, str | int | Sequence[str]] | Sequence[tuple[str, str | int]]


class _BaseClient:
    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        tenant: str,
        store: str,
        *,
        scopes: Sequence[str] = (),
        timeout: float | httpx.Timeout = 30.0,
        verify: bool | ssl.SSLContext = True,
        transport: httpx.BaseTransport | httpx.AsyncBaseTransport | None = None,
    ) -> None:
        url = httpx.URL(base_url)
        if (
            url.scheme not in ("http", "https")
            or not url.host
            or url.query
            or url.fragment
            or url.userinfo
        ):
            raise ValueError(
                "base_url must be an absolute HTTP(S) URL without credentials or query"
            )
        if not all((client_id, client_secret, tenant, store)):
            raise ValueError("client_id, client_secret, tenant, and store must be nonempty")
        if isinstance(scopes, str):
            raise TypeError("scopes must be a sequence of scope strings")
        self.tenant = tenant
        self.store = store
        base_url = str(url).rstrip("/")
        auth = ClientCredentialsAuth(base_url + "/oauth/token", client_id, client_secret, scopes)
        self.inner = GeneratedClient(
            base_url=base_url,
            timeout=timeout if isinstance(timeout, httpx.Timeout) else httpx.Timeout(timeout),
            verify_ssl=verify,
            follow_redirects=False,
            headers={"Accept": "application/fhir+json", "User-Agent": "phenostore-sdk-python"},
            httpx_args={"auth": auth, "transport": transport},
            raise_on_unexpected_status=True,
        )

    def _read(self, resource_type: str, id: str) -> JSON:
        return read_resource._get_kwargs(
            self.tenant, self.store, cast(ResourceType, resource_type), id
        )

    def _create(
        self, resource_type: str, body: Mapping[str, Any], if_none_exist: str | None
    ) -> JSON:
        return create_resource._get_kwargs(
            self.tenant,
            self.store,
            cast(ResourceType, resource_type),
            body=FhirResource.from_dict(body),
            if_none_exist=if_none_exist if if_none_exist is not None else UNSET,
        )

    def _update(
        self, resource_type: str, id: str, body: Mapping[str, Any], if_match: str | None
    ) -> JSON:
        return update_resource._get_kwargs(
            self.tenant,
            self.store,
            cast(ResourceType, resource_type),
            id,
            body=FhirResource.from_dict(body),
            if_match=if_match if if_match is not None else UNSET,
        )

    def _delete(self, resource_type: str, id: str) -> JSON:
        return delete_resource._get_kwargs(
            self.tenant, self.store, cast(ResourceType, resource_type), id
        )

    def _search(self, resource_type: str, params: SearchParams | None) -> JSON:
        kwargs = search_resources._get_kwargs(
            self.tenant, self.store, cast(ResourceType, resource_type)
        )
        # The generated signature only includes parameters explicitly named in the
        # spec. FHIR also allows arbitrary names, modifiers, chains and repetition.
        kwargs["params"] = params if params is not None else {}
        return kwargs

    def _bundle(self, bundle: Mapping[str, Any]) -> JSON:
        return process_bundle._get_kwargs(
            self.tenant, self.store, body=FhirResource.from_dict(bundle)
        )


class Client(_BaseClient):
    """Synchronous Phenostore client with lazy OAuth2 authentication.

    Use as a context manager or call close() to release pooled connections.
    The transport, timeout and TLS configuration also apply to token requests.
    Access inner to use generated API functions and typed models directly.
    """

    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        tenant: str,
        store: str,
        *,
        scopes: Sequence[str] = (),
        timeout: float | httpx.Timeout = 30.0,
        verify: bool | ssl.SSLContext = True,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        super().__init__(
            base_url,
            client_id,
            client_secret,
            tenant,
            store,
            scopes=scopes,
            timeout=timeout,
            verify=verify,
            transport=transport,
        )
        # Construct once before the client can be shared between threads. Token
        # acquisition stays lazy; the generated client's lazy initializer is not
        # synchronized and can otherwise allocate multiple connection pools.
        self.inner.get_httpx_client()

    def _request(self, kwargs: JSON) -> httpx.Response:
        response = self.inner.get_httpx_client().request(**kwargs)
        if not 200 <= response.status_code < 300:
            raise OperationOutcomeError(response)
        return response

    def read_resource(self, resource_type: str, id: str) -> JSON:
        """Read a resource, preserving every JSON field."""
        return _json_object(self._request(self._read(resource_type, id)))

    def create_resource(
        self, resource_type: str, body: Mapping[str, Any], *, if_none_exist: str | None = None
    ) -> JSON:
        """Create a resource, optionally with conditional search criteria."""
        return _json_object(self._request(self._create(resource_type, body, if_none_exist)))

    def update_resource(
        self, resource_type: str, id: str, body: Mapping[str, Any], *, if_match: str | None = None
    ) -> JSON:
        """Update or upsert, optionally requiring an ETag such as W/\"1\"."""
        return _json_object(self._request(self._update(resource_type, id, body, if_match)))

    def delete_resource(self, resource_type: str, id: str) -> None:
        """Delete a resource. Deleted and missing resources may raise API errors."""
        self._request(self._delete(resource_type, id))

    def search_resources(self, resource_type: str, params: SearchParams | None = None) -> JSON:
        """Search with arbitrary FHIR parameters; sequence values repeat a parameter."""
        return _json_object(self._request(self._search(resource_type, params)))

    def process_bundle(self, bundle: Mapping[str, Any]) -> JSON:
        """Execute a transaction or batch bundle."""
        return _json_object(self._request(self._bundle(bundle)))

    def close(self) -> None:
        """Close the underlying synchronous HTTP client."""
        self.inner.get_httpx_client().close()

    def __enter__(self) -> Self:
        self.inner.get_httpx_client().__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncClient(_BaseClient):
    """Asynchronous equivalent of Client. Use async with or await aclose()."""

    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        tenant: str,
        store: str,
        *,
        scopes: Sequence[str] = (),
        timeout: float | httpx.Timeout = 30.0,
        verify: bool | ssl.SSLContext = True,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        super().__init__(
            base_url,
            client_id,
            client_secret,
            tenant,
            store,
            scopes=scopes,
            timeout=timeout,
            verify=verify,
            transport=transport,
        )

    async def _request(self, kwargs: JSON) -> httpx.Response:
        response = await self.inner.get_async_httpx_client().request(**kwargs)
        if not 200 <= response.status_code < 300:
            raise OperationOutcomeError(response)
        return response

    async def read_resource(self, resource_type: str, id: str) -> JSON:
        """Read a resource, preserving every JSON field."""
        return _json_object(await self._request(self._read(resource_type, id)))

    async def create_resource(
        self, resource_type: str, body: Mapping[str, Any], *, if_none_exist: str | None = None
    ) -> JSON:
        """Create a resource, optionally with conditional search criteria."""
        return _json_object(await self._request(self._create(resource_type, body, if_none_exist)))

    async def update_resource(
        self, resource_type: str, id: str, body: Mapping[str, Any], *, if_match: str | None = None
    ) -> JSON:
        """Update or upsert, optionally requiring an ETag."""
        return _json_object(await self._request(self._update(resource_type, id, body, if_match)))

    async def delete_resource(self, resource_type: str, id: str) -> None:
        """Delete a resource."""
        await self._request(self._delete(resource_type, id))

    async def search_resources(
        self, resource_type: str, params: SearchParams | None = None
    ) -> JSON:
        """Search with arbitrary FHIR parameters, including repeated values."""
        return _json_object(await self._request(self._search(resource_type, params)))

    async def process_bundle(self, bundle: Mapping[str, Any]) -> JSON:
        """Execute a transaction or batch bundle."""
        return _json_object(await self._request(self._bundle(bundle)))

    async def aclose(self) -> None:
        """Close the underlying asynchronous HTTP client."""
        await self.inner.get_async_httpx_client().aclose()

    async def __aenter__(self) -> Self:
        await self.inner.get_async_httpx_client().__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()
