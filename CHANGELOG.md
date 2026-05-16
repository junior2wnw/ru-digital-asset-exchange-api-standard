# Changelog

## 0.3.0

- Reframed the public project name as RU Digital Market Interoperability Profile, with RU-DAX retained as the exchange/trading core.
- Added L5 Compliance & Reporting specification for consent, AML/KYC boundary, audit events, regulatory report descriptors, and currency-control references.
- Added private L5 REST endpoints: `/v1/compliance/profile`, `/v1/compliance/consents`, `/v1/compliance/audit-events`, and `/v1/reports/regulatory`.
- Added L5 JSON Schema, mock venue responses, SDK methods, Postman coverage, and conformance tests.
- Updated Russian positioning, legal alignment, standard, white paper, roadmap, README, and package versions to Draft 0.3.

## 0.2.0

- Added `/v1/profile` for venue roles, compatibility levels, capabilities, legal profiles, and data governance.
- Added participant profile documentation for exchanges, brokers, banks, OIS CFA, OOTSFA, custody, wallet providers, market makers, issuers, compliance, analytics, and developer tools.
- Added Russian legal alignment notes for CFA, digital ruble, AML/KYC, personal data, currency control, experimental legal regimes, Open API consent, and mining/tax reporting.
- Added optional law-aware instrument fields: legal classification, regulatory scope, investor access, payment-use flag, and jurisdiction.
- Added L5 Compliance & Reporting as the next compatibility target.
- Updated mock exchange, OpenAPI, JSON Schema, Python SDK, TypeScript SDK, and L0 conformance tests.

## 0.1.0

- Initial draft of the RU-DAX interoperability profile.
- Added submission package for policy outreach: Duma, Bank of Russia, Ministry of Finance.
- Added white paper and go-to-market strategy.
- Added REST, WebSocket, FIX, wallet, error, market model, and conformance specs.
- Added OpenAPI and JSON Schema drafts.
- Added Python SDK reference implementation.
- Added TypeScript SDK reference implementation.
- Added FastAPI mock exchange.
- Added conformance test suite.
- Added Postman collection and GitHub Actions CI template.
