from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, Query
from fastapi.responses import JSONResponse


app = FastAPI(
    title="SpreadX Mock Exchange",
    version="0.2.0",
    description="Reference mock exchange for the RU-DAX interoperability profile draft.",
)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def error(code: str, message: str, category: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "category": category,
                "request_id": f"req_{uuid4().hex[:12]}",
                "details": {},
            }
        },
    )


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if x_api_key != "sandbox-key":
        raise Unauthorized()


class Unauthorized(Exception):
    pass


@app.exception_handler(Unauthorized)
async def unauthorized_handler(_, __) -> JSONResponse:
    return error("INVALID_SIGNATURE", "Missing or invalid sandbox API key", "authentication", 401)


INSTRUMENTS = [
    {
        "instrument_id": "BTC-RUB-SPOT",
        "symbol": "BTC/RUB",
        "type": "spot",
        "base_asset": "BTC",
        "quote_asset": "RUB",
        "status": "online",
        "price_tick": "1",
        "quantity_step": "0.00000001",
        "min_quantity": "0.0001",
        "max_quantity": "100",
        "min_notional": "1000",
        "fee_schedule_id": "standard",
        "risk_profile_id": "spot-standard",
        "legal_classification": "digital_currency",
        "regulatory_scope": "sandbox",
        "investor_access": "implementation_defined",
        "payment_use_allowed": False,
        "jurisdiction": "RU",
    },
    {
        "instrument_id": "BTC-USDT-PERP",
        "symbol": "BTC/USDT PERP",
        "type": "perpetual_future",
        "base_asset": "BTC",
        "quote_asset": "USDT",
        "status": "online",
        "price_tick": "0.1",
        "quantity_step": "0.001",
        "min_quantity": "0.001",
        "max_quantity": "1000",
        "min_notional": "5",
        "fee_schedule_id": "derivatives",
        "risk_profile_id": "perp-standard",
        "legal_classification": "derivative",
        "regulatory_scope": "sandbox",
        "investor_access": "qualified_investor",
        "payment_use_allowed": False,
        "jurisdiction": "RU",
        "underlying": "BTC-USD-INDEX",
        "settlement_asset": "USDT",
        "margin_asset": "USDT",
        "contract_size": "1",
        "funding_interval": "8h",
        "settlement_method": "cash",
    },
    {
        "instrument_id": "ETH-USDT-20260626-FUT",
        "symbol": "ETH/USDT 2026-06-26 FUT",
        "type": "dated_future",
        "base_asset": "ETH",
        "quote_asset": "USDT",
        "status": "online",
        "price_tick": "0.01",
        "quantity_step": "0.01",
        "min_quantity": "0.01",
        "max_quantity": "5000",
        "min_notional": "5",
        "fee_schedule_id": "derivatives",
        "risk_profile_id": "future-standard",
        "legal_classification": "derivative",
        "regulatory_scope": "sandbox",
        "investor_access": "qualified_investor",
        "payment_use_allowed": False,
        "jurisdiction": "RU",
        "underlying": "ETH-USD-INDEX",
        "settlement_asset": "USDT",
        "margin_asset": "USDT",
        "contract_size": "1",
        "expiry_time": "2026-06-26T08:00:00Z",
        "settlement_method": "cash",
    },
    {
        "instrument_id": "BTC-USDT-20260626-80000-C",
        "symbol": "BTC/USDT 2026-06-26 80000 CALL",
        "type": "option",
        "base_asset": "BTC",
        "quote_asset": "USDT",
        "status": "online",
        "price_tick": "0.1",
        "quantity_step": "0.001",
        "min_quantity": "0.001",
        "max_quantity": "100",
        "min_notional": "1",
        "fee_schedule_id": "options",
        "risk_profile_id": "option-standard",
        "legal_classification": "derivative",
        "regulatory_scope": "sandbox",
        "investor_access": "qualified_investor",
        "payment_use_allowed": False,
        "jurisdiction": "RU",
        "underlying": "BTC-USD-INDEX",
        "settlement_asset": "USDT",
        "margin_asset": "USDT",
        "contract_size": "1",
        "expiry_time": "2026-06-26T08:00:00Z",
        "strike_price": "80000",
        "option_type": "call",
        "settlement_method": "cash",
    },
    {
        "instrument_id": "BTC-ETH-SWAP",
        "symbol": "BTC/ETH SWAP",
        "type": "swap",
        "base_asset": "BTC",
        "quote_asset": "ETH",
        "status": "online",
        "price_tick": "0.0001",
        "quantity_step": "0.001",
        "min_quantity": "0.001",
        "max_quantity": "500",
        "min_notional": "0.01",
        "fee_schedule_id": "swaps",
        "risk_profile_id": "swap-standard",
        "legal_classification": "derivative",
        "regulatory_scope": "sandbox",
        "investor_access": "qualified_investor",
        "payment_use_allowed": False,
        "jurisdiction": "RU",
        "underlying": "BTC-ETH-INDEX",
        "settlement_asset": "ETH",
        "margin_asset": "ETH",
        "contract_size": "1",
        "settlement_method": "hybrid",
    },
]

