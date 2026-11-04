import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bundle import Bundle
from ...models.operation_outcome import OperationOutcome
from ...models.search_total_mode import SearchTotalMode
from ...types import UNSET, Response, Unset


def _get_kwargs(
    tenant_id: str,
    store_id: str,
    *,
    patient: str,
    start: datetime.date | Unset = UNSET,
    end: datetime.date | Unset = UNSET,
    type_: str | Unset = UNSET,
    field_total: SearchTotalMode | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["patient"] = patient

    json_start: str | Unset = UNSET
    if not isinstance(start, Unset):
        json_start = start.isoformat()
    params["start"] = json_start

    json_end: str | Unset = UNSET
    if not isinstance(end, Unset):
        json_end = end.isoformat()
    params["end"] = json_end

    params["type"] = type_

    json_field_total: str | Unset = UNSET
    if not isinstance(field_total, Unset):
        json_field_total = field_total.value

    params["_total"] = json_field_total

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/tenants/{tenant_id}/stores/{store_id}/DocumentReference/$docref".format(
            tenant_id=quote(str(tenant_id), safe=""),
            store_id=quote(str(store_id), safe=""),
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
    *,
    client: AuthenticatedClient | Client,
    patient: str,
    start: datetime.date | Unset = UNSET,
    end: datetime.date | Unset = UNSET,
    type_: str | Unset = UNSET,
    field_total: SearchTotalMode | Unset = UNSET,
) -> Response[Bundle | OperationOutcome]:
    """US Core $docref operation (GET)

    Args:
        tenant_id (str):
        store_id (str):
        patient (str):
        start (datetime.date | Unset):
        end (datetime.date | Unset):
        type_ (str | Unset):
        field_total (SearchTotalMode | Unset): FHIR `_total` mode controlling whether a result
            total is returned. These are the three values defined by FHIR R4. `estimate` is accepted
            but currently behaves like `none` (no total is emitted).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Bundle | OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        patient=patient,
        start=start,
        end=end,
        type_=type_,
        field_total=field_total,
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
    patient: str,
    start: datetime.date | Unset = UNSET,
    end: datetime.date | Unset = UNSET,
    type_: str | Unset = UNSET,
    field_total: SearchTotalMode | Unset = UNSET,
) -> Bundle | OperationOutcome | None:
    """US Core $docref operation (GET)

    Args:
        tenant_id (str):
        store_id (str):
        patient (str):
        start (datetime.date | Unset):
        end (datetime.date | Unset):
        type_ (str | Unset):
        field_total (SearchTotalMode | Unset): FHIR `_total` mode controlling whether a result
            total is returned. These are the three values defined by FHIR R4. `estimate` is accepted
            but currently behaves like `none` (no total is emitted).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Bundle | OperationOutcome
    """

    return sync_detailed(
        tenant_id=tenant_id,
        store_id=store_id,
        client=client,
        patient=patient,
        start=start,
        end=end,
        type_=type_,
        field_total=field_total,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    store_id: str,
    *,
    client: AuthenticatedClient | Client,
    patient: str,
    start: datetime.date | Unset = UNSET,
    end: datetime.date | Unset = UNSET,
    type_: str | Unset = UNSET,
    field_total: SearchTotalMode | Unset = UNSET,
) -> Response[Bundle | OperationOutcome]:
    """US Core $docref operation (GET)

    Args:
        tenant_id (str):
        store_id (str):
        patient (str):
        start (datetime.date | Unset):
        end (datetime.date | Unset):
        type_ (str | Unset):
        field_total (SearchTotalMode | Unset): FHIR `_total` mode controlling whether a result
            total is returned. These are the three values defined by FHIR R4. `estimate` is accepted
            but currently behaves like `none` (no total is emitted).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Bundle | OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        patient=patient,
        start=start,
        end=end,
        type_=type_,
        field_total=field_total,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    store_id: str,
    *,
    client: AuthenticatedClient | Client,
    patient: str,
    start: datetime.date | Unset = UNSET,
    end: datetime.date | Unset = UNSET,
    type_: str | Unset = UNSET,
    field_total: SearchTotalMode | Unset = UNSET,
) -> Bundle | OperationOutcome | None:
    """US Core $docref operation (GET)

    Args:
        tenant_id (str):
        store_id (str):
        patient (str):
        start (datetime.date | Unset):
        end (datetime.date | Unset):
        type_ (str | Unset):
        field_total (SearchTotalMode | Unset): FHIR `_total` mode controlling whether a result
            total is returned. These are the three values defined by FHIR R4. `estimate` is accepted
            but currently behaves like `none` (no total is emitted).

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
            client=client,
            patient=patient,
            start=start,
            end=end,
            type_=type_,
            field_total=field_total,
        )
    ).parsed
