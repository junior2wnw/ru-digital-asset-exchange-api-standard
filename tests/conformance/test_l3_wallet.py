from __future__ import annotations

from uuid import uuid4

import httpx


def test_l3_wallet_assets(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    response = client.get("/v1/wallet/assets", headers=auth_headers)
    assert response.status_code == 200
    asset = response.json()["items"][0]
    assert asset["asset_id"]
    assert asset["networks"]


def test_l3_deposit_address(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    response = client.post(
        "/v1/wallet/deposit-addresses",
        headers=auth_headers | {"X-Idempotency-Key": f"deposit-address-{uuid4().hex}"},
        json={"asset_id": "USDT", "network_id": "TRON"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["asset_id"] == "USDT"
    assert payload["network_id"] == "TRON"
    assert payload["address"]


def test_l3_withdrawal_and_transfer(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    withdrawal = client.post(
        "/v1/wallet/withdrawals",
        headers=auth_headers | {"X-Idempotency-Key": f"withdrawal-{uuid4().hex}"},
        json={
            "asset_id": "USDT",
            "network_id": "TRON",
            "amount": "10",
            "address": "TRUDMIPREFERENCEADDRESS000000000",
        },
    )
    assert withdrawal.status_code == 201
    assert withdrawal.json()["type"] == "withdrawal"

    transfer = client.post(
        "/v1/transfers",
        headers=auth_headers | {"X-Idempotency-Key": f"transfer-{uuid4().hex}"},
        json={
            "asset_id": "USDT",
            "amount": "5",
            "from_account_id": "main",
            "to_account_id": "derivatives",
        },
    )
    assert transfer.status_code == 201
    assert transfer.json()["status"] == "completed"
