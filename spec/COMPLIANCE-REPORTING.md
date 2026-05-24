# Compliance and Reporting Profile

Version: Draft 0.5

This profile defines the L5 compatibility layer for consent, AML/KYC boundary, audit events, regulatory reports, and currency-control references.

L5 is not a public disclosure channel and not a legal permission. It is a structured, permissioned API surface that lets regulated implementations exchange the minimum metadata needed for compliance, audit, reporting, and operational reconciliation.

## Scope

L5 covers:

- consent and open API data-sharing metadata;
- AML/KYC and screening status vocabulary;
- audit events for orders, wallet operations, digital-right operations, reports, API keys, and consent changes;
- regulatory report descriptors and protected export references;
- currency-control document references for digital-right operations when applicable;
- retention, masking, access scope, and evidence-chain metadata.

L5 does not standardize:

- personal data payloads;
- copies of identity documents;
- bank secrecy or legally protected secrets;
- regulator-specific reporting forms;
- legal conclusions about whether an operation is permitted;
- internal scoring models, typologies, or monitoring rules.

## Endpoints

| Method | Path | Access | Description |
| --- | --- | --- | --- |
| `GET` | `/v1/compliance/profile` | private | Compliance, consent, audit, and reporting capabilities |
| `GET` | `/v1/compliance/consents` | private | Consent records and data-sharing scopes |
| `GET` | `/v1/compliance/audit-events` | private | Audit event feed with stable event ids |
| `GET` | `/v1/reports/regulatory` | private | Regulatory report descriptors and protected export references |

Implementations MAY expose narrower role-specific subsets. A bank, broker, OIS CFA, OOTSFA, custodian, or analytics provider can all claim L5 only for the scopes they actually support.

## Consent Model

Consent records SHOULD include:

- `consent_id`;
- `subject_ref`, a pseudonymous or internal reference;
- `subject_type`;
- `status`;
- `scopes`;
- `data_categories`;
- `purpose`;
- `legal_basis`;
- `granted_at`;
- `expires_at`, if applicable;
- `revoked_at`, if applicable.

Consent status values:

- `active`;
- `pending`;
- `expired`;
- `revoked`;
- `rejected`;
- `suspended`.

The API SHOULD expose enough data for reconciliation and revocation-aware flows. It SHOULD NOT expose personal data where a reference is sufficient.

## AML/KYC Boundary

Compliance statuses SHOULD be structured and conservative:

- `not_required`;
- `pending`;
- `approved`;
- `information_required`;
- `manual_review`;
- `rejected`;
- `blocked`;
- `expired`.

The status explains the machine state, not the full legal or risk analysis. Rejection reasons SHOULD use stable reason codes and SHOULD avoid exposing internal monitoring logic.

## Audit Events

Audit events MUST be immutable after publication.

Required fields:

- `audit_event_id`;
- `event_type`;
- `event_time`;
- `actor_type`;
- `actor_ref`;
- `resource_type`;
- `resource_id`;
- `action`;
- `result`;
- `request_id`;
- `retention_class`.

Audit event types SHOULD cover:

- order lifecycle;
- trade booking;
- balance movement;
- wallet operation;
- internal transfer;
- API key change;
- consent lifecycle;
- compliance decision;
- report generation;
- ruleset or platform-configuration change.

## Regulatory Reports

Report descriptors SHOULD include:

- `report_id`;
- `report_type`;
- `framework_id`;
- `period_start`;
- `period_end`;
- `status`;
- `generated_at`;
- `delivery_channel`;
- `protected_download_ref`, if available;
- `checksum`, if available;
- `retention_class`.

Report status values:

- `not_started`;
- `preparing`;
- `ready`;
- `submitted`;
- `accepted`;
- `rejected`;
- `cancelled`;
- `expired`.

The descriptor can be standardized even when the actual report file is jurisdiction-specific.

## Currency-Control References

When digital rights are used in foreign-trade or other currency-control relevant scenarios, L5 SHOULD provide structured references rather than free-form notes:

- contract reference;
- resident or non-resident classification when lawful to expose;
- document list status;
- authorized-bank interaction status;
- operation reference;
- reporting period.

The profile does not decide whether a specific currency operation is allowed. It only reserves stable fields for lawful implementations.

## Data Governance

L5 implementations SHOULD document:

- data categories;
- retention classes;
- masking rules;
- access scopes;
- lawful basis or consent model;
- incident notification boundary;
- export integrity checks;
- sandbox/production separation.

Every L5 endpoint MUST be protected by private authentication. Production implementations SHOULD use stronger authorization than a single API key when the data can affect client rights, reporting, or protected information.

## Conformance

An L5 conformance test can check the API shape, status vocabularies, and data-minimization guardrails. It cannot certify that an institution has the required legal status, registration, license, platform rules, or regulator acceptance.
