# Conformance Tests

The conformance suite checks that a venue behaves like the RU-DAX interoperability profile draft.

Run against the local mock exchange:

```powershell
pytest --base-url http://127.0.0.1:8080 --api-key sandbox-key
```

Levels:

- L0: discovery, venue profile, and standard errors.
- L1: market data.
- L2: trading.
- L3: wallet and custody.
- L4: derivatives data surface.
- L5: compliance and reporting profile (planned).

The suite is intentionally small in Draft 0.2. Future versions should add WebSocket tests, FIX certification helpers, JSON Schema validation, legal-profile assertions, load tests, and negative-path risk checks.
