from __future__ import annotations

import httpx


def test_l5_compliance_profile(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    response = client.get("/v1/compliance/profile", headers=auth_headers)
    assert response.status_code == 200
    payload = response.json()
    assert payload["profile_id"] == "ru-dmip-l5"
    assert payload["level"] == "L5"
    assert payload["consent_required"] is True
    assert payload["personal_data_public_api_allowed"] is False
    assert "manual_review" in payload["status_vocabulary"]


def test_l5_consent_records_are_scoped(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    response = client.get("/v1/compliance/consents", headers=auth_headers)
    assert response.status_code == 200
    consent = response.json()["items"][0]
    assert consent["consent_id"]
    assert consent["subject_ref"].startswith("subject_")
    assert consent["status"] in {"active", "pending", "expired", "revoked", "rejected", "suspended"}
    assert consent["scopes"]
    assert "full_name" not in consent
    assert "passport_number" not in consent


def test_l5_audit_events(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    response = client.get("/v1/compliance/audit-events", headers=auth_headers)
    assert response.status_code == 200
    event = response.json()["items"][0]
    for field in [
        "audit_event_id",
        "event_type",
        "event_time",
        "actor_type",
        "actor_ref",
        "resource_type",
        "resource_id",
        "action",
        "result",
        "request_id",
        "retention_class",
    ]:
        assert field in event


def test_l5_regulatory_reports(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    response = client.get("/v1/reports/regulatory", headers=auth_headers)
    assert response.status_code == 200
    report = response.json()["items"][0]
    assert report["framework_id"]
    assert report["status"] in {
        "not_started",
        "preparing",
        "ready",
        "submitted",
        "accepted",
        "rejected",
        "cancelled",
        "expired",
    }
    assert report["delivery_channel"] == "protected_api"
    assert report["retention_class"] == "regulatory"
