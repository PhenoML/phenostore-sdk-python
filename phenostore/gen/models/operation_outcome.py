from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.operation_outcome_resource_type import OperationOutcomeResourceType

if TYPE_CHECKING:
    from ..models.operation_outcome_issue import OperationOutcomeIssue


T = TypeVar("T", bound="OperationOutcome")


@_attrs_define
class OperationOutcome:
    """
    Attributes:
        resource_type (OperationOutcomeResourceType):
        issue (list[OperationOutcomeIssue]):
    """

    resource_type: OperationOutcomeResourceType
    issue: list[OperationOutcomeIssue]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_type = self.resource_type.value

        issue = []
        for issue_item_data in self.issue:
            issue_item = issue_item_data.to_dict()
            issue.append(issue_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resourceType": resource_type,
                "issue": issue,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.operation_outcome_issue import OperationOutcomeIssue  # noqa: PLC0415

        d = dict(src_dict)
        resource_type = OperationOutcomeResourceType(d.pop("resourceType"))

        issue = []
        _issue = d.pop("issue")
        for issue_item_data in _issue:
            issue_item = OperationOutcomeIssue.from_dict(issue_item_data)

            issue.append(issue_item)

        operation_outcome = cls(
            resource_type=resource_type,
            issue=issue,
        )

        operation_outcome.additional_properties = d
        return operation_outcome

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
