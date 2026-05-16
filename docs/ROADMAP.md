# Roadmap

## 0.3 L5 Compliance & Reporting

- Reframe the public project name as RU Digital Market Interoperability Profile, with RU-DAX as the exchange/trading core.
- Add L5 Compliance & Reporting profile.
- Add private L5 endpoints for compliance profile, consent records, audit events, and regulatory report descriptors.
- Add JSON Schema, OpenAPI, SDK, mock venue, Postman, and conformance coverage for L5.
- Add data-minimization and legal-boundary language for consent, AML/KYC, audit, regulatory reporting, and currency-control references.

## 0.2 Universal Market Profile

- Add `/v1/profile` for participant roles, capabilities, legal profiles, and data governance.
- Add participant-role model for exchanges, brokers, banks, OIS CFA, OOTSFA, custody, wallets, market makers, issuers, compliance, analytics, and developer tools.
- Add Russian law-aware alignment document.
- Add optional law-aware instrument fields: legal classification, regulatory scope, investor access, payment-use flag, and jurisdiction.
- Add L5 Compliance & Reporting target level.

## 0.1 Draft

- Опубликовать white paper.
- Опубликовать модульную спецификацию.
- Добавить OpenAPI draft.
- Добавить JSON Schema draft.
- Добавить Python SDK skeleton.
- Добавить TypeScript SDK skeleton.
- Добавить mock venue.
- Добавить conformance tests.

## 0.4 Market Data

- REST order book, trades, candles, tickers.
- WebSocket snapshots and deltas.
- Replay and sequence model.
- Market data conformance tests.

## 0.5 Trading

- Unified order lifecycle.
- Idempotency and retry guidance.
- Fees and limits endpoints.
- Trading conformance tests.

## 0.6 Wallet & Custody

- Deposit addresses.
- Deposit and withdrawal lifecycle.
- Internal transfers.
- Subaccounts.
- Travel rule metadata profile.
- Wallet conformance tests.

## 0.7 Derivatives

- Perpetual futures.
- Dated futures.
- Options.
- Margin modes.
- Funding, settlement, liquidation data.
- Derivatives conformance tests.

## 0.8 Institutional

- FIX-compatible profile.
- Certification checklist.
- Operational monitoring.
- Security review checklist.
- Pilot package for regulators and industry associations.

## 0.9 Advanced Compliance & Reporting

- Role-specific reporting profiles for banks, OIS CFA, OOTSFA, custodians, brokers, and analytics providers.
- JSON Schema validation for L5 report descriptors.
- Negative-path tests for protected-data leakage.
- Optional report export job lifecycle.
- Tax/reporting hooks for supported roles.

## 1.0 Candidate

- At least two independent implementations.
- Public conformance reports.
- Legal review.
- Security review.
- Regulator-ready specification package.
