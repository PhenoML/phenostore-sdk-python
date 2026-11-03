from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bulk_operation_accepted import BulkOperationAccepted
from ...models.bundle import Bundle
from ...models.fhir_resource import FhirResource
from ...models.operation_outcome import OperationOutcome
from ...types import Response


def _get_kwargs(
    tenant_id: str,
    store_id: str,
    *,
    body: FhirResource,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/tenants/{tenant_id}/stores/{store_id}/$bulk".format(
            tenant_id=quote(str(tenant_id), safe=""),
            store_id=quote(str(store_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/fhir+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BulkOperationAccepted | Bundle | OperationOutcome | None:
    if response.status_code == 200:
        response_200 = Bundle.from_dict(response.json())

        return response_200

    if response.status_code == 202:
        response_202 = BulkOperationAccepted.from_dict(response.json())

        return response_202

    if response.status_code == 400:
        response_400 = OperationOutcome.from_dict(response.json())

        return response_400

    if response.status_code == 403:
        response_403 = OperationOutcome.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BulkOperationAccepted | Bundle | OperationOutcome]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    store_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: FhirResource,
) -> Response[BulkOperationAccepted | Bundle | OperationOutcome]:
    """Submit a bulk operation

     Submits a batch Bundle for bulk processing. Operations with ≤100 entries
    are processed synchronously; larger batches are processed asynchronously
    and return 202 with a Content-Location header for polling.

    Args:
        tenant_id (str):
        store_id (str):
        body (FhirResource): An arbitrary FHIR resource stored as raw JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BulkOperationAccepted | Bundle | OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    store_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: FhirResource,
) -> BulkOperationAccepted | Bundle | OperationOutcome | None:
    """Submit a bulk operation

     Submits a batch Bundle for bulk processing. Operations with ≤100 entries
    are processed synchronously; larger batches are processed asynchronously
    and return 202 with a Content-Location header for polling.

    Args:
        tenant_id (str):
        store_id (str):
        body (FhirResource): An arbitrary FHIR resource stored as raw JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BulkOperationAccepted | Bundle | OperationOutcome
    """

    return sync_detailed(
        tenant_id=tenant_id,
        store_id=store_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    store_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: FhirResource,
) -> Response[BulkOperationAccepted | Bundle | OperationOutcome]:
    """Submit a bulk operation

     Submits a batch Bundle for bulk processing. Operations with ≤100 entries
    are processed synchronously; larger batches are processed asynchronously
    and return 202 with a Content-Location header for polling.

    Args:
        tenant_id (str):
        store_id (str):
        body (FhirResource): An arbitrary FHIR resource stored as raw JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BulkOperationAccepted | Bundle | OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    store_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: FhirResource,
) -> BulkOperationAccepted | Bundle | OperationOutcome | None:
    """Submit a bulk operation

     Submits a batch Bundle for bulk processing. Operations with ≤100 entries
    are processed synchronously; larger batches are processed asynchronously
    and return 202 with a Content-Location header for polling.

    Args:
        tenant_id (str):
        store_id (str):
        body (FhirResource): An arbitrary FHIR resource stored as raw JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BulkOperationAccepted | Bundle | OperationOutcome
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            store_id=store_id,
            client=client,
            body=body,
        )
    ).parsed
