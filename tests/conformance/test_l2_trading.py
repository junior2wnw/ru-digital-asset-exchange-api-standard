from __future__ import annotations

from uuid import uuid4

import httpx


def test_l2_balances(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    response = client.get("/v1/account/balances", headers=auth_headers)
    assert response.status_code == 200
    balance = response.json()["items"][0]
    for field in ["asset_id", "available", "reserved", "locked", "total", "credit", "debt"]:
        assert field in balance


def test_l2_order_idempotency_and_cancel(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    key = f"test-order-{uuid4().hex}"
    payload = {
        "instrument_id": "BTC-RUB-SPOT",
        "side": "buy",
        "type": "limit",
        "quantity": "0.01",
        "price": "5000000",
        "client_order_id": key,
    }
    headers = auth_headers | {"X-Idempotency-Key": key}
    first = client.post("/v1/orders", json=payload, headers=headers)
    second = client.post("/v1/orders", json=payload, headers=headers)
    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["exchange_order_id"] == second.json()["exchange_order_id"]

    order_id = first.json()["exchange_order_id"]
    cancelled = client.delete(
        f"/v1/orders/{order_id}",
        headers=auth_headers | {"X-Idempotency-Key": f"cancel-{key}"},
    )
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"


def test_l2_positions_surface(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    response = client.get("/v1/account/positions", headers=auth_headers)
    assert response.status_code == 200
    position = response.json()["items"][0]
    for field in ["instrument_id", "side", "quantity", "entry_price", "mark_price", "margin_mode"]:
        assert field in position

