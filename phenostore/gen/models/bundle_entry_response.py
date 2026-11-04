from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BundleEntryResponse")


@_attrs_define
class BundleEntryResponse:
    """
    Attributes:
        status (str | Unset):
        location (str | Unset):
        etag (str | Unset):
        last_modified (str | Unset):
        outcome (Any | Unset): OperationOutcome for this entry (arbitrary JSON).
    """

    status: str | Unset = UNSET
    location: str | Unset = UNSET
    etag: str | Unset = UNSET
    last_modified: str | Unset = UNSET
    outcome: Any | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        location = self.location

        etag = self.etag

        last_modified = self.last_modified

        outcome = self.outcome

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if location is not UNSET:
            field_dict["location"] = location
        if etag is not UNSET:
            field_dict["etag"] = etag
        if last_modified is not UNSET:
            field_dict["lastModified"] = last_modified
        if outcome is not UNSET:
            field_dict["outcome"] = outcome

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = d.pop("status", UNSET)

        location = d.pop("location", UNSET)

        etag = d.pop("etag", UNSET)

        last_modified = d.pop("lastModified", UNSET)

        outcome = d.pop("outcome", UNSET)

        bundle_entry_response = cls(
            status=status,
            location=location,
            etag=etag,
            last_modified=last_modified,
            outcome=outcome,
        )

        bundle_entry_response.additional_properties = d
        return bundle_entry_response

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
