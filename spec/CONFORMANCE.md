# Conformance Profile

Conformance is test-based. A venue is compatible only for the levels it passes.

## Levels

| Level | Name | Scope |
| --- | --- | --- |
| L0 | Discovery | Venue profile, time, instruments, errors |
| L1 | Market Data | REST and WebSocket market data |
| L2 | Trading | Orders, trades, fees, limits, idempotency |
| L3 | Wallet & Custody | Deposits, withdrawals, transfers, subaccounts |
| L4 | Derivatives & FIX | Positions, margin, funding, settlement, FIX |
| L5 | Compliance & Reporting | Consent metadata, compliance statuses, audit events, report descriptors |

## Required Evidence

A conformance report SHOULD include:

- venue name;
- API base URL;
- environment: sandbox or production;
- standard version;
- date;
- level;
- test suite commit hash;
- passed tests;
- failed tests;
- waived tests with reason.

## Compatibility Rule

A venue MAY support optional extensions, but it MUST pass the mandatory tests for the claimed level without requiring a custom client.

## Sandbox Rule

Sandbox MUST use the same contract as production. Differences MAY exist only for:

- asset universe;
- balances;
- risk parameters;
- external blockchain broadcasting;
- compliance review simulation.
- regulator-specific reporting files.

## Badge Examples

- `RU-DMIP L0 Sandbox`;
- `RU-DMIP L2 Production`;
- `RU-DMIP L4 Institutional`;
- `RU-DMIP L5 Compliance & Reporting`.

`RU-DAX` remains an acceptable alias for the exchange/trading core. New cross-market reports SHOULD use `RU-DMIP`.
