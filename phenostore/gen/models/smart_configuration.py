from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SmartConfiguration")


@_attrs_define
class SmartConfiguration:
    """
    Attributes:
        token_endpoint (str | Unset):
        grant_types_supported (list[str] | Unset):
        token_endpoint_auth_methods_supported (list[str] | Unset):
        scopes_supported (list[str] | Unset):
        capabilities (list[str] | Unset):
    """

    token_endpoint: str | Unset = UNSET
    grant_types_supported: list[str] | Unset = UNSET
    token_endpoint_auth_methods_supported: list[str] | Unset = UNSET
    scopes_supported: list[str] | Unset = UNSET
    capabilities: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token_endpoint = self.token_endpoint

        grant_types_supported: list[str] | Unset = UNSET
        if not isinstance(self.grant_types_supported, Unset):
            grant_types_supported = self.grant_types_supported

        token_endpoint_auth_methods_supported: list[str] | Unset = UNSET
        if not isinstance(self.token_endpoint_auth_methods_supported, Unset):
            token_endpoint_auth_methods_supported = (
                self.token_endpoint_auth_methods_supported
            )

        scopes_supported: list[str] | Unset = UNSET
        if not isinstance(self.scopes_supported, Unset):
            scopes_supported = self.scopes_supported

        capabilities: list[str] | Unset = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if token_endpoint is not UNSET:
            field_dict["token_endpoint"] = token_endpoint
        if grant_types_supported is not UNSET:
            field_dict["grant_types_supported"] = grant_types_supported
        if token_endpoint_auth_methods_supported is not UNSET:
            field_dict["token_endpoint_auth_methods_supported"] = (
                token_endpoint_auth_methods_supported
            )
        if scopes_supported is not UNSET:
            field_dict["scopes_supported"] = scopes_supported
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        token_endpoint = d.pop("token_endpoint", UNSET)

        grant_types_supported = cast(list[str], d.pop("grant_types_supported", UNSET))

        token_endpoint_auth_methods_supported = cast(
            list[str], d.pop("token_endpoint_auth_methods_supported", UNSET)
        )

        scopes_supported = cast(list[str], d.pop("scopes_supported", UNSET))

        capabilities = cast(list[str], d.pop("capabilities", UNSET))

        smart_configuration = cls(
            token_endpoint=token_endpoint,
            grant_types_supported=grant_types_supported,
            token_endpoint_auth_methods_supported=token_endpoint_auth_methods_supported,
            scopes_supported=scopes_supported,
            capabilities=capabilities,
        )

        smart_configuration.additional_properties = d
        return smart_configuration

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
