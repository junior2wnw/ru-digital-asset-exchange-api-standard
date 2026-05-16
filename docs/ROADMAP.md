# Roadmap

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
- Добавить mock exchange.
- Добавить conformance tests.

## 0.2 Market Data

- REST order book, trades, candles, tickers.
- WebSocket snapshots and deltas.
- Replay and sequence model.
- Market data conformance tests.

## 0.3 Trading

- Unified order lifecycle.
- Idempotency and retry guidance.
- Fees and limits endpoints.
- Trading conformance tests.

## 0.4 Wallet & Custody

- Deposit addresses.
- Deposit and withdrawal lifecycle.
- Internal transfers.
- Subaccounts.
- Travel rule metadata profile.
- Wallet conformance tests.

## 0.5 Derivatives

- Perpetual futures.
- Dated futures.
- Options.
- Margin modes.
- Funding, settlement, liquidation data.
- Derivatives conformance tests.

## 0.6 Institutional

- FIX-compatible profile.
- Certification checklist.
- Operational monitoring.
- Security review checklist.
- Pilot package for regulators and industry associations.

## 0.7 Compliance & Reporting

- Consent-aware Open API profile.
- AML/KYC status vocabulary.
- Audit export profile.
- Regulatory reporting metadata.
- Currency-control document references.
- Tax/reporting hooks for supported roles.

## 1.0 Candidate

- At least two independent implementations.
- Public conformance reports.
- Legal review.
- Security review.
- Regulator-ready specification package.