BALS = [
    {
        "asset_id": "RUB",
        "available": "10000000",
        "reserved": "0",
        "locked": "0",
        "total": "10000000",
        "credit": "0",
        "debt": "0",
    },
    {
        "asset_id": "BTC",
        "available": "1.5",
        "reserved": "0",
        "locked": "0",
        "total": "1.5",
        "credit": "0",
        "debt": "0",
    },
    {
        "asset_id": "USDT",
        "available": "250000",
        "reserved": "0",
        "locked": "0",
        "total": "250000",
        "credit": "0",
        "debt": "0",
    },
]

POSITIONS = [
    {
        "instrument_id": "BTC-USDT-PERP",
        "side": "long",
        "quantity": "0.5",
        "entry_price": "70000",
        "mark_price": "70500",
        "liquidation_price": "42000",
        "unrealized_pnl": "250",
        "realized_pnl": "0",
        "initial_margin": "3500",
        "maintenance_margin": "350",
        "leverage": "10",
        "margin_mode": "isolated",
    }
]

ORDERS: list[dict[str, object]] = []
PRIVATE_TRADES: list[dict[str, object]] = []
WITHDRAWALS: list[dict[str, object]] = []
DEPOSITS: list[dict[str, object]] = []
TRANSFERS: list[dict[str, object]] = []
IDEMPOTENCY: dict[str, dict[str, object]] = {}

PROFILE = {
    "profile_id": "ru-dax",
    "profile_version": "0.2.0",
    "jurisdiction": "RU",
    "operator_roles": [
        "exchange",
        "broker",
        "bank",
        "ois_cfa",
        "ootsfa",
        "custodian",
        "wallet_provider",
        "market_maker",
        "compliance_provider",
        "analytics_provider",
        "developer_tool",
    ],
    "compatibility_levels": ["L0", "L1", "L2", "L3", "L4"],
    "capabilities": [
        {"capability_id": "discovery", "level": "L0", "status": "supported"},
        {"capability_id": "sandbox", "level": "L0", "status": "supported"},
        {"capability_id": "conformance", "level": "L0", "status": "supported"},
        {"capability_id": "market_data", "level": "L1", "status": "supported"},
        {"capability_id": "trading", "level": "L2", "status": "supported"},
        {"capability_id": "wallet_custody", "level": "L3", "status": "supported"},
        {"capability_id": "derivatives", "level": "L4", "status": "supported"},
        {"capability_id": "fix", "level": "L4", "status": "planned"},
        {"capability_id": "aml_kyc", "level": "L3", "status": "sandbox_only"},
        {"capability_id": "regulatory_reporting", "level": "L5", "status": "planned"},
    ],
    "legal_profiles": [
        {
            "framework_id": "259-fz-cfa",
            "status": "requires_license_or_register",
            "applies_to": ["cfa_issuance", "cfa_exchange"],
            "description": "CFA issuance and CFA exchange activity require an eligible Russian legal entity and inclusion in the relevant Bank of Russia register.",
            "source_url": "https://www.cbr.ru/finm_infrastructure/digital_oper/",
        },
        {
            "framework_id": "115-fz-aml",
            "status": "implementation_responsibility",
            "applies_to": ["aml_kyc", "wallet_custody", "digital_ruble"],
            "description": "Identification, transaction monitoring, access restriction, and AML controls remain the responsibility of the regulated implementation.",
            "source_url": "https://cbr.ru/press/event/?id=24612",
        },
        {
            "framework_id": "152-fz-personal-data",
            "status": "implementation_responsibility",
            "applies_to": ["open_api_consent", "aml_kyc", "audit_export"],
            "description": "Personal data processing, consent, localization, security, and incident notification are implementation responsibilities.",
            "source_url": "https://rkn.gov.ru/",
        },
    ],
    "data_governance": {
        "client_consent_required": True,
        "personal_data_policy": "implementation_responsibility",
        "audit_trail_required": True,
        "retention_policy": "Defined by the regulated venue and applicable Russian law.",
    },
    "last_updated": "2026-05-16T00:00:00Z",
}


