from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timezone
from urllib.parse import quote

import httpx
import pytest


class HmacRequestAuth(httpx.Auth):
    requires_request_body = True

    def __init__(self, api_secret: str) -> None:
        self.api_secret = api_secret

    def auth_flow(self, request: httpx.Request):
        if "X-API-Key" in request.headers and "X-Signature" not in request.headers:
            timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            encoded_query = [
                (quote(key, safe="~-._"), quote(value, safe="~-._"))
                for key, value in request.url.params.multi_items()
            ]
            canonical_query = "&".join(f"{key}={value}" for key, value in sorted(encoded_query))
            body_hash = hashlib.sha256(request.content).hexdigest()
            payload = f"{timestamp}{request.method.upper()}{request.url.path}{canonical_query}{body_hash}"
            request.headers["X-Timestamp"] = timestamp
            request.headers["X-Signature"] = hmac.new(
                self.api_secret.encode(),
                payload.encode(),
                hashlib.sha256,
            ).hexdigest()
        yield request


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--base-url", default="http://127.0.0.1:8080")
    parser.addoption("--api-key", default="sandbox-key")
    parser.addoption("--api-secret", default="sandbox-secret")


@pytest.fixture
def base_url(request: pytest.FixtureRequest) -> str:
    return str(request.config.getoption("--base-url")).rstrip("/")


@pytest.fixture
def api_key(request: pytest.FixtureRequest) -> str:
    return str(request.config.getoption("--api-key"))


@pytest.fixture
def api_secret(request: pytest.FixtureRequest) -> str:
    return str(request.config.getoption("--api-secret"))


@pytest.fixture
def client(base_url: str, api_secret: str) -> httpx.Client:
    with httpx.Client(base_url=base_url, timeout=10.0, auth=HmacRequestAuth(api_secret)) as http_client:
        yield http_client


@pytest.fixture
def unsigned_client(base_url: str) -> httpx.Client:
    with httpx.Client(base_url=base_url, timeout=10.0) as http_client:
        yield http_client


@pytest.fixture
def auth_headers(api_key: str) -> dict[str, str]:
    return {"X-API-Key": api_key}


def assert_error_envelope(payload: dict[str, object]) -> None:
    assert "error" in payload
    error = payload["error"]
    assert isinstance(error, dict)
    assert isinstance(error.get("code"), str)
    assert isinstance(error.get("message"), str)
    assert isinstance(error.get("category"), str)
    assert isinstance(error.get("request_id"), str)
