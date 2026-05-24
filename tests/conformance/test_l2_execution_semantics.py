from __future__ import annotations

import httpx


def test_l2_execution_capability_manifest(client: httpx.Client) -> None:
    response = client.get("/v1/execution/capabilities")
    assert response.status_code == 200
    payload = response.json()
    assert payload["profile_id"] == "ru-dmip-execution"
    assert "spread" in payload["intent_types"]
    assert "created" in payload["base_states"]
    assert "filled" in payload["base_states"]
    assert "fresh" in payload["quality_statuses"]
    assert payload["replay"]["supported"] is True
    assert payload["idempotency"]["required_for_commands"] is True
    assert payload["venue_specific_logic_boundary"] == "adapter_only"


def test_l2_execution_contract_declares_race_and_stale_data_policy(client: httpx.Client) -> None:
    response = client.get("/v1/execution/capabilities")
    assert response.status_code == 200
    contracts = response.json()["contracts"]
    assert "partial_allowed" in contracts["fill_models"]
    assert contracts["cancel_fill_race_policy"] in {
        "event_ordering_wins",
        "venue_ack_wins",
        "requires_reconciliation",
    }
    assert contracts["stale_data_policy"] in {
        "reject",
        "warn",
        "require_confirmation",
        "implementation_defined",
    }
