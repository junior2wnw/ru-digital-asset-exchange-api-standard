# RU-DMIP Reference Sandbox

Reference sandbox implementation for the RU Digital Market Interoperability Profile draft.

Run locally:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install .
uvicorn ru_dmip_mock.app:app --reload --port 8080
```

All private endpoints require:

```text
X-API-Key: sandbox-key
X-Timestamp: <current UTC ISO-8601 timestamp>
X-Signature: hmac_sha256("sandbox-secret", timestamp + method + path + canonical_query + sha256(body))
```

The sandbox rejects stale timestamps, invalid signatures, and replayed signatures. An exact command repeat is accepted only with the same idempotency key; reuse of that key for a different command returns `IDEMPOTENCY_CONFLICT`.

The sandbox is intentionally deterministic and small. It exists to test clients, examples, Postman collections, and conformance checks.

Use `GET /v1/profile` to inspect the advertised participant roles, compatibility levels, capabilities, legal profiles, and data-governance contract.

Use `GET /v1/compliance/profile`, `/v1/compliance/consents`, `/v1/compliance/audit-events`, and `/v1/reports/regulatory` to inspect the L5 compliance and reporting surface.
