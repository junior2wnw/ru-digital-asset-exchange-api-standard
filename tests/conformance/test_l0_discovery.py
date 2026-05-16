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
    assert payload["profile_id"] == "ru-dax"
    assert payload["jurisdiction"] == "RU"
    assert "L0" in payload["compatibility_levels"]
    assert payload["operator_roles"]
    assert payload["capabilities"]
    assert payload["legal_profiles"]
    assert payload["data_governance"]["audit_trail_required"] is True


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