@app.get("/v1/profile")
def venue_profile() -> dict[str, object]:
    return PROFILE


@app.get("/v1/time")
def server_time() -> dict[str, str]:
    return {"server_time": now()}


@app.get("/v1/instruments")
def list_instruments(type: str | None = None) -> dict[str, list[dict[str, object]]]:
    items = [item for item in INSTRUMENTS if type is None or item["type"] == type]
    return {"items": items}


@app.get("/v1/instruments/{instrument_id}", response_model=None)
def get_instrument(instrument_id: str) -> dict[str, object] | JSONResponse:
    for item in INSTRUMENTS:
        if item["instrument_id"] == instrument_id:
            return item
    return error("RESOURCE_NOT_FOUND", "Instrument not found", "not_found", 404)


@app.get("/v1/market/orderbook")
def orderbook(instrument_id: str, depth: int = Query(default=50, ge=1, le=500)) -> dict[str, object]:
    mid = "5000000" if instrument_id == "BTC-RUB-SPOT" else "70000"
    return {
        "instrument_id": instrument_id,
        "sequence": 1000,
        "bids": [{"price": mid, "quantity": "0.5"} for _ in range(min(depth, 3))],
        "asks": [{"price": str(int(float(mid)) + 100), "quantity": "0.4"} for _ in range(min(depth, 3))],
        "event_time": now(),
    }


@app.get("/v1/market/trades")
def public_trades(instrument_id: str, limit: int = Query(default=100, ge=1, le=1000)) -> dict[str, list[dict[str, object]]]:
    trade = {
        "trade_id": "trade_demo_1",
        "instrument_id": instrument_id,
        "exchange_order_id": "order_demo_1",
        "side": "buy",
        "price": "5000000" if instrument_id == "BTC-RUB-SPOT" else "70000",
        "quantity": "0.01",
        "quote_quantity": "50000",
        "fee": {"asset_id": "RUB", "amount": "50"},
        "liquidity_role": "taker",
        "trade_time": now(),
    }
    return {"items": [trade][:limit]}


@app.get("/v1/market/candles")
def candles(instrument_id: str, interval: str, limit: int = Query(default=100, ge=1, le=1000)) -> dict[str, list[dict[str, object]]]:
    close = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    items = []
    for index in range(min(limit, 10)):
        close_time = close - timedelta(minutes=index)
        open_time = close_time - timedelta(minutes=1)
        items.append(
            {
                "open_time": open_time.isoformat().replace("+00:00", "Z"),
                "close_time": close_time.isoformat().replace("+00:00", "Z"),
                "open": "5000000",
                "high": "5010000",
                "low": "4990000",
                "close": "5005000",
                "volume": "2.5",
                "extensions": {"interval": interval, "instrument_id": instrument_id},
            }
        )
    return {"items": items}


@app.get("/v1/account/balances", dependencies=[Depends(require_api_key)])
def balances() -> dict[str, list[dict[str, object]]]:
    stamped = [item | {"updated_at": now()} for item in BALS]
    return {"items": stamped}


