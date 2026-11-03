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
    id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/tenants/{tenant_id}/stores/{store_id}/{resource_type}/{id}".format(
            tenant_id=quote(str(tenant_id), safe=""),
            store_id=quote(str(store_id), safe=""),
            resource_type=quote(str(resource_type), safe=""),
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> FhirResource | OperationOutcome | None:
    if response.status_code == 200:
        response_200 = FhirResource.from_dict(response.json())

        return response_200

    if response.status_code == 403:
        response_403 = OperationOutcome.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = OperationOutcome.from_dict(response.json())

        return response_404

    if response.status_code == 410:
        response_410 = OperationOutcome.from_dict(response.json())

        return response_410

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[FhirResource | OperationOutcome]:
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
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[FhirResource | OperationOutcome]:
    """Read a FHIR resource

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FhirResource | OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        resource_type=resource_type,
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> FhirResource | OperationOutcome | None:
    """Read a FHIR resource

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FhirResource | OperationOutcome
    """

    return sync_detailed(
        tenant_id=tenant_id,
        store_id=store_id,
        resource_type=resource_type,
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[FhirResource | OperationOutcome]:
    """Read a FHIR resource

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FhirResource | OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        resource_type=resource_type,
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    id: str,
    *,
    client: AuthenticatedClient | Client,
) -> FhirResource | OperationOutcome | None:
    """Read a FHIR resource

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FhirResource | OperationOutcome
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            store_id=store_id,
            resource_type=resource_type,
            id=id,
            client=client,
        )
    ).parsed
