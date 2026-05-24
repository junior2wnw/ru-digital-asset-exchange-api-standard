from __future__ import annotations

import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlencode

import httpx

from .errors import APIError


JsonObject = dict[str, Any]


class Client:
    """Small synchronous reference client for RU-DMIP compatible APIs."""

    def __init__(
        self,
        base_url: str,
        *,
        api_key: str | None = None,
        api_secret: str | None = None,
        timeout: float = 10.0,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.api_secret = api_secret
        self._client = http_client or httpx.Client(timeout=timeout)
        self._owns_client = http_client is None

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def time(self) -> JsonObject:
        return self._request("GET", "/v1/time")

    def profile(self) -> JsonObject:
        return self._request("GET", "/v1/profile")

    def instruments(self, *, type: str | None = None) -> list[JsonObject]:
        params = {"type": type} if type else None
        return self._request("GET", "/v1/instruments", params=params)["items"]

    def instrument(self, instrument_id: str) -> JsonObject:
        return self._request("GET", f"/v1/instruments/{instrument_id}")

    def orderbook(self, instrument_id: str, *, depth: int = 50) -> JsonObject:
        return self._request(
            "GET",
            "/v1/market/orderbook",
            params={"instrument_id": instrument_id, "depth": depth},
        )

    def public_trades(self, instrument_id: str, *, limit: int = 100) -> list[JsonObject]:
        return self._request(
            "GET",
            "/v1/market/trades",
            params={"instrument_id": instrument_id, "limit": limit},
        )["items"]

    def candles(self, instrument_id: str, interval: str, *, limit: int = 100) -> list[JsonObject]:
        return self._request(
            "GET",
            "/v1/market/candles",
            params={"instrument_id": instrument_id, "interval": interval, "limit": limit},
        )["items"]

    def execution_capabilities(self) -> JsonObject:
        return self._request("GET", "/v1/execution/capabilities")

    def entitlement_capabilities(self) -> JsonObject:
        return self._request("GET", "/v1/entitlements/capabilities")

    def entitlements(self) -> list[JsonObject]:
        return self._request("GET", "/v1/entitlements", private=True)["items"]

    def evaluate_entitlement_authorization(self, **decision_request: Any) -> JsonObject:
        return self._request(
            "POST",
            "/v1/entitlements/authorization/evaluate",
            json_body=decision_request,
            private=True,
        )

    def balances(self) -> list[JsonObject]:
        return self._request("GET", "/v1/account/balances", private=True)["items"]

    def positions(self) -> list[JsonObject]:
        return self._request("GET", "/v1/account/positions", private=True)["items"]

    def orders(self, *, instrument_id: str | None = None, status: str | None = None) -> list[JsonObject]:
        params = {k: v for k, v in {"instrument_id": instrument_id, "status": status}.items() if v}
        return self._request("GET", "/v1/orders", params=params or None, private=True)["items"]

    def create_order(self, **order: Any) -> JsonObject:
        idempotency_key = order.pop("idempotency_key", None)
        return self._request(
            "POST",
            "/v1/orders",
            json_body=order,
            private=True,
            idempotency_key=idempotency_key,
        )

    def cancel_order(self, order_id: str, *, idempotency_key: str | None = None) -> JsonObject:
        return self._request(
            "DELETE",
            f"/v1/orders/{order_id}",
            private=True,
            idempotency_key=idempotency_key,
        )

    def private_trades(self, *, instrument_id: str | None = None, limit: int = 100) -> list[JsonObject]:
        params = {"limit": limit}
        if instrument_id:
            params["instrument_id"] = instrument_id
        return self._request("GET", "/v1/trades", params=params, private=True)["items"]

    def wallet_assets(self) -> list[JsonObject]:
        return self._request("GET", "/v1/wallet/assets", private=True)["items"]

    def create_deposit_address(
        self,
        asset_id: str,
        network_id: str,
        *,
        idempotency_key: str | None = None,
    ) -> JsonObject:
        return self._request(
            "POST",
            "/v1/wallet/deposit-addresses",
            json_body={"asset_id": asset_id, "network_id": network_id},
            private=True,
            idempotency_key=idempotency_key,
        )

    def deposits(self) -> list[JsonObject]:
        return self._request("GET", "/v1/wallet/deposits", private=True)["items"]

    def withdrawals(self) -> list[JsonObject]:
        return self._request("GET", "/v1/wallet/withdrawals", private=True)["items"]

    def create_withdrawal(self, **withdrawal: Any) -> JsonObject:
        idempotency_key = withdrawal.pop("idempotency_key", None)
        return self._request(
            "POST",
            "/v1/wallet/withdrawals",
            json_body=withdrawal,
            private=True,
            idempotency_key=idempotency_key,
        )

    def create_transfer(self, **transfer: Any) -> JsonObject:
        idempotency_key = transfer.pop("idempotency_key", None)
        return self._request(
            "POST",
            "/v1/transfers",
            json_body=transfer,
            private=True,
            idempotency_key=idempotency_key,
        )

    def compliance_profile(self) -> JsonObject:
        return self._request("GET", "/v1/compliance/profile", private=True)

    def compliance_consents(self) -> list[JsonObject]:
        return self._request("GET", "/v1/compliance/consents", private=True)["items"]

    def audit_events(self, *, limit: int = 100) -> list[JsonObject]:
        return self._request(
            "GET",
            "/v1/compliance/audit-events",
            params={"limit": limit},
            private=True,
        )["items"]

    def regulatory_reports(self) -> list[JsonObject]:
        return self._request("GET", "/v1/reports/regulatory", private=True)["items"]

    def fees(self) -> list[JsonObject]:
        return self._request("GET", "/v1/fees")["items"]

    def limits(self) -> list[JsonObject]:
        return self._request("GET", "/v1/limits")["items"]

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: JsonObject | None = None,
        private: bool = False,
        idempotency_key: str | None = None,
    ) -> JsonObject:
        body = json.dumps(json_body or {}, separators=(",", ":"), sort_keys=True) if json_body else ""
        headers = self._headers(method, path, params, body, private, idempotency_key)
        response = self._client.request(
            method,
            f"{self.base_url}{path}",
            params=params,
            json=json_body,
            headers=headers,
        )
        if response.status_code >= 400:
            raise APIError.from_response(response)
        data = response.json()
        if not isinstance(data, dict):
            raise APIError("INVALID_RESPONSE", "Response body is not a JSON object", response.status_code)
        return data

    def _headers(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None,
        body: str,
        private: bool,
        idempotency_key: str | None,
    ) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        if not private:
            return headers
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        headers["X-Timestamp"] = timestamp
        if idempotency_key:
            headers["X-Idempotency-Key"] = idempotency_key
        if self.api_secret:
            canonical_query = urlencode(sorted((params or {}).items()))
            body_hash = hashlib.sha256(body.encode()).hexdigest()
            payload = f"{timestamp}{method.upper()}{path}{canonical_query}{body_hash}"
            signature = hmac.new(self.api_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
            headers["X-Signature"] = signature
        return headers
