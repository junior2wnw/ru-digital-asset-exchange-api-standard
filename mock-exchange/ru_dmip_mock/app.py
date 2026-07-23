from __future__ import annotations

import hashlib
import hmac
import json
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from urllib.parse import quote
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI(
    title="RU-DMIP Reference Sandbox",
    version="0.5.0",
    description="Reference sandbox for the RU Digital Market Interoperability Profile draft.",
)

SANDBOX_API_KEY = "sandbox-key"
SANDBOX_API_SECRET = "sandbox-secret"
SIGNATURE_WINDOW_SECONDS = 30
SEEN_SIGNATURES: dict[str, tuple[datetime, str | None]] = {}


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


def idempotency_required() -> JSONResponse:
    return error(
        "IDEMPOTENCY_KEY_REQUIRED",
        "X-Idempotency-Key is required for sandbox commands",
        "validation",
        400,
    )


def validate_idempotency_key(idempotency_key: str | None) -> JSONResponse | None:
    if not idempotency_key:
        return idempotency_required()
    if not 8 <= len(idempotency_key) <= 128:
        return error(
            "INVALID_IDEMPOTENCY_KEY",
            "X-Idempotency-Key must contain between 8 and 128 characters",
            "validation",
            400,
        )
    return None


def idempotency_fingerprint(payload: object) -> str:
    canonical = json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()


def canonicalize_query(items: list[tuple[str, str]]) -> str:
    encoded = [
        (quote(key, safe="~-._"), quote(value, safe="~-._"))
        for key, value in items
    ]
    return "&".join(
        f"{key}={value}"
        for key, value in sorted(encoded)
    )


def cached_command(
    scope: str,
    idempotency_key: str,
    fingerprint: str,
) -> dict[str, object] | JSONResponse | None:
    cached = IDEMPOTENCY.get((scope, idempotency_key))
    if cached is None:
        return None
    cached_fingerprint, cached_response = cached
    if cached_fingerprint != fingerprint:
        return error(
            "IDEMPOTENCY_CONFLICT",
            "Idempotency key was already used with a different command",
            "conflict",
            409,
        )
    return deepcopy(cached_response)


def remember_command(
    scope: str,
    idempotency_key: str,
    fingerprint: str,
    response: dict[str, object],
) -> None:
    IDEMPOTENCY[(scope, idempotency_key)] = (fingerprint, deepcopy(response))


