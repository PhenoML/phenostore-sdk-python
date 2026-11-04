from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.bundle_resource_type import BundleResourceType
from ..models.bundle_type import BundleType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.bundle_entry import BundleEntry
    from ..models.bundle_link import BundleLink


T = TypeVar("T", bound="Bundle")


@_attrs_define
class Bundle:
    """
    Attributes:
        resource_type (BundleResourceType):
        type_ (BundleType): FHIR Bundle type
        total (int | Unset):
        link (list[BundleLink] | Unset):
        entry (list[BundleEntry] | Unset):
    """

    resource_type: BundleResourceType
    type_: BundleType
    total: int | Unset = UNSET
    link: list[BundleLink] | Unset = UNSET
    entry: list[BundleEntry] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_type = self.resource_type.value

        type_ = self.type_.value

        total = self.total

        link: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.link, Unset):
            link = []
            for link_item_data in self.link:
                link_item = link_item_data.to_dict()
                link.append(link_item)

        entry: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.entry, Unset):
            entry = []
            for entry_item_data in self.entry:
                entry_item = entry_item_data.to_dict()
                entry.append(entry_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resourceType": resource_type,
                "type": type_,
            }
        )
        if total is not UNSET:
            field_dict["total"] = total
        if link is not UNSET:
            field_dict["link"] = link
        if entry is not UNSET:
            field_dict["entry"] = entry

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bundle_entry import BundleEntry  # noqa: PLC0415
        from ..models.bundle_link import BundleLink  # noqa: PLC0415

        d = dict(src_dict)
        resource_type = BundleResourceType(d.pop("resourceType"))

        type_ = BundleType(d.pop("type"))

        total = d.pop("total", UNSET)

        _link = d.pop("link", UNSET)
        link: list[BundleLink] | Unset = UNSET
        if _link is not UNSET:
            link = []
            for link_item_data in _link:
                link_item = BundleLink.from_dict(link_item_data)

                link.append(link_item)

        _entry = d.pop("entry", UNSET)
        entry: list[BundleEntry] | Unset = UNSET
        if _entry is not UNSET:
            entry = []
            for entry_item_data in _entry:
                entry_item = BundleEntry.from_dict(entry_item_data)

                entry.append(entry_item)

        bundle = cls(
            resource_type=resource_type,
            type_=type_,
            total=total,
            link=link,
            entry=entry,
        )

        bundle.additional_properties = d
        return bundle

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
