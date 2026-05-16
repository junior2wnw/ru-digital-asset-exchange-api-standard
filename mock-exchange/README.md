# SpreadX Mock Exchange

Reference sandbox implementation for the RU-DAX interoperability profile draft.

Run locally:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install .
uvicorn spreadx_mock.app:app --reload --port 8080
```

Private endpoints accept:

```text
X-API-Key: sandbox-key
```

The mock exchange is intentionally deterministic and small. It exists to test SDKs, demos, Postman collections, and conformance checks.

Use `GET /v1/profile` to inspect the advertised participant roles, compatibility levels, capabilities, legal profiles, and data-governance contract.
