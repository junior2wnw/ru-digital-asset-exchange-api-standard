from __future__ import annotations

import httpx


def test_l1_orderbook(client: httpx.Client) -> None:
    response = client.get("/v1/market/orderbook", params={"instrument_id": "BTC-RUB-SPOT", "depth": 10})
    assert response.status_code == 200
    payload = response.json()
    assert payload["instrument_id"] == "BTC-RUB-SPOT"
    assert isinstance(payload["sequence"], int)
    assert payload["bids"]
    assert payload["asks"]


def test_l1_public_trades(client: httpx.Client) -> None:
    response = client.get("/v1/market/trades", params={"instrument_id": "BTC-RUB-SPOT", "limit": 10})
    assert response.status_code == 200
    trade = response.json()["items"][0]
    assert trade["instrument_id"] == "BTC-RUB-SPOT"
    assert trade["fee"]["asset_id"]
    assert trade["liquidity_role"] in {"maker", "taker", "auction", "liquidation", "settlement"}


def test_l1_candles(client: httpx.Client) -> None:
    response = client.get(
        "/v1/market/candles",
        params={"instrument_id": "BTC-RUB-SPOT", "interval": "1m", "limit": 5},
    )
    assert response.status_code == 200
    candle = response.json()["items"][0]
    for field in ["open_time", "close_time", "open", "high", "low", "close", "volume"]:
        assert field in candle

