from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.bulk_operation_status_code import BulkOperationStatusCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkOperationStatus")


@_attrs_define
class BulkOperationStatus:
    """
    Attributes:
        id (str):
        status (BulkOperationStatusCode): Bulk operation lifecycle status
        total_count (int):
        processed_count (int):
        error_count (int):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        result (Any | Unset): Result Bundle (present when status is completed).
    """

    id: str
    status: BulkOperationStatusCode
    total_count: int
    processed_count: int
    error_count: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    result: Any | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        total_count = self.total_count

        processed_count = self.processed_count

        error_count = self.error_count

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        result = self.result

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "total_count": total_count,
                "processed_count": processed_count,
                "error_count": error_count,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        status = BulkOperationStatusCode(d.pop("status"))

        total_count = d.pop("total_count")

        processed_count = d.pop("processed_count")

        error_count = d.pop("error_count")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        result = d.pop("result", UNSET)

        bulk_operation_status = cls(
            id=id,
            status=status,
            total_count=total_count,
            processed_count=processed_count,
            error_count=error_count,
            created_at=created_at,
            updated_at=updated_at,
            result=result,
        )

        bulk_operation_status.additional_properties = d
        return bulk_operation_status

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
