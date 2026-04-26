from __future__ import annotations

import httpx


def test_l4_derivative_instrument_types(client: httpx.Client) -> None:
    response = client.get("/v1/instruments")
    assert response.status_code == 200
    types = {item["type"] for item in response.json()["items"]}
    assert "perpetual_future" in types
    assert "dated_future" in types
    assert "option" in types
    assert "swap" in types


def test_l4_derivative_fields(client: httpx.Client) -> None:
    response = client.get("/v1/instruments/BTC-USDT-PERP")
    assert response.status_code == 200
    instrument = response.json()
    for field in ["underlying", "settlement_asset", "margin_asset", "contract_size", "funding_interval"]:
        assert field in instrument

