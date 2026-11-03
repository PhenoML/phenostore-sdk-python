from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bundle import Bundle
from ...models.operation_outcome import OperationOutcome
from ...models.resource_type import ResourceType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    id: str,
    *,
    field_count: int | Unset = 20,
    field_offset: int | Unset = 0,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["_count"] = field_count

    params["_offset"] = field_offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/tenants/{tenant_id}/stores/{store_id}/{resource_type}/{id}/_history".format(
            tenant_id=quote(str(tenant_id), safe=""),
            store_id=quote(str(store_id), safe=""),
            resource_type=quote(str(resource_type), safe=""),
            id=quote(str(id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Bundle | OperationOutcome | None:
    if response.status_code == 200:
        response_200 = Bundle.from_dict(response.json())

        return response_200

    if response.status_code == 403:
        response_403 = OperationOutcome.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Bundle | OperationOutcome]:
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
    field_count: int | Unset = 20,
    field_offset: int | Unset = 0,
) -> Response[Bundle | OperationOutcome]:
    """Get resource instance history

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        id (str):
        field_count (int | Unset):  Default: 20.
        field_offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Bundle | OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        resource_type=resource_type,
        id=id,
        field_count=field_count,
        field_offset=field_offset,
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
    field_count: int | Unset = 20,
    field_offset: int | Unset = 0,
) -> Bundle | OperationOutcome | None:
    """Get resource instance history

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        id (str):
        field_count (int | Unset):  Default: 20.
        field_offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Bundle | OperationOutcome
    """

    return sync_detailed(
        tenant_id=tenant_id,
        store_id=store_id,
        resource_type=resource_type,
        id=id,
        client=client,
        field_count=field_count,
        field_offset=field_offset,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    id: str,
    *,
    client: AuthenticatedClient | Client,
    field_count: int | Unset = 20,
    field_offset: int | Unset = 0,
) -> Response[Bundle | OperationOutcome]:
    """Get resource instance history

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        id (str):
        field_count (int | Unset):  Default: 20.
        field_offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Bundle | OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        resource_type=resource_type,
        id=id,
        field_count=field_count,
        field_offset=field_offset,
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
    field_count: int | Unset = 20,
    field_offset: int | Unset = 0,
) -> Bundle | OperationOutcome | None:
    """Get resource instance history

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        id (str):
        field_count (int | Unset):  Default: 20.
        field_offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Bundle | OperationOutcome
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            store_id=store_id,
            resource_type=resource_type,
            id=id,
            client=client,
            field_count=field_count,
            field_offset=field_offset,
        )
    ).parsed
