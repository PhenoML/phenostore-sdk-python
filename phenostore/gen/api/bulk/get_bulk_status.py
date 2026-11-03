from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bulk_operation_status import BulkOperationStatus
from ...models.operation_outcome import OperationOutcome
from ...types import Response


def _get_kwargs(
    tenant_id: str,
    store_id: str,
    op_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/tenants/{tenant_id}/stores/{store_id}/$bulk/{op_id}".format(
            tenant_id=quote(str(tenant_id), safe=""),
            store_id=quote(str(store_id), safe=""),
            op_id=quote(str(op_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BulkOperationStatus | OperationOutcome | None:
    if response.status_code == 200:
        response_200 = BulkOperationStatus.from_dict(response.json())

        return response_200

    if response.status_code == 202:
        response_202 = BulkOperationStatus.from_dict(response.json())

        return response_202

    if response.status_code == 404:
        response_404 = OperationOutcome.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BulkOperationStatus | OperationOutcome]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tenant_id: str,
    store_id: str,
    op_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[BulkOperationStatus | OperationOutcome]:
    """Get bulk operation status

    Args:
        tenant_id (str):
        store_id (str):
        op_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BulkOperationStatus | OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        op_id=op_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tenant_id: str,
    store_id: str,
    op_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> BulkOperationStatus | OperationOutcome | None:
    """Get bulk operation status

    Args:
        tenant_id (str):
        store_id (str):
        op_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BulkOperationStatus | OperationOutcome
    """

    return sync_detailed(
        tenant_id=tenant_id,
        store_id=store_id,
        op_id=op_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    store_id: str,
    op_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[BulkOperationStatus | OperationOutcome]:
    """Get bulk operation status

    Args:
        tenant_id (str):
        store_id (str):
        op_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BulkOperationStatus | OperationOutcome]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
        op_id=op_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    store_id: str,
    op_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> BulkOperationStatus | OperationOutcome | None:
    """Get bulk operation status

    Args:
        tenant_id (str):
        store_id (str):
        op_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BulkOperationStatus | OperationOutcome
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            store_id=store_id,
            op_id=op_id,
            client=client,
        )
    ).parsed
