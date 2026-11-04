from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.search_summary_mode import SearchSummaryMode
from ..models.search_total_mode import SearchTotalMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchResourcesPostBody")


@_attrs_define
class SearchResourcesPostBody:
    """
    Attributes:
        field_count (int | Unset):
        field_offset (int | Unset):
        field_cursor (str | Unset):
        field_total (SearchTotalMode | Unset): FHIR `_total` mode controlling whether a result total is returned. These
            are the three values defined by FHIR R4. `estimate` is accepted but currently behaves like `none` (no total is
            emitted).
        field_summary (SearchSummaryMode | Unset): Search response summary mode
        field_elements (str | Unset):
        field_sort (str | Unset):
        field_include (list[str] | Unset):
        field_revinclude (list[str] | Unset):
    """

    field_count: int | Unset = UNSET
    field_offset: int | Unset = UNSET
    field_cursor: str | Unset = UNSET
    field_total: SearchTotalMode | Unset = UNSET
    field_summary: SearchSummaryMode | Unset = UNSET
    field_elements: str | Unset = UNSET
    field_sort: str | Unset = UNSET
    field_include: list[str] | Unset = UNSET
    field_revinclude: list[str] | Unset = UNSET
    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_count = self.field_count

        field_offset = self.field_offset

        field_cursor = self.field_cursor

        field_total: str | Unset = UNSET
        if not isinstance(self.field_total, Unset):
            field_total = self.field_total.value

        field_summary: str | Unset = UNSET
        if not isinstance(self.field_summary, Unset):
            field_summary = self.field_summary.value

        field_elements = self.field_elements

        field_sort = self.field_sort

        field_include: list[str] | Unset = UNSET
        if not isinstance(self.field_include, Unset):
            field_include = self.field_include

        field_revinclude: list[str] | Unset = UNSET
        if not isinstance(self.field_revinclude, Unset):
            field_revinclude = self.field_revinclude

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_count is not UNSET:
            field_dict["_count"] = field_count
        if field_offset is not UNSET:
            field_dict["_offset"] = field_offset
        if field_cursor is not UNSET:
            field_dict["_cursor"] = field_cursor
        if field_total is not UNSET:
            field_dict["_total"] = field_total
        if field_summary is not UNSET:
            field_dict["_summary"] = field_summary
        if field_elements is not UNSET:
            field_dict["_elements"] = field_elements
        if field_sort is not UNSET:
            field_dict["_sort"] = field_sort
        if field_include is not UNSET:
            field_dict["_include"] = field_include
        if field_revinclude is not UNSET:
            field_dict["_revinclude"] = field_revinclude

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field_count = d.pop("_count", UNSET)

        field_offset = d.pop("_offset", UNSET)

        field_cursor = d.pop("_cursor", UNSET)

        _field_total = d.pop("_total", UNSET)
        field_total: SearchTotalMode | Unset
        if isinstance(_field_total, Unset):
            field_total = UNSET
        else:
            field_total = SearchTotalMode(_field_total)

        _field_summary = d.pop("_summary", UNSET)
        field_summary: SearchSummaryMode | Unset
        if isinstance(_field_summary, Unset):
            field_summary = UNSET
        else:
            field_summary = SearchSummaryMode(_field_summary)

        field_elements = d.pop("_elements", UNSET)

        field_sort = d.pop("_sort", UNSET)

        field_include = cast(list[str], d.pop("_include", UNSET))

        field_revinclude = cast(list[str], d.pop("_revinclude", UNSET))

        search_resources_post_body = cls(
            field_count=field_count,
            field_offset=field_offset,
            field_cursor=field_cursor,
            field_total=field_total,
            field_summary=field_summary,
            field_elements=field_elements,
            field_sort=field_sort,
            field_include=field_include,
            field_revinclude=field_revinclude,
        )

        search_resources_post_body.additional_properties = d
        return search_resources_post_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
