from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.issue_token_body_grant_type import IssueTokenBodyGrantType
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTokenBody")


@_attrs_define
class IssueTokenBody:
    """
    Attributes:
        grant_type (IssueTokenBodyGrantType):
        client_id (str | Unset): Required when credentials are not sent via HTTP Basic auth.
        client_secret (str | Unset): Required when credentials are not sent via HTTP Basic auth.
        scope (str | Unset): Space-delimited list of requested scopes (subset of granted permissions)
    """

    grant_type: IssueTokenBodyGrantType
    client_id: str | Unset = UNSET
    client_secret: str | Unset = UNSET
    scope: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        grant_type = self.grant_type.value

        client_id = self.client_id

        client_secret = self.client_secret

        scope = self.scope

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "grant_type": grant_type,
            }
        )
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        grant_type = IssueTokenBodyGrantType(d.pop("grant_type"))

        client_id = d.pop("client_id", UNSET)

        client_secret = d.pop("client_secret", UNSET)

        scope = d.pop("scope", UNSET)

        issue_token_body = cls(
            grant_type=grant_type,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
        )

        issue_token_body.additional_properties = d
        return issue_token_body

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
