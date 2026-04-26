# SpreadX Mock Exchange

Reference sandbox implementation for the RU Digital Asset Exchange API Standard.

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
