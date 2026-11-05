"""Python SDK for the Phenostore FHIR data API."""

from .client import AsyncClient, Client
from .errors import (
    AuthenticationError,
    InvalidResponseError,
    OperationOutcomeError,
    is_conflict,
    is_forbidden,
    is_gone,
    is_not_found,
)

__version__ = "0.1.2"  # x-release-please-version

__all__ = [
    "AsyncClient",
    "AuthenticationError",
    "Client",
    "InvalidResponseError",
    "OperationOutcomeError",
    "is_conflict",
    "is_forbidden",
    "is_gone",
    "is_not_found",
]
