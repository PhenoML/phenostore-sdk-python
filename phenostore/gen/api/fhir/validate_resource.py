from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.fhir_resource import FhirResource
from ...models.operation_outcome import OperationOutcome
from ...models.resource_type import ResourceType
from ...types import Response


def _get_kwargs(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    *,
    body: FhirResource,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/tenants/{tenant_id}/stores/{store_id}/{resource_type}/$validate".format(
            tenant_id=quote(str(tenant_id), safe=""),
            store_id=quote(str(store_id), safe=""),
            resource_type=quote(str(resource_type), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/fhir+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> OperationOutcome | None:
    if response.status_code == 200:
        response_200 = OperationOutcome.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[OperationOutcome]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    *,
    client: AuthenticatedClient | Client,
    body: FhirResource,
) -> Response[OperationOutcome]:
    """Validate a FHIR resource

     Returns an OperationOutcome with validation results. Always returns
    HTTP 200 regardless of whether the resource is valid.

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        body (FhirResource): An arbitrary FHIR resource stored as raw JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        resource_type=resource_type,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    *,
    client: AuthenticatedClient | Client,
    body: FhirResource,
) -> OperationOutcome | None:
    """Validate a FHIR resource

     Returns an OperationOutcome with validation results. Always returns
    HTTP 200 regardless of whether the resource is valid.

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        body (FhirResource): An arbitrary FHIR resource stored as raw JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OperationOutcome
    """

    return sync_detailed(
        tenant_id=tenant_id,
        store_id=store_id,
        resource_type=resource_type,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    *,
    client: AuthenticatedClient | Client,
    body: FhirResource,
) -> Response[OperationOutcome]:
    """Validate a FHIR resource

     Returns an OperationOutcome with validation results. Always returns
    HTTP 200 regardless of whether the resource is valid.

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        body (FhirResource): An arbitrary FHIR resource stored as raw JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        resource_type=resource_type,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    *,
    client: AuthenticatedClient | Client,
    body: FhirResource,
) -> OperationOutcome | None:
    """Validate a FHIR resource

     Returns an OperationOutcome with validation results. Always returns
    HTTP 200 regardless of whether the resource is valid.

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        body (FhirResource): An arbitrary FHIR resource stored as raw JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OperationOutcome
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            store_id=store_id,
            resource_type=resource_type,
            client=client,
            body=body,
        )
    ).parsed