@app.get("/v1/account/positions", dependencies=[Depends(require_api_key)])
def positions() -> dict[str, list[dict[str, object]]]:
    stamped = [item | {"updated_at": now()} for item in POSITIONS]
    return {"items": stamped}


@app.get("/v1/orders", dependencies=[Depends(require_api_key)])
def list_orders(instrument_id: str | None = None, status: str | None = None) -> dict[str, list[dict[str, object]]]:
    items = [
        item
        for item in ORDERS
        if (instrument_id is None or item["instrument_id"] == instrument_id)
        and (status is None or item["status"] == status)
    ]
    return {"items": items}


@app.post("/v1/orders", status_code=201, dependencies=[Depends(require_api_key)], response_model=None)
def create_order(payload: dict[str, object], x_idempotency_key: str | None = Header(default=None)) -> dict[str, object] | JSONResponse:
    if x_idempotency_key and x_idempotency_key in IDEMPOTENCY:
        return IDEMPOTENCY[x_idempotency_key]
    required = {"instrument_id", "side", "type", "quantity"}
    if missing := required - payload.keys():
        return error("INVALID_REQUEST", f"Missing fields: {', '.join(sorted(missing))}", "validation", 400)
    order = {
        "exchange_order_id": f"ord_{uuid4().hex[:12]}",
        "client_order_id": payload.get("client_order_id"),
        "instrument_id": payload["instrument_id"],
        "side": payload["side"],
        "type": payload["type"],
        "status": "open",
        "time_in_force": payload.get("time_in_force", "gtc"),
        "position_intent": payload.get("position_intent", "open"),
        "quantity": payload["quantity"],
        "filled_quantity": "0",
        "price": payload.get("price"),
        "average_price": "0",
        "fee": {"asset_id": "RUB", "amount": "0"},
        "created_at": now(),
        "updated_at": now(),
    }
    ORDERS.append(order)
    if x_idempotency_key:
        IDEMPOTENCY[x_idempotency_key] = order
    return order


@app.delete("/v1/orders/{order_id}", dependencies=[Depends(require_api_key)], response_model=None)
def cancel_order(order_id: str, x_idempotency_key: str | None = Header(default=None)) -> dict[str, object] | JSONResponse:
    if x_idempotency_key and x_idempotency_key in IDEMPOTENCY:
        return IDEMPOTENCY[x_idempotency_key]
    for order in ORDERS:
        if order["exchange_order_id"] == order_id:
            order["status"] = "cancelled"
            order["updated_at"] = now()
            if x_idempotency_key:
                IDEMPOTENCY[x_idempotency_key] = order
            return order
    return error("RESOURCE_NOT_FOUND", "Order not found", "not_found", 404)


@app.get("/v1/trades", dependencies=[Depends(require_api_key)])
def private_trades(instrument_id: str | None = None, limit: int = Query(default=100, ge=1, le=1000)) -> dict[str, list[dict[str, object]]]:
    items = [item for item in PRIVATE_TRADES if instrument_id is None or item["instrument_id"] == instrument_id]
    return {"items": items[:limit]}


@app.get("/v1/wallet/assets", dependencies=[Depends(require_api_key)])
def wallet_assets() -> dict[str, list[dict[str, object]]]:
    return {
        "items": [
            {
                "asset_id": "USDT",
                "networks": [
                    {
                        "network_id": "TRON",
                        "deposit_enabled": True,
                        "withdrawal_enabled": True,
                        "min_confirmations": 20,
                        "withdrawal_fee": "1",
                    },
                    {
                        "network_id": "ETHEREUM",
                        "deposit_enabled": True,
                        "withdrawal_enabled": True,
                        "min_confirmations": 12,
                        "withdrawal_fee": "5",
                    },
                ],
            },
            {
                "asset_id": "BTC",
                "networks": [
                    {
                        "network_id": "BITCOIN",
                        "deposit_enabled": True,
                        "withdrawal_enabled": True,
                        "min_confirmations": 3,
                        "withdrawal_fee": "0.0001",
                    }
                ],
            },
        ]
    }


