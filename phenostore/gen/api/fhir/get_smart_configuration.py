from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.smart_configuration import SmartConfiguration
from ...types import Response


def _get_kwargs(
    tenant_id: str,
    store_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/tenants/{tenant_id}/stores/{store_id}/.well-known/smart-configuration".format(
            tenant_id=quote(str(tenant_id), safe=""),
            store_id=quote(str(store_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> SmartConfiguration | None:
    if response.status_code == 200:
        response_200 = SmartConfiguration.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[SmartConfiguration]:
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
) -> Response[SmartConfiguration]:
    """SMART on FHIR well-known configuration

    Args:
        tenant_id (str):
        store_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SmartConfiguration]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
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
) -> SmartConfiguration | None:
    """SMART on FHIR well-known configuration

    Args:
        tenant_id (str):
        store_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SmartConfiguration
    """

    return sync_detailed(
        tenant_id=tenant_id,
        store_id=store_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    tenant_id: str,
    store_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[SmartConfiguration]:
    """SMART on FHIR well-known configuration

    Args:
        tenant_id (str):
        store_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SmartConfiguration]
    """

    kwargs = _get_kwargs(
        tenant_id=tenant_id,
        store_id=store_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tenant_id: str,
    store_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> SmartConfiguration | None:
    """SMART on FHIR well-known configuration

    Args:
        tenant_id (str):
        store_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SmartConfiguration
    """

    return (
        await asyncio_detailed(
            tenant_id=tenant_id,
            store_id=store_id,
            client=client,
        )
    ).parsed
