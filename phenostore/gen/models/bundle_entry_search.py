from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.bundle_entry_search_mode import BundleEntrySearchMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="BundleEntrySearch")


@_attrs_define
class BundleEntrySearch:
    """
    Attributes:
        mode (BundleEntrySearchMode | Unset):
    """

    mode: BundleEntrySearchMode | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mode is not UNSET:
            field_dict["mode"] = mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _mode = d.pop("mode", UNSET)
        mode: BundleEntrySearchMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = BundleEntrySearchMode(_mode)

        bundle_entry_search = cls(
            mode=mode,
        )

        bundle_entry_search.additional_properties = d
        return bundle_entry_search

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
