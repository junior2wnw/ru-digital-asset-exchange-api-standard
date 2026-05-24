from __future__ import annotations

import hashlib
import hmac
import json
from datetime import datetime, timezone
from urllib.parse import urlencode

import httpx


SANDBOX_API_SECRET = "sandbox-secret"


def signed_entitlement_headers(
    auth_headers: dict[str, str],
    method: str,
    path: str,
    *,
    body: str = "",
    query: dict[str, object] | None = None,
) -> dict[str, str]:
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    canonical_query = urlencode(sorted((query or {}).items()))
    body_hash = hashlib.sha256(body.encode()).hexdigest()
    payload = f"{timestamp}{method.upper()}{path}{canonical_query}{body_hash}"
    signature = hmac.new(SANDBOX_API_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return {
        **auth_headers,
        "X-Signature": signature,
        "X-Timestamp": timestamp,
    }


def test_l5_entitlement_capabilities_are_secure_by_default(client: httpx.Client) -> None:
    response = client.get("/v1/entitlements/capabilities")
    assert response.status_code == 200
    payload = response.json()
    assert payload["profile_id"] == "ru-dmip-entitlements-auth"
    assert payload["level"] == "L5"
    assert "claim_right" in payload["supported_entitlement_types"]
    assert "digital_financial_asset" in payload["supported_entitlement_types"]
    assert payload["minimum_assurance_for_sensitive_actions"] in {"high", "qualified_signature"}
    assert "deny_by_default" in payload["security_controls"]
    assert "request_signing" in payload["security_controls"]
    assert "step_up_for_entitlement_transfer" in payload["security_controls"]
    assert payload["prohibited_entitlement_policy"]["illegal_entitlements_rejected"] is True
    assert payload["prohibited_entitlement_policy"]["infringing_terms_rejected"] is True
    assert payload["evidence_policy"]["raw_documents_public_api_allowed"] is False
    assert payload["audit_required"] is True


def test_l5_entitlements_require_signed_private_access(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    missing_signature = client.get("/v1/entitlements", headers=auth_headers)
    assert missing_signature.status_code == 401

    invalid_headers = signed_entitlement_headers(auth_headers, "GET", "/v1/entitlements")
    invalid_headers["X-Signature"] = "invalid-signature"
    invalid_signature = client.get("/v1/entitlements", headers=invalid_headers)
    assert invalid_signature.status_code == 401

    response = client.get(
        "/v1/entitlements",
        headers=signed_entitlement_headers(auth_headers, "GET", "/v1/entitlements"),
    )
    assert response.status_code == 200
    entitlement = response.json()["items"][0]
    assert entitlement["entitlement_id"]
    assert entitlement["holder_ref"].startswith("subject_")
    assert entitlement["status"] in {"active", "encumbered", "suspended", "disputed", "blocked_by_law"}
    assert entitlement["evidence"]
    assert "full_name" not in entitlement
    assert "passport_number" not in entitlement
    assert entitlement["extensions"]["raw_documents_included"] is False


def test_l5_entitlement_authorization_denies_low_assurance_transfer(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    payload = {
        "subject_ref": "subject_demo_hash_001",
        "subject_type": "legal_entity",
        "action": "transfer",
        "resource_ref": "entitlement_demo_cfa_holding_1",
        "purpose": "pilot_transfer_check",
        "authentication_assurance": "low",
        "scopes": ["entitlements.transfer"],
        "requested_at": "2026-05-25T00:00:00Z",
    }
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    response = client.post(
        "/v1/entitlements/authorization/evaluate",
        headers={
            **signed_entitlement_headers(auth_headers, "POST", "/v1/entitlements/authorization/evaluate", body=body),
            "Content-Type": "application/json",
        },
        content=body,
    )
    assert response.status_code == 200
    decision = response.json()
    assert decision["allow"] is False
    assert "insufficient_authentication_assurance" in decision["reason_codes"]
    assert decision["step_up_required"] is True
    assert decision["audit_required"] is True


def test_l5_entitlement_authorization_blocks_unlawful_or_infringing_action(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    payload = {
        "subject_ref": "subject_demo_hash_001",
        "subject_type": "legal_entity",
        "action": "illegal_or_infringing_action",
        "resource_ref": "entitlement_demo_claim_services_1",
        "purpose": "negative_path",
        "authentication_assurance": "qualified_signature",
        "scopes": ["entitlements.write"],
        "requested_at": "2026-05-25T00:00:00Z",
    }
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    response = client.post(
        "/v1/entitlements/authorization/evaluate",
        headers={
            **signed_entitlement_headers(auth_headers, "POST", "/v1/entitlements/authorization/evaluate", body=body),
            "Content-Type": "application/json",
        },
        content=body,
    )
    assert response.status_code == 200
    decision = response.json()
    assert decision["allow"] is False
    assert "blocked_by_law" in decision["reason_codes"]
    assert "infringing_term" in decision["reason_codes"]