@app.post("/v1/wallet/deposit-addresses", dependencies=[Depends(require_api_key)])
def create_deposit_address(payload: dict[str, object], x_idempotency_key: str | None = Header(default=None)) -> dict[str, object]:
    if x_idempotency_key and x_idempotency_key in IDEMPOTENCY:
        return IDEMPOTENCY[x_idempotency_key]
    response = {
        "asset_id": payload.get("asset_id", "USDT"),
        "network_id": payload.get("network_id", "TRON"),
        "address": "TSPREADXMOCKADDRESS000000000000",
        "memo": None,
    }
    if x_idempotency_key:
        IDEMPOTENCY[x_idempotency_key] = response
    return response


@app.get("/v1/wallet/deposits", dependencies=[Depends(require_api_key)])
def list_deposits() -> dict[str, list[dict[str, object]]]:
    return {"items": DEPOSITS}


@app.get("/v1/wallet/withdrawals", dependencies=[Depends(require_api_key)])
def list_withdrawals() -> dict[str, list[dict[str, object]]]:
    return {"items": WITHDRAWALS}


@app.post("/v1/wallet/withdrawals", status_code=201, dependencies=[Depends(require_api_key)])
def create_withdrawal(payload: dict[str, object], x_idempotency_key: str | None = Header(default=None)) -> dict[str, object]:
    if x_idempotency_key and x_idempotency_key in IDEMPOTENCY:
        return IDEMPOTENCY[x_idempotency_key]
    withdrawal = {
        "wallet_transaction_id": f"wdr_{uuid4().hex[:12]}",
        "type": "withdrawal",
        "asset_id": payload.get("asset_id", "USDT"),
        "network_id": payload.get("network_id", "TRON"),
        "amount": payload.get("amount", "0"),
        "fee": "1",
        "address": payload.get("address", ""),
        "memo": payload.get("memo"),
        "status": "compliance_review",
        "travel_rule": payload.get("travel_rule", {}),
        "created_at": now(),
        "updated_at": now(),
    }
    WITHDRAWALS.append(withdrawal)
    if x_idempotency_key:
        IDEMPOTENCY[x_idempotency_key] = withdrawal
    return withdrawal


@app.post("/v1/transfers", status_code=201, dependencies=[Depends(require_api_key)])
def create_transfer(payload: dict[str, object], x_idempotency_key: str | None = Header(default=None)) -> dict[str, object]:
    if x_idempotency_key and x_idempotency_key in IDEMPOTENCY:
        return IDEMPOTENCY[x_idempotency_key]
    transfer = {
        "wallet_transaction_id": f"trf_{uuid4().hex[:12]}",
        "type": "transfer",
        "asset_id": payload.get("asset_id", "USDT"),
        "amount": payload.get("amount", "0"),
        "from_account_id": payload.get("from_account_id", "main"),
        "to_account_id": payload.get("to_account_id", "derivatives"),
        "status": "completed",
        "created_at": now(),
        "updated_at": now(),
    }
    TRANSFERS.append(transfer)
    if x_idempotency_key:
        IDEMPOTENCY[x_idempotency_key] = transfer
    return transfer


@app.get("/v1/fees")
def fees() -> dict[str, list[dict[str, str]]]:
    return {
        "items": [
            {"fee_schedule_id": "standard", "maker_fee": "0.001", "taker_fee": "0.002"},
            {"fee_schedule_id": "derivatives", "maker_fee": "0.0002", "taker_fee": "0.0005"},
            {"fee_schedule_id": "options", "maker_fee": "0.0003", "taker_fee": "0.0006"},
        ]
    }


@app.get("/v1/limits")
def limits() -> dict[str, list[dict[str, str]]]:
    return {
        "items": [
            {"limit_id": "orders_per_second", "scope": "account", "value": "20", "used": "0"},
            {"limit_id": "withdrawal_daily_usdt", "scope": "account", "value": "100000", "used": "0"},
            {"limit_id": "btc_usdt_perp_position", "scope": "instrument", "value": "100", "used": "0"},
        ]
    }
