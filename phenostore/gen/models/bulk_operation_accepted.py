from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.bulk_operation_accepted_status import BulkOperationAcceptedStatus

T = TypeVar("T", bound="BulkOperationAccepted")


@_attrs_define
class BulkOperationAccepted:
    """
    Attributes:
        id (str):
        status (BulkOperationAcceptedStatus):
        total (int):
    """

    id: str
    status: BulkOperationAcceptedStatus
    total: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        status = BulkOperationAcceptedStatus(d.pop("status"))

        total = d.pop("total")

        bulk_operation_accepted = cls(
            id=id,
            status=status,
            total=total,
        )

        bulk_operation_accepted.additional_properties = d
        return bulk_operation_accepted

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
