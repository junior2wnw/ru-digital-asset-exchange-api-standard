from __future__ import annotations

import httpx

from conftest import assert_error_envelope


def test_l0_time_endpoint(client: httpx.Client) -> None:
    response = client.get("/v1/time")
    assert response.status_code == 200
    assert isinstance(response.json()["server_time"], str)


def test_l0_profile_endpoint(client: httpx.Client) -> None:
    response = client.get("/v1/profile")
    assert response.status_code == 200
    payload = response.json()
    assert payload["profile_id"] == "ru-dmip"
    assert payload["jurisdiction"] == "RU"
    assert "L0" in payload["compatibility_levels"]
    assert "L5" in payload["compatibility_levels"]
    assert payload["operator_roles"]
    assert "crypto_exchange" in payload["operator_roles"]
    assert "digital_depository" in payload["operator_roles"]
    assert payload["capabilities"]
    capability_ids = {item["capability_id"] for item in payload["capabilities"]}
    assert "execution_semantics" in capability_ids
    assert "event_replay" in capability_ids
    assert "entitlements" in capability_ids
    assert "strong_authentication" in capability_ids
    assert "authorization_policy" in capability_ids
    assert "crypto_circulation" in capability_ids
    crypto_capability = next(
        item for item in payload["capabilities"] if item["capability_id"] == "crypto_circulation"
    )
    assert crypto_capability["status"] == "sandbox_only"
    assert payload["legal_profiles"]
    framework_ids = {item["framework_id"] for item in payload["legal_profiles"]}
    assert "ru-crypto-circulation-2026" in framework_ids
    assert payload["data_governance"]["audit_trail_required"] is True
    assert payload["extensions"]["public_name"] == "RU Digital Market Interoperability Profile"


def test_l0_instruments_endpoint(client: httpx.Client) -> None:
    response = client.get("/v1/instruments")
    assert response.status_code == 200
    items = response.json()["items"]
    assert items
    first = items[0]
    for field in [
        "instrument_id",
        "symbol",
        "type",
        "base_asset",
        "quote_asset",
        "status",
        "price_tick",
        "quantity_step",
        "min_quantity",
        "max_quantity",
        "min_notional",
    ]:
        assert field in first


def test_l0_standard_error_envelope(client: httpx.Client) -> None:
    response = client.get("/v1/instruments/UNKNOWN")
    assert response.status_code == 404
    assert_error_envelope(response.json())

    missing_route = client.get("/v1/not-a-route")
    assert missing_route.status_code == 404
    assert missing_route.json()["error"]["code"] == "RESOURCE_NOT_FOUND"
    assert_error_envelope(missing_route.json())

    invalid_request = client.get("/v1/market/orderbook")
    assert invalid_request.status_code == 422
    assert invalid_request.json()["error"]["code"] == "INVALID_REQUEST"
    assert_error_envelope(invalid_request.json())

    method_not_allowed = client.post("/v1/time")
    assert method_not_allowed.status_code == 405
    assert method_not_allowed.json()["error"]["code"] == "METHOD_NOT_ALLOWED"
    assert_error_envelope(method_not_allowed.json())
