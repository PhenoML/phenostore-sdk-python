from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.search_total_mode import SearchTotalMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="PostDocrefBody")


@_attrs_define
class PostDocrefBody:
    """
    Attributes:
        patient (str): Patient reference
        start (datetime.date | Unset): Period start date
        end (datetime.date | Unset): Period end date
        type_ (str | Unset): Document type (CodeableConcept token)
        field_total (SearchTotalMode | Unset): FHIR `_total` mode controlling whether a result total is returned. These
            are the three values defined by FHIR R4. `estimate` is accepted but currently behaves like `none` (no total is
            emitted).
    """

    patient: str
    start: datetime.date | Unset = UNSET
    end: datetime.date | Unset = UNSET
    type_: str | Unset = UNSET
    field_total: SearchTotalMode | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        patient = self.patient

        start: str | Unset = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat()

        end: str | Unset = UNSET
        if not isinstance(self.end, Unset):
            end = self.end.isoformat()

        type_ = self.type_

        field_total: str | Unset = UNSET
        if not isinstance(self.field_total, Unset):
            field_total = self.field_total.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "patient": patient,
            }
        )
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if type_ is not UNSET:
            field_dict["type"] = type_
        if field_total is not UNSET:
            field_dict["_total"] = field_total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        patient = d.pop("patient")

        _start = d.pop("start", UNSET)
        start: datetime.date | Unset
        if isinstance(_start, Unset):
            start = UNSET
        else:
            start = datetime.date.fromisoformat(_start)

        _end = d.pop("end", UNSET)
        end: datetime.date | Unset
        if isinstance(_end, Unset):
            end = UNSET
        else:
            end = datetime.date.fromisoformat(_end)

        type_ = d.pop("type", UNSET)

        _field_total = d.pop("_total", UNSET)
        field_total: SearchTotalMode | Unset
        if isinstance(_field_total, Unset):
            field_total = UNSET
        else:
            field_total = SearchTotalMode(_field_total)

        post_docref_body = cls(
            patient=patient,
            start=start,
            end=end,
            type_=type_,
            field_total=field_total,
        )

        post_docref_body.additional_properties = d
        return post_docref_body

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
