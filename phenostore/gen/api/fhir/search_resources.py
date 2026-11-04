from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bundle import Bundle
from ...models.operation_outcome import OperationOutcome
from ...models.resource_type import ResourceType
from ...models.search_summary_mode import SearchSummaryMode
from ...models.search_total_mode import SearchTotalMode
from ...types import UNSET, Response, Unset


def _get_kwargs(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    *,
    field_count: int | Unset = 20,
    field_offset: int | Unset = 0,
    field_cursor: str | Unset = UNSET,
    field_total: SearchTotalMode | Unset = UNSET,
    field_summary: SearchSummaryMode | Unset = UNSET,
    field_elements: str | Unset = UNSET,
    field_sort: str | Unset = UNSET,
    field_include: list[str] | Unset = UNSET,
    field_revinclude: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["_count"] = field_count

    params["_offset"] = field_offset

    params["_cursor"] = field_cursor

    json_field_total: str | Unset = UNSET
    if not isinstance(field_total, Unset):
        json_field_total = field_total.value

    params["_total"] = json_field_total

    json_field_summary: str | Unset = UNSET
    if not isinstance(field_summary, Unset):
        json_field_summary = field_summary.value

    params["_summary"] = json_field_summary

    params["_elements"] = field_elements

    params["_sort"] = field_sort

    json_field_include: list[str] | Unset = UNSET
    if not isinstance(field_include, Unset):
        json_field_include = field_include

    params["_include"] = json_field_include

    json_field_revinclude: list[str] | Unset = UNSET
    if not isinstance(field_revinclude, Unset):
        json_field_revinclude = field_revinclude

    params["_revinclude"] = json_field_revinclude

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
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
) -> Bundle | OperationOutcome | None:
    if response.status_code == 200:
        response_200 = Bundle.from_dict(response.json())

        return response_200

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
    *,
    client: AuthenticatedClient | Client,
    field_count: int | Unset = 20,
    field_offset: int | Unset = 0,
    field_cursor: str | Unset = UNSET,
    field_total: SearchTotalMode | Unset = UNSET,
    field_summary: SearchSummaryMode | Unset = UNSET,
    field_elements: str | Unset = UNSET,
    field_sort: str | Unset = UNSET,
    field_include: list[str] | Unset = UNSET,
    field_revinclude: list[str] | Unset = UNSET,
) -> Response[Bundle | OperationOutcome]:
    """Search for FHIR resources

     Searches for resources of the given type. Supports standard FHIR search
    parameters, pagination, sorting, _include/_revinclude, and response shaping.
    Arbitrary FHIR search parameters beyond the named ones below are also accepted,
    including the `:exact` and `:contains` (string) and `:missing` (any type)
    modifiers and chained references (e.g. `subject:Patient.name=Smith`).
    Unrecognized `_`-prefixed control parameters are ignored.

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        field_count (int | Unset):  Default: 20.
        field_offset (int | Unset):  Default: 0.
        field_cursor (str | Unset):
        field_total (SearchTotalMode | Unset): FHIR `_total` mode controlling whether a result
            total is returned. These are the three values defined by FHIR R4. `estimate` is accepted
            but currently behaves like `none` (no total is emitted).
        field_summary (SearchSummaryMode | Unset): Search response summary mode
        field_elements (str | Unset):
        field_sort (str | Unset):
        field_include (list[str] | Unset):
        field_revinclude (list[str] | Unset):

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
        field_count=field_count,
        field_offset=field_offset,
        field_cursor=field_cursor,
        field_total=field_total,
        field_summary=field_summary,
        field_elements=field_elements,
        field_sort=field_sort,
        field_include=field_include,
        field_revinclude=field_revinclude,
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
    field_count: int | Unset = 20,
    field_offset: int | Unset = 0,
    field_cursor: str | Unset = UNSET,
    field_total: SearchTotalMode | Unset = UNSET,
    field_summary: SearchSummaryMode | Unset = UNSET,
    field_elements: str | Unset = UNSET,
    field_sort: str | Unset = UNSET,
    field_include: list[str] | Unset = UNSET,
    field_revinclude: list[str] | Unset = UNSET,
) -> Bundle | OperationOutcome | None:
    """Search for FHIR resources

     Searches for resources of the given type. Supports standard FHIR search
    parameters, pagination, sorting, _include/_revinclude, and response shaping.
    Arbitrary FHIR search parameters beyond the named ones below are also accepted,
    including the `:exact` and `:contains` (string) and `:missing` (any type)
    modifiers and chained references (e.g. `subject:Patient.name=Smith`).
    Unrecognized `_`-prefixed control parameters are ignored.

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        field_count (int | Unset):  Default: 20.
        field_offset (int | Unset):  Default: 0.
        field_cursor (str | Unset):
        field_total (SearchTotalMode | Unset): FHIR `_total` mode controlling whether a result
            total is returned. These are the three values defined by FHIR R4. `estimate` is accepted
            but currently behaves like `none` (no total is emitted).
        field_summary (SearchSummaryMode | Unset): Search response summary mode
        field_elements (str | Unset):
        field_sort (str | Unset):
        field_include (list[str] | Unset):
        field_revinclude (list[str] | Unset):

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
        client=client,
        field_count=field_count,
        field_offset=field_offset,
        field_cursor=field_cursor,
        field_total=field_total,
        field_summary=field_summary,
        field_elements=field_elements,
        field_sort=field_sort,
        field_include=field_include,
        field_revinclude=field_revinclude,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    *,
    client: AuthenticatedClient | Client,
    field_count: int | Unset = 20,
    field_offset: int | Unset = 0,
    field_cursor: str | Unset = UNSET,
    field_total: SearchTotalMode | Unset = UNSET,
    field_summary: SearchSummaryMode | Unset = UNSET,
    field_elements: str | Unset = UNSET,
    field_sort: str | Unset = UNSET,
    field_include: list[str] | Unset = UNSET,
    field_revinclude: list[str] | Unset = UNSET,
) -> Response[Bundle | OperationOutcome]:
    """Search for FHIR resources

     Searches for resources of the given type. Supports standard FHIR search
    parameters, pagination, sorting, _include/_revinclude, and response shaping.
    Arbitrary FHIR search parameters beyond the named ones below are also accepted,
    including the `:exact` and `:contains` (string) and `:missing` (any type)
    modifiers and chained references (e.g. `subject:Patient.name=Smith`).
    Unrecognized `_`-prefixed control parameters are ignored.

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        field_count (int | Unset):  Default: 20.
        field_offset (int | Unset):  Default: 0.
        field_cursor (str | Unset):
        field_total (SearchTotalMode | Unset): FHIR `_total` mode controlling whether a result
            total is returned. These are the three values defined by FHIR R4. `estimate` is accepted
            but currently behaves like `none` (no total is emitted).
        field_summary (SearchSummaryMode | Unset): Search response summary mode
        field_elements (str | Unset):
        field_sort (str | Unset):
        field_include (list[str] | Unset):
        field_revinclude (list[str] | Unset):

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
        field_count=field_count,
        field_offset=field_offset,
        field_cursor=field_cursor,
        field_total=field_total,
        field_summary=field_summary,
        field_elements=field_elements,
        field_sort=field_sort,
        field_include=field_include,
        field_revinclude=field_revinclude,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    store_id: str,
    resource_type: ResourceType,
    *,
    client: AuthenticatedClient | Client,
    field_count: int | Unset = 20,
    field_offset: int | Unset = 0,
    field_cursor: str | Unset = UNSET,
    field_total: SearchTotalMode | Unset = UNSET,
    field_summary: SearchSummaryMode | Unset = UNSET,
    field_elements: str | Unset = UNSET,
    field_sort: str | Unset = UNSET,
    field_include: list[str] | Unset = UNSET,
    field_revinclude: list[str] | Unset = UNSET,
) -> Bundle | OperationOutcome | None:
    """Search for FHIR resources

     Searches for resources of the given type. Supports standard FHIR search
    parameters, pagination, sorting, _include/_revinclude, and response shaping.
    Arbitrary FHIR search parameters beyond the named ones below are also accepted,
    including the `:exact` and `:contains` (string) and `:missing` (any type)
    modifiers and chained references (e.g. `subject:Patient.name=Smith`).
    Unrecognized `_`-prefixed control parameters are ignored.

    Args:
        tenant_id (str):
        store_id (str):
        resource_type (ResourceType): FHIR resource type
        field_count (int | Unset):  Default: 20.
        field_offset (int | Unset):  Default: 0.
        field_cursor (str | Unset):
        field_total (SearchTotalMode | Unset): FHIR `_total` mode controlling whether a result
            total is returned. These are the three values defined by FHIR R4. `estimate` is accepted
            but currently behaves like `none` (no total is emitted).
        field_summary (SearchSummaryMode | Unset): Search response summary mode
        field_elements (str | Unset):
        field_sort (str | Unset):
        field_include (list[str] | Unset):
        field_revinclude (list[str] | Unset):

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
            client=client,
            field_count=field_count,
            field_offset=field_offset,
            field_cursor=field_cursor,
            field_total=field_total,
            field_summary=field_summary,
            field_elements=field_elements,
            field_sort=field_sort,
            field_include=field_include,
            field_revinclude=field_revinclude,
        )
    ).parsed