async def require_private_auth(
    request: Request,
    x_api_key: str | None = Header(default=None),
    x_signature: str | None = Header(default=None),
    x_timestamp: str | None = Header(default=None),
    x_idempotency_key: str | None = Header(default=None),
) -> None:
    if x_api_key != SANDBOX_API_KEY or not x_signature or not x_timestamp:
        raise AuthenticationError()
    try:
        signed_at = datetime.fromisoformat(x_timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AuthenticationError() from exc
    if signed_at.tzinfo is None:
        raise AuthenticationError()
    current_time = datetime.now(timezone.utc)
    skew = abs((current_time - signed_at.astimezone(timezone.utc)).total_seconds())
    if skew > SIGNATURE_WINDOW_SECONDS:
        raise AuthenticationError("SIGNATURE_EXPIRED", "Sandbox request timestamp is outside the allowed window")
    body = await request.body()
    canonical_query = canonicalize_query(list(request.query_params.multi_items()))
    body_hash = hashlib.sha256(body).hexdigest()
    payload = f"{x_timestamp}{request.method.upper()}{request.url.path}{canonical_query}{body_hash}"
    expected = hmac.new(SANDBOX_API_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, x_signature):
        raise AuthenticationError()

    expired_before = current_time - timedelta(seconds=SIGNATURE_WINDOW_SECONDS)
    for signature, (observed_at, _) in list(SEEN_SIGNATURES.items()):
        if observed_at < expired_before:
            del SEEN_SIGNATURES[signature]
    previous = SEEN_SIGNATURES.get(x_signature)
    if previous and not (x_idempotency_key and previous[1] == x_idempotency_key):
        raise AuthenticationError("REPLAY_DETECTED", "Duplicate sandbox request signature")
    SEEN_SIGNATURES[x_signature] = (current_time, x_idempotency_key)


class AuthenticationError(Exception):
    def __init__(
        self,
        code: str = "INVALID_SIGNATURE",
        message: str = "Missing or invalid sandbox authentication",
    ) -> None:
        self.code = code
        self.message = message


@app.exception_handler(AuthenticationError)
async def authentication_error_handler(_, exc: AuthenticationError) -> JSONResponse:
    return error(exc.code, exc.message, "authentication", 401)


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(_, __: RequestValidationError) -> JSONResponse:
    return error("INVALID_REQUEST", "Request validation failed", "validation", 422)


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(_, exc: StarletteHTTPException) -> JSONResponse:
    if exc.status_code == 404:
        return error("RESOURCE_NOT_FOUND", "Resource not found", "not_found", 404)
    if exc.status_code == 405:
        return error("METHOD_NOT_ALLOWED", "Method not allowed", "validation", 405)
    return error("HTTP_ERROR", "HTTP request failed", "request", exc.status_code)


@app.exception_handler(Exception)
async def unhandled_error_handler(_, __: Exception) -> JSONResponse:
    return error("INTERNAL_ERROR", "Unexpected sandbox error", "internal", 500)


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
IDEMPOTENCY: dict[tuple[str, str], tuple[str, dict[str, object]]] = {}

PROFILE = {
    "profile_id": "ru-dmip",
    "profile_version": "0.5.0",
    "jurisdiction": "RU",
    "operator_roles": [
        "exchange",
        "broker",
        "bank",
        "ois_cfa",
        "ootsfa",
        "crypto_exchange",
        "digital_depository",
        "management_company",
        "organized_trading_operator",
        "custodian",
        "wallet_provider",
        "payment_provider",
        "market_maker",
        "issuer",
        "qualified_investor_gateway",
        "compliance_provider",
        "analytics_provider",
        "developer_tool",
        "regulator_observer",
        "mining_infrastructure_operator",
    ],
    "compatibility_levels": ["L0", "L1", "L2", "L3", "L4", "L5"],
    "capabilities": [
        {"capability_id": "discovery", "level": "L0", "status": "supported"},
        {"capability_id": "sandbox", "level": "L0", "status": "supported"},
        {"capability_id": "conformance", "level": "L0", "status": "supported"},
        {"capability_id": "market_data", "level": "L1", "status": "supported"},
        {"capability_id": "execution_semantics", "level": "L2", "status": "supported"},
        {"capability_id": "event_replay", "level": "L2", "status": "supported"},
        {"capability_id": "synthetic_position", "level": "L2", "status": "supported"},
        {"capability_id": "trading", "level": "L2", "status": "supported"},
        {"capability_id": "wallet_custody", "level": "L3", "status": "supported"},
        {"capability_id": "derivatives", "level": "L4", "status": "supported"},
        {"capability_id": "fix", "level": "L4", "status": "planned"},
        {"capability_id": "crypto_circulation", "level": "L5", "status": "sandbox_only"},
        {"capability_id": "open_api_consent", "level": "L5", "status": "supported"},
        {"capability_id": "aml_kyc", "level": "L5", "status": "supported"},
        {"capability_id": "audit_export", "level": "L5", "status": "supported"},
        {"capability_id": "regulatory_reporting", "level": "L5", "status": "supported"},
        {"capability_id": "fx_control", "level": "L5", "status": "supported"},
        {"capability_id": "entitlements", "level": "L5", "status": "supported"},
        {"capability_id": "strong_authentication", "level": "L5", "status": "supported"},
        {"capability_id": "authorization_policy", "level": "L5", "status": "supported"},
        {"capability_id": "delegated_authority", "level": "L5", "status": "supported"},
        {"capability_id": "tax_reporting", "level": "L5", "status": "planned"},
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
            "framework_id": "ru-crypto-circulation-2026",
            "status": "implementation_responsibility",
            "applies_to": [
                "crypto_circulation",
                "trading",
                "wallet_custody",
                "entitlements",
                "aml_kyc",
                "regulatory_reporting",
            ],
            "description": "The July 2026 regulatory announcement is represented for sandbox discovery only. Production eligibility, effective dates, and controls depend on the officially published act, implementing rules, and each participant's legal status. Cryptocurrency payment use is not implied.",
            "source_url": "https://www.cbr.ru/press/event/?id=32719",
        },
        {
            "framework_id": "open-api-cbr-standards",
            "status": "implementation_responsibility",
            "applies_to": ["open_api_consent"],
            "description": "Client data exchange through Open API-style integrations is consent-based and must follow the applicable security and consent model.",
            "source_url": "https://www.cbr.ru/fintech/api/",
        },
        {
            "framework_id": "161-fz-digital-ruble",
            "status": "implementation_responsibility",
            "applies_to": ["digital_ruble", "aml_kyc"],
            "description": "Digital ruble operations are a separate platform and payment contour with AML responsibilities allocated by the applicable rules.",
            "source_url": "https://www.cbr.ru/fintech/dr/",
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
        {
            "framework_id": "173-fz-currency-control",
            "status": "implementation_responsibility",
            "applies_to": ["fx_control", "regulatory_reporting"],
            "description": "Digital-right operations connected to foreign-trade or currency-control scenarios require structured document and operation references in the authorized-bank contour.",
            "source_url": "https://www.cbr.ru/press/event/?id=23173",
        },
        {
            "framework_id": "63-fz-electronic-signature",
            "status": "implementation_responsibility",
            "applies_to": ["strong_authentication", "authorization_policy", "delegated_authority"],
            "description": "Legally significant electronic actions may require an appropriate electronic signature, request signing, and non-repudiation controls.",
            "source_url": "https://publication.pravo.gov.ru/Document/View/0001202504210023",
        },
    ],
    "data_governance": {
        "client_consent_required": True,
        "personal_data_policy": "implementation_responsibility",
        "audit_trail_required": True,
        "retention_policy": "Defined by the regulated implementation and applicable Russian law.",
    },
    "last_updated": "2026-07-23T00:00:00Z",
    "extensions": {
        "public_name": "RU Digital Market Interoperability Profile",
    },
}

COMPLIANCE_PROFILE = {
    "profile_id": "ru-dmip-l5",
    "level": "L5",
    "supported_scopes": [
        "consent.read",
        "compliance.status.read",
        "audit.events.read",
        "reports.regulatory.read",
        "fx_control.references.read",
        "entitlements.read",
        "entitlements.authorization.evaluate",
    ],
    "consent_required": True,
    "personal_data_public_api_allowed": False,
    "status_vocabulary": [
        "not_required",
        "pending",
        "approved",
        "information_required",
        "manual_review",
        "rejected",
        "blocked",
        "expired",
    ],
    "retention_classes": ["operational", "regulatory", "security", "client_consent"],
    "extensions": {
        "data_minimization": True,
        "sandbox_notice": "Reference data is synthetic and does not contain personal data.",
    },
}

ENTITLEMENT_CAPABILITIES = {
    "profile_id": "ru-dmip-entitlements-auth",
    "profile_version": "0.5.0",
    "level": "L5",
    "supported_entitlement_types": [
        "digital_asset_holding",
        "digital_financial_asset",
        "claim_right",
        "monetary_claim",
        "goods_delivery_claim",
        "service_claim",
        "work_performance_claim",
        "ip_exclusive_right",
        "ip_usage_right",
        "revenue_share_right",
        "governance_right",
        "voting_right",
        "access_right",
        "custody_right",
        "pledge_or_encumbrance",
        "beneficial_interest",
        "nominee_holding",
        "settlement_right",
        "other_lawful_right",
    ],
    "entitlement_statuses": [
        "draft",
        "active",
        "suspended",
        "encumbered",
        "pending_transfer",
        "transferred",
        "redeemed",
        "expired",
        "cancelled",
        "disputed",
        "blocked_by_law",
    ],
    "subject_types": [
        "individual",
        "legal_entity",
        "public_entity",
        "account",
        "subaccount",
        "nominee",
        "beneficial_owner",
        "qualified_investor_gateway",
        "system",
    ],
    "authentication_methods": [
        "api_key",
        "request_signature",
        "mutual_tls",
        "oauth2_client_credentials",
        "oauth2_authorization_code_pkce",
        "hardware_key",
        "webauthn",
        "qualified_electronic_signature",
        "trusted_federated_identity",
    ],
    "minimum_assurance_for_sensitive_actions": "high",
    "authorization_models": [
        "scopes",
        "rbac",
        "abac",
        "purpose_limitation",
        "delegated_authority",
        "transaction_policy",
        "dual_control",
        "risk_based_step_up",
        "revocation_check",
        "consent_check",
    ],
    "security_controls": [
        "least_privilege",
        "deny_by_default",
        "separation_of_duties",
        "mfa_for_sensitive_operations",
        "step_up_for_entitlement_transfer",
        "request_signing",
        "timestamp_and_nonce",
        "replay_protection",
        "idempotency",
        "tamper_evident_audit_log",
        "key_rotation",
        "data_minimization",
        "masking",
        "revocation_check",
        "protected_exports",
    ],
    "sensitive_actions": [
        "create",
        "update",
        "transfer",
        "encumber",
        "release_encumbrance",
        "redeem",
        "delegate",
        "revoke_delegation",
        "evidence_read",
    ],
    "supported_scopes": [
        "entitlements.read",
        "entitlements.write",
        "entitlements.transfer",
        "entitlements.encumber",
        "entitlements.redeem",
        "entitlements.delegate",
        "entitlements.evidence.read",
        "entitlements.audit.read",
        "entitlements.authorization.evaluate",
    ],
    "prohibited_entitlement_policy": {
        "illegal_entitlements_rejected": True,
        "infringing_terms_rejected": True,
        "discriminatory_terms_rejected": True,
        "lawful_basis_required": True,
    },
    "evidence_policy": {
        "raw_documents_public_api_allowed": False,
        "hashes_supported": True,
        "protected_download_refs_supported": True,
    },
    "audit_required": True,
    "extensions": {
        "sandbox_notice": "Reference data is synthetic and does not create legal rights.",
        "bearer_only_sensitive_actions_allowed": False,
    },
}

ENTITLEMENTS = [
    {
        "entitlement_id": "entitlement_demo_cfa_holding_1",
        "entitlement_type": "digital_financial_asset",
        "status": "active",
        "holder_ref": "subject_demo_hash_001",
        "holder_type": "legal_entity",
        "instrument_id": "BTC-RUB-SPOT",
        "asset_ref": "asset_demo_cfa_001",
        "issuer_ref": "issuer_demo_hash_001",
        "registry_ref": "registry_entry_demo_001",
        "legal_classification": "digital_financial_asset",
        "governing_framework": "259-fz-cfa",
        "quantity": "10",
        "unit": "unit",
        "restrictions": [
            {
                "restriction_type": "investor_access",
                "status": "active",
                "framework_id": "platform-rules",
                "description": "Access is verified by the implementation before transfer.",
            },
            {
                "restriction_type": "payment_use_prohibited",
                "status": "active",
                "framework_id": "259-fz-cfa",
                "description": "The entitlement record must not be interpreted as permission to use digital currency as payment.",
            },
        ],
        "encumbrances": [],
        "evidence": [
            {
                "evidence_type": "issuance_decision",
                "evidence_ref": "evidence_ref_demo_issuance_001",
                "evidence_hash": "sha256:demo-issuance-decision",
                "issuer_ref": "issuer_demo_hash_001",
                "issued_at": "2026-05-25T00:00:00Z",
                "verification_status": "verified",
                "protected_download_ref": "protected_evidence_demo_001",
            }
        ],
        "authorization_policy_id": "entitlement_policy_high_assurance_v1",
        "created_at": "2026-05-25T00:00:00Z",
        "updated_at": "2026-05-25T00:00:00Z",
        "extensions": {
            "contains_personal_data": False,
            "raw_documents_included": False,
        },
    },
    {
        "entitlement_id": "entitlement_demo_claim_services_1",
        "entitlement_type": "service_claim",
        "status": "active",
        "holder_ref": "subject_demo_hash_001",
        "holder_type": "legal_entity",
        "contract_ref": "contract_ref_demo_services_001",
        "issuer_ref": "issuer_demo_hash_002",
        "registry_ref": "registry_entry_demo_002",
        "legal_classification": "claim_right",
        "governing_framework": "platform-rules",
        "quantity": "1",
        "unit": "claim",
        "restrictions": [
            {
                "restriction_type": "lawful_object_required",
                "status": "active",
                "framework_id": "platform-rules",
                "description": "The claimed service must remain lawful and non-infringing.",
            }
        ],
        "encumbrances": [],
        "evidence": [
            {
                "evidence_type": "contract_reference",
                "evidence_ref": "evidence_ref_demo_contract_001",
                "evidence_hash": "sha256:demo-contract-reference",
                "issuer_ref": "issuer_demo_hash_002",
                "issued_at": "2026-05-25T00:00:00Z",
                "verification_status": "verified",
            }
        ],
        "authorization_policy_id": "entitlement_policy_high_assurance_v1",
        "created_at": "2026-05-25T00:00:00Z",
        "updated_at": "2026-05-25T00:00:00Z",
        "extensions": {
            "contains_personal_data": False,
            "raw_documents_included": False,
        },
    },
]


CONSENTS = [
    {
        "consent_id": "consent_demo_open_api_1",
        "subject_ref": "subject_demo_hash_001",
        "subject_type": "legal_entity",
        "status": "active",
        "scopes": ["accounts.summary.read", "reports.regulatory.read"],
        "data_categories": ["account_metadata", "operation_references", "report_descriptors"],
        "purpose": "Interoperability pilot and reporting reconciliation",
        "legal_basis": "client_consent",
        "granted_at": "2026-05-16T00:00:00Z",
        "expires_at": "2026-11-16T00:00:00Z",
    }
]

AUDIT_EVENTS = [
    {
        "audit_event_id": "audit_demo_0001",
        "event_type": "consent_lifecycle",
        "event_time": "2026-05-16T00:00:00Z",
        "actor_type": "api_key",
        "actor_ref": "key_demo_reporting",
        "resource_type": "consent",
        "resource_id": "consent_demo_open_api_1",
        "action": "granted",
        "result": "success",
        "request_id": "req_demo_0001",
        "retention_class": "client_consent",
    },
    {
        "audit_event_id": "audit_demo_0002",
        "event_type": "report_generation",
        "event_time": "2026-05-16T00:01:00Z",
        "actor_type": "system",
        "actor_ref": "reporting_scheduler",
        "resource_type": "regulatory_report",
        "resource_id": "report_demo_q2_fx_refs",
        "action": "prepared",
        "result": "success",
        "request_id": "req_demo_0002",
        "retention_class": "regulatory",
    },
]

REGULATORY_REPORTS = [
    {
        "report_id": "report_demo_q2_fx_refs",
        "report_type": "currency_control_digital_rights_references",
        "framework_id": "173-fz-currency-control",
        "period_start": "2026-04-01T00:00:00Z",
        "period_end": "2026-06-30T23:59:59Z",
        "status": "ready",
        "generated_at": "2026-05-16T00:01:00Z",
        "delivery_channel": "protected_api",
        "protected_download_ref": "export_ref_demo_q2_fx_refs",
        "checksum": "sha256:demo",
        "retention_class": "regulatory",
        "extensions": {
            "contains_personal_data": False,
            "contains_document_references": True,
        },
    }
]

EXECUTION_CAPABILITIES = {
    "profile_id": "ru-dmip-execution",
    "profile_version": "0.5.0",
    "intent_types": [
        "single_order",
        "basket",
        "spread",
        "hedge",
        "rebalance",
        "close_position",
        "transfer",
        "reporting_action",
    ],
    "base_states": [
        "created",
        "accepted",
        "working",
        "partially_filled",
        "filled",
        "cancel_requested",
        "partially_cancelled",
        "cancelled",
        "expired",
        "rejected",
        "failed",
    ],
    "event_types": [
        "intent_created",
        "intent_accepted",
        "intent_rejected",
        "order_acknowledged",
        "fill_received",
        "cancel_requested",
        "cancel_acknowledged",
        "risk_blocked",
        "state_reconciled",
        "replay_gap_detected",
    ],
    "quality_statuses": ["fresh", "stale", "gap_detected", "recovered", "unknown"],
    "contracts": {
        "acknowledgement_models": ["sync", "async", "eventual"],
        "fill_models": ["atomic", "partial_allowed", "best_effort"],
        "cancel_fill_race_policy": "event_ordering_wins",
        "stale_data_policy": "require_confirmation",
    },
    "risk_constraints": [
        "max_notional",
        "max_quantity",
        "max_slippage",
        "max_latency",
        "reduce_only",
        "position_limit",
        "portfolio_exposure",
        "legal_access",
        "client_permission",
        "freshness_required",
    ],
    "replay": {
        "supported": True,
        "sequence_policy": "gapless",
        "gap_recovery_policy": "replay_from_sequence",
    },
    "idempotency": {
        "required_for_commands": True,
        "window": "24h",
    },
    "venue_specific_logic_boundary": "adapter_only",
}


@app.get("/v1/profile")
def participant_profile() -> dict[str, object]:
    return PROFILE


@app.get("/v1/entitlements/capabilities")
def entitlement_capabilities() -> dict[str, object]:
    return ENTITLEMENT_CAPABILITIES


@app.get("/v1/compliance/profile", dependencies=[Depends(require_private_auth)])
def compliance_profile() -> dict[str, object]:
    return COMPLIANCE_PROFILE


@app.get("/v1/compliance/consents", dependencies=[Depends(require_private_auth)])
def compliance_consents() -> dict[str, list[dict[str, object]]]:
    return {"items": CONSENTS}


@app.get("/v1/compliance/audit-events", dependencies=[Depends(require_private_auth)])
def compliance_audit_events(limit: int = Query(default=100, ge=1, le=1000)) -> dict[str, list[dict[str, object]]]:
    return {"items": AUDIT_EVENTS[:limit]}


@app.get("/v1/reports/regulatory", dependencies=[Depends(require_private_auth)])
def regulatory_reports() -> dict[str, list[dict[str, object]]]:
    return {"items": REGULATORY_REPORTS}


@app.get("/v1/entitlements", dependencies=[Depends(require_private_auth)])
def entitlements() -> dict[str, list[dict[str, object]]]:
    return {"items": ENTITLEMENTS}


@app.post("/v1/entitlements/authorization/evaluate", dependencies=[Depends(require_private_auth)])
def entitlement_authorization_evaluate(payload: dict[str, object]) -> dict[str, object]:
    action = str(payload.get("action", "read"))
    resource_ref = str(payload.get("resource_ref", "unknown"))
    scopes = set(payload.get("scopes") or [])
    assurance = str(payload.get("authentication_assurance", "low"))
    sensitive_actions = set(ENTITLEMENT_CAPABILITIES["sensitive_actions"])
    high_assurance = assurance in {"high", "qualified_signature"}
    reason_codes: list[str] = []
    allow = False
    step_up_required = False
    dual_control_required = action in {"transfer", "encumber", "redeem", "delegate"}

    if action == "illegal_or_infringing_action":
        reason_codes.extend(["blocked_by_law", "infringing_term"])
    elif action in sensitive_actions and not high_assurance:
        reason_codes.extend(["insufficient_authentication_assurance", "step_up_required"])
        step_up_required = True
    elif action == "read" and "entitlements.read" not in scopes:
        reason_codes.append("missing_scope")
    elif action != "read" and f"entitlements.{action}" not in scopes:
        reason_codes.append("missing_scope")
    else:
        allow = True
        reason_codes.append("allowed")

    return {
        "decision_id": f"decision_{uuid4().hex[:12]}",
        "allow": allow,
        "action": action,
        "resource_ref": resource_ref,
        "reason_codes": reason_codes,
        "required_assurance": "high" if action in sensitive_actions else "substantial",
        "step_up_required": step_up_required,
        "dual_control_required": dual_control_required and allow,
        "audit_required": True,
        "decided_at": now(),
    }


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


@app.get("/v1/execution/capabilities")
def execution_capabilities() -> dict[str, object]:
    return EXECUTION_CAPABILITIES


@app.get("/v1/account/balances", dependencies=[Depends(require_private_auth)])
def balances() -> dict[str, list[dict[str, object]]]:
    stamped = [item | {"updated_at": now()} for item in BALS]
    return {"items": stamped}


@app.get("/v1/account/positions", dependencies=[Depends(require_private_auth)])
def positions() -> dict[str, list[dict[str, object]]]:
    stamped = [item | {"updated_at": now()} for item in POSITIONS]
    return {"items": stamped}


@app.get("/v1/orders", dependencies=[Depends(require_private_auth)])
def list_orders(instrument_id: str | None = None, status: str | None = None) -> dict[str, list[dict[str, object]]]:
    items = [
        item
        for item in ORDERS
        if (instrument_id is None or item["instrument_id"] == instrument_id)
        and (status is None or item["status"] == status)
    ]
    return {"items": items}


@app.post("/v1/orders", status_code=201, dependencies=[Depends(require_private_auth)], response_model=None)
def create_order(payload: dict[str, object], x_idempotency_key: str | None = Header(default=None)) -> dict[str, object] | JSONResponse:
    if validation_error := validate_idempotency_key(x_idempotency_key):
        return validation_error
    assert x_idempotency_key is not None
    fingerprint = idempotency_fingerprint(payload)
    cached = cached_command("orders:create", x_idempotency_key, fingerprint)
    if cached is not None:
        return cached
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
    remember_command("orders:create", x_idempotency_key, fingerprint, order)
    return order


@app.delete("/v1/orders/{order_id}", dependencies=[Depends(require_private_auth)], response_model=None)
def cancel_order(order_id: str, x_idempotency_key: str | None = Header(default=None)) -> dict[str, object] | JSONResponse:
    if validation_error := validate_idempotency_key(x_idempotency_key):
        return validation_error
    assert x_idempotency_key is not None
    scope = f"orders:cancel:{order_id}"
    fingerprint = idempotency_fingerprint({"order_id": order_id})
    cached = cached_command(scope, x_idempotency_key, fingerprint)
    if cached is not None:
        return cached
    for order in ORDERS:
        if order["exchange_order_id"] == order_id:
            order["status"] = "cancelled"
            order["updated_at"] = now()
            remember_command(scope, x_idempotency_key, fingerprint, order)
            return order
    return error("RESOURCE_NOT_FOUND", "Order not found", "not_found", 404)


@app.get("/v1/trades", dependencies=[Depends(require_private_auth)])
def private_trades(instrument_id: str | None = None, limit: int = Query(default=100, ge=1, le=1000)) -> dict[str, list[dict[str, object]]]:
    items = [item for item in PRIVATE_TRADES if instrument_id is None or item["instrument_id"] == instrument_id]
    return {"items": items[:limit]}


@app.get("/v1/wallet/assets", dependencies=[Depends(require_private_auth)])
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


@app.post(
    "/v1/wallet/deposit-addresses",
    dependencies=[Depends(require_private_auth)],
    response_model=None,
)
def create_deposit_address(
    payload: dict[str, object],
    x_idempotency_key: str | None = Header(default=None),
) -> dict[str, object] | JSONResponse:
    if validation_error := validate_idempotency_key(x_idempotency_key):
        return validation_error
    assert x_idempotency_key is not None
    fingerprint = idempotency_fingerprint(payload)
    cached = cached_command("wallet:deposit-address", x_idempotency_key, fingerprint)
    if cached is not None:
        return cached
    response = {
        "asset_id": payload.get("asset_id", "USDT"),
        "network_id": payload.get("network_id", "TRON"),
        "address": "TRUDMIPREFERENCEADDRESS000000000",
        "memo": None,
    }
    remember_command("wallet:deposit-address", x_idempotency_key, fingerprint, response)
    return response


@app.get("/v1/wallet/deposits", dependencies=[Depends(require_private_auth)])
def list_deposits() -> dict[str, list[dict[str, object]]]:
    return {"items": DEPOSITS}


@app.get("/v1/wallet/withdrawals", dependencies=[Depends(require_private_auth)])
def list_withdrawals() -> dict[str, list[dict[str, object]]]:
    return {"items": WITHDRAWALS}


@app.post(
    "/v1/wallet/withdrawals",
    status_code=201,
    dependencies=[Depends(require_private_auth)],
    response_model=None,
)
def create_withdrawal(
    payload: dict[str, object],
    x_idempotency_key: str | None = Header(default=None),
) -> dict[str, object] | JSONResponse:
    if validation_error := validate_idempotency_key(x_idempotency_key):
        return validation_error
    assert x_idempotency_key is not None
    fingerprint = idempotency_fingerprint(payload)
    cached = cached_command("wallet:withdrawal", x_idempotency_key, fingerprint)
    if cached is not None:
        return cached
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
    remember_command("wallet:withdrawal", x_idempotency_key, fingerprint, withdrawal)
    return withdrawal


@app.post(
    "/v1/transfers",
    status_code=201,
    dependencies=[Depends(require_private_auth)],
    response_model=None,
)
def create_transfer(
    payload: dict[str, object],
    x_idempotency_key: str | None = Header(default=None),
) -> dict[str, object] | JSONResponse:
    if validation_error := validate_idempotency_key(x_idempotency_key):
        return validation_error
    assert x_idempotency_key is not None
    fingerprint = idempotency_fingerprint(payload)
    cached = cached_command("wallet:transfer", x_idempotency_key, fingerprint)
    if cached is not None:
        return cached
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
    remember_command("wallet:transfer", x_idempotency_key, fingerprint, transfer)
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
