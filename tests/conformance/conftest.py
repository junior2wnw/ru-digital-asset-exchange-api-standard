from __future__ import annotations

import httpx
import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--base-url", default="http://127.0.0.1:8080")
    parser.addoption("--api-key", default="sandbox-key")


@pytest.fixture
def base_url(request: pytest.FixtureRequest) -> str:
    return str(request.config.getoption("--base-url")).rstrip("/")


@pytest.fixture
def api_key(request: pytest.FixtureRequest) -> str:
    return str(request.config.getoption("--api-key"))


@pytest.fixture
def client(base_url: str) -> httpx.Client:
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

