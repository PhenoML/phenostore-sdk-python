"""Errors raised by the convenience clients."""

from __future__ import annotations

import json
from typing import Any

import httpx


class OperationOutcomeError(Exception):
    """An API error, retaining the HTTP response and unmodified response bytes."""

    def __init__(self, response: httpx.Response) -> None:
        self.response = response
        self.status_code = response.status_code
        self.body = response.content
        self.outcome: dict[str, Any] | None = None
        message = f"phenostore: HTTP {self.status_code}"
        try:
            parsed = response.json()
        except (ValueError, UnicodeError):
            parsed = None
        if isinstance(parsed, dict):
            self.outcome = parsed
            issues = parsed.get("issue")
            if isinstance(issues, list) and issues and isinstance(issues[0], dict):
                issue = issues[0]
                message = "[{}/{}] {}".format(
                    issue.get("severity", ""), issue.get("code", ""), issue.get("diagnostics", "")
                )
        super().__init__(message)


class AuthenticationError(Exception):
    """Token exchange failed or returned an invalid token response."""

    def __init__(self, response: httpx.Response, message: str = "token exchange failed") -> None:
        self.response = response
        self.status_code = response.status_code
        self.body = response.content
        # Avoid putting credentials or token response bodies in exception messages.
        super().__init__(f"phenostore: {message} (HTTP {self.status_code})")


class InvalidResponseError(ValueError):
    """A successful API response did not contain a JSON object."""

    def __init__(self, response: httpx.Response) -> None:
        self.response = response
        super().__init__(f"phenostore: expected a JSON object (HTTP {response.status_code})")


def _has_status(error: BaseException | None, status: int) -> bool:
    seen: set[int] = set()
    while error is not None and id(error) not in seen:
        seen.add(id(error))
        if isinstance(error, OperationOutcomeError):
            return error.status_code == status
        error = error.__cause__ or error.__context__
    return False


def is_not_found(error: BaseException | None) -> bool:
    """Return whether an error (including chained exceptions) represents HTTP 404."""
    return _has_status(error, 404)


def is_gone(error: BaseException | None) -> bool:
    """Return whether an error represents HTTP 410."""
    return _has_status(error, 410)


def is_conflict(error: BaseException | None) -> bool:
    """Return whether an error represents HTTP 412 (a failed precondition)."""
    return _has_status(error, 412)


def is_forbidden(error: BaseException | None) -> bool:
    """Return whether an error represents HTTP 403."""
    return _has_status(error, 403)


def _json_object(response: httpx.Response) -> dict[str, Any]:
    if not 200 <= response.status_code < 300:
        raise OperationOutcomeError(response)
    try:
        result = response.json()
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise InvalidResponseError(response) from exc
    if not isinstance(result, dict):
        raise InvalidResponseError(response)
    return result
