from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.json_patch_op import JsonPatchOp
from ..types import UNSET, Unset

T = TypeVar("T", bound="JsonPatchItem")


@_attrs_define
class JsonPatchItem:
    """
    Attributes:
        op (JsonPatchOp): JSON Patch operation type (RFC 6902)
        path (str):
        value (Any | Unset):
        from_ (str | Unset):
    """

    op: JsonPatchOp
    path: str
    value: Any | Unset = UNSET
    from_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        op = self.op.value

        path = self.path

        value = self.value

        from_ = self.from_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "op": op,
                "path": path,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value
        if from_ is not UNSET:
            field_dict["from"] = from_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        op = JsonPatchOp(d.pop("op"))

        path = d.pop("path")

        value = d.pop("value", UNSET)

        from_ = d.pop("from", UNSET)

        json_patch_item = cls(
            op=op,
            path=path,
            value=value,
            from_=from_,
        )

        json_patch_item.additional_properties = d
        return json_patch_item

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
