from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.bundle_entry_request import BundleEntryRequest
    from ..models.bundle_entry_response import BundleEntryResponse
    from ..models.bundle_entry_search import BundleEntrySearch


T = TypeVar("T", bound="BundleEntry")


@_attrs_define
class BundleEntry:
    """
    Attributes:
        full_url (str | Unset):
        resource (Any | Unset): The resource content (arbitrary FHIR resource JSON).
        search (BundleEntrySearch | Unset):
        request (BundleEntryRequest | Unset):
        response (BundleEntryResponse | Unset):
    """

    full_url: str | Unset = UNSET
    resource: Any | Unset = UNSET
    search: BundleEntrySearch | Unset = UNSET
    request: BundleEntryRequest | Unset = UNSET
    response: BundleEntryResponse | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        full_url = self.full_url

        resource = self.resource

        search: dict[str, Any] | Unset = UNSET
        if not isinstance(self.search, Unset):
            search = self.search.to_dict()

        request: dict[str, Any] | Unset = UNSET
        if not isinstance(self.request, Unset):
            request = self.request.to_dict()

        response: dict[str, Any] | Unset = UNSET
        if not isinstance(self.response, Unset):
            response = self.response.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if full_url is not UNSET:
            field_dict["fullUrl"] = full_url
        if resource is not UNSET:
            field_dict["resource"] = resource
        if search is not UNSET:
            field_dict["search"] = search
        if request is not UNSET:
            field_dict["request"] = request
        if response is not UNSET:
            field_dict["response"] = response

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bundle_entry_request import BundleEntryRequest  # noqa: PLC0415
        from ..models.bundle_entry_response import BundleEntryResponse  # noqa: PLC0415
        from ..models.bundle_entry_search import BundleEntrySearch  # noqa: PLC0415

        d = dict(src_dict)
        full_url = d.pop("fullUrl", UNSET)

        resource = d.pop("resource", UNSET)

        _search = d.pop("search", UNSET)
        search: BundleEntrySearch | Unset
        if isinstance(_search, Unset):
            search = UNSET
        else:
            search = BundleEntrySearch.from_dict(_search)

        _request = d.pop("request", UNSET)
        request: BundleEntryRequest | Unset
        if isinstance(_request, Unset):
            request = UNSET
        else:
            request = BundleEntryRequest.from_dict(_request)

        _response = d.pop("response", UNSET)
        response: BundleEntryResponse | Unset
        if isinstance(_response, Unset):
            response = UNSET
        else:
            response = BundleEntryResponse.from_dict(_response)

        bundle_entry = cls(
            full_url=full_url,
            resource=resource,
            search=search,
            request=request,
            response=response,
        )

        bundle_entry.additional_properties = d
        return bundle_entry

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
