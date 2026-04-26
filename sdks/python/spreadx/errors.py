from __future__ import annotations

from typing import Any

import httpx


class APIError(Exception):
    """Error returned by a RU-DAX compatible API."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int,
        *,
        category: str | None = None,
        request_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.status_code = status_code
        self.category = category
        self.request_id = request_id
        self.details = details or {}

    @classmethod
    def from_response(cls, response: httpx.Response) -> "APIError":
        try:
            payload = response.json()
            error = payload.get("error", {})
        except ValueError:
            error = {}
        return cls(
            error.get("code", "HTTP_ERROR"),
            error.get("message", response.text),
            response.status_code,
            category=error.get("category"),
            request_id=error.get("request_id"),
            details=error.get("details") or {},
        )

