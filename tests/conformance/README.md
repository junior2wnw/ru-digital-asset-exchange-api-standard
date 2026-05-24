# Conformance Tests

The conformance suite checks that a venue behaves like the RU Digital Market Interoperability Profile draft.

Run against the local mock venue:

```powershell
pytest --base-url http://127.0.0.1:8080 --api-key sandbox-key
```

Levels:

- L0: discovery, venue profile, and standard errors.
- L1: market data.
- L2: trading and universal execution semantics.
- L3: wallet and custody.
- L4: derivatives data surface.
- L5: compliance, entitlements, authentication, authorization, and reporting profile.

The suite is intentionally compact in Draft 0.5. Future versions should add WebSocket tests, FIX certification helpers, JSON Schema validation, legal-profile assertions, load tests, and negative-path risk checks.
