from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.operation_outcome import OperationOutcome
from ...models.resource_type import ResourceType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    *,
    field_id: str | Unset = UNSET,
    field_last_updated: str | Unset = UNSET,
    identifier: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["_id"] = field_id

    params["_lastUpdated"] = field_last_updated

    params["identifier"] = identifier

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/tenants/{tenant_id}/stores/{store_id}/{resource_type}".format(
            tenant_id=quote(str(tenant_id), safe=""),
            store_id=quote(str(store_id), safe=""),
            resource_type=quote(str(resource_type), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | OperationOutcome | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = OperationOutcome.from_dict(response.json())

        return response_400

    if response.status_code == 403:
        response_403 = OperationOutcome.from_dict(response.json())

        return response_403

    if response.status_code == 412:
        response_412 = OperationOutcome.from_dict(response.json())

        return response_412

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | OperationOutcome]:
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
    field_id: str | Unset = UNSET,
    field_last_updated: str | Unset = UNSET,
    identifier: str | Unset = UNSET,
) -> Response[Any | OperationOutcome]:
    """Conditionally delete a FHIR resource

     Deletes a resource matching the given search criteria.
    0 matches → 204, 1 match → delete + 204, 2+ matches → 412.
    Requires at least one search parameter. Pass FHIR search parameters
    as query parameters (e.g. ?identifier=http://example.com|123).
    Any resource-type-specific search parameter is accepted in addition
    to the common parameters listed below.

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        field_id (str | Unset):
        field_last_updated (str | Unset):
        identifier (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        resource_type=resource_type,
        field_id=field_id,
        field_last_updated=field_last_updated,
        identifier=identifier,
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
    field_id: str | Unset = UNSET,
    field_last_updated: str | Unset = UNSET,
    identifier: str | Unset = UNSET,
) -> Any | OperationOutcome | None:
    """Conditionally delete a FHIR resource

     Deletes a resource matching the given search criteria.
    0 matches → 204, 1 match → delete + 204, 2+ matches → 412.
    Requires at least one search parameter. Pass FHIR search parameters
    as query parameters (e.g. ?identifier=http://example.com|123).
    Any resource-type-specific search parameter is accepted in addition
    to the common parameters listed below.

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        field_id (str | Unset):
        field_last_updated (str | Unset):
        identifier (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | OperationOutcome
    """

    return sync_detailed(
        tenant_id=tenant_id,
        store_id=store_id,
        resource_type=resource_type,
        client=client,
        field_id=field_id,
        field_last_updated=field_last_updated,
        identifier=identifier,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    *,
    client: AuthenticatedClient | Client,
    field_id: str | Unset = UNSET,
    field_last_updated: str | Unset = UNSET,
    identifier: str | Unset = UNSET,
) -> Response[Any | OperationOutcome]:
    """Conditionally delete a FHIR resource

     Deletes a resource matching the given search criteria.
    0 matches → 204, 1 match → delete + 204, 2+ matches → 412.
    Requires at least one search parameter. Pass FHIR search parameters
    as query parameters (e.g. ?identifier=http://example.com|123).
    Any resource-type-specific search parameter is accepted in addition
    to the common parameters listed below.

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        field_id (str | Unset):
        field_last_updated (str | Unset):
        identifier (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        resource_type=resource_type,
        field_id=field_id,
        field_last_updated=field_last_updated,
        identifier=identifier,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    *,
    client: AuthenticatedClient | Client,
    field_id: str | Unset = UNSET,
    field_last_updated: str | Unset = UNSET,
    identifier: str | Unset = UNSET,
) -> Any | OperationOutcome | None:
    """Conditionally delete a FHIR resource

     Deletes a resource matching the given search criteria.
    0 matches → 204, 1 match → delete + 204, 2+ matches → 412.
    Requires at least one search parameter. Pass FHIR search parameters
    as query parameters (e.g. ?identifier=http://example.com|123).
    Any resource-type-specific search parameter is accepted in addition
    to the common parameters listed below.

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        field_id (str | Unset):
        field_last_updated (str | Unset):
        identifier (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | OperationOutcome
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            store_id=store_id,
            resource_type=resource_type,
            client=client,
            field_id=field_id,
            field_last_updated=field_last_updated,
            identifier=identifier,
        )
    ).parsed
