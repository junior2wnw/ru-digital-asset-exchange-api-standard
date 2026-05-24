# Entitlements and Authorization Profile

Version: Draft 0.5

This profile defines a small, universal, law-aware layer for entitlements and authorization. It does not create legal rights, transfer assets, replace a registry, or validate an issuer document. It lets a client safely answer three questions:

- what entitlement is visible to this subject;
- what restrictions and evidence references are attached to it;
- whether a proposed action is allowed, denied, or requires stronger authorization.

## Purpose

Digital market infrastructure needs more than balances and orders. A regulated participant may need to represent holdings, claims, custody interests, nominee records, pledge or encumbrance facts, voting or governance powers, access rights, settlement rights, and other lawful entitlements.

The optimal API surface is intentionally narrow. It standardizes metadata, authorization decisions, and evidence references. Production legal validity remains with the regulated implementation, registry records, platform rules, contracts, issuer documents, and applicable law.

## Core Rule

Entitlement APIs MUST be deny-by-default.

An implementation MUST NOT expose or allow an entitlement action unless all applicable checks pass:

- authentication assurance;
- authorization scope;
- subject role and delegated authority;
- consent and purpose limitation, if protected data is involved;
- legal classification and investor-access restrictions;
- sanctions, AML/KYC, fraud, and platform policy checks where applicable;
- entitlement status and encumbrance checks;
- audit and non-repudiation requirements.

Bearer-only access SHOULD NOT be sufficient for transfer, encumbrance, redemption, delegation, or evidence reads.

## Prohibited Entitlement Rule

Implementations MUST reject entitlements, terms, or requested actions that are illegal, discriminatory, exploitative, infringing, or otherwise contrary to the applicable legal regime.

The API SHOULD return a structured refusal reason such as `blocked_by_law`, `missing_legal_basis`, `insufficient_authority`, `infringing_term`, or `policy_blocked`.

## Endpoints

| Method | Path | Access | Description |
| --- | --- | --- | --- |
| `GET` | `/v1/entitlements/capabilities` | public or client-specific | Supported entitlement, authentication, authorization, evidence, and audit controls |
| `GET` | `/v1/entitlements` | private | Entitlements visible to the authenticated subject |
| `POST` | `/v1/entitlements/authorization/evaluate` | private | Authorization decision for a proposed entitlement action, without executing the action |

Capability discovery MAY be public because it describes supported controls. Implementations MAY require authentication if capabilities vary by client role.

## Entitlement Model

An entitlement SHOULD include:

- `entitlement_id`;
- `entitlement_type`;
- `status`;
- `holder_ref` and `holder_type`;
- `asset_ref`, `instrument_id`, `contract_ref`, or another object reference;
- `issuer_ref`, `registry_ref`, or platform reference, if applicable;
- `legal_classification`;
- `governing_framework`;
- `restrictions`;
- `encumbrances`;
- `evidence`;
- `authorization_policy_id`;
- `created_at` and `updated_at`;
- `extensions`.

Supported `entitlement_type` values include focused market primitives:

- `digital_asset_holding`;
- `digital_financial_asset`;
- `claim_right`;
- `monetary_claim`;
- `goods_delivery_claim`;
- `service_claim`;
- `work_performance_claim`;
- `ip_exclusive_right`;
- `ip_usage_right`;
- `revenue_share_right`;
- `governance_right`;
- `voting_right`;
- `access_right`;
- `custody_right`;
- `pledge_or_encumbrance`;
- `beneficial_interest`;
- `nominee_holding`;
- `settlement_right`;
- `other_lawful_right`.

`other_lawful_right` MUST include a legal basis, human-readable description, and implementation policy check before production use.

## Authentication

The profile separates authentication method from authentication assurance.

Supported methods may include:

- API key plus request signature;
- mutual TLS;
- OAuth 2.0 / OpenID Connect profiles;
- authorization code with PKCE for user-facing flows;
- hardware-backed key or WebAuthn-style authenticator;
- qualified electronic signature where legally required;
- trusted federated identity, if allowed by the implementation.

Sensitive entitlement actions SHOULD require high assurance and step-up authentication.

## Authorization

Authorization SHOULD combine:

- scopes;
- role-based access control;
- attribute-based access control;
- purpose limitation;
- delegated authority;
- transaction policy;
- dual control for high-risk actions;
- risk-based step-up;
- revocation checks;
- consent checks;
- legal and investor-access checks.

Authorization decisions MUST be explainable with machine-readable reason codes. The response MUST avoid exposing protected internal rules or personal data.

## Evidence and Audit

Evidence objects MUST avoid raw personal data and protected documents in ordinary API responses. They SHOULD contain references:

- `evidence_type`;
- `evidence_ref`;
- `evidence_hash`;
- `issued_at`;
- `issuer_ref`;
- `verification_status`;
- `protected_download_ref`, if the file is available through a protected channel.

Every sensitive entitlement action MUST produce an audit event with actor, subject, requested action, decision, reason codes, request id, and retention class.

## Conformance

Conformance tests SHOULD verify:

- entitlement capabilities are discoverable;
- sensitive actions declare high-assurance authentication requirements;
- private entitlement endpoints reject unsigned access;
- entitlement responses do not leak direct personal identifiers or protected documents;
- authorization decisions include `allow`, reason codes, assurance requirements, and audit policy;
- unlawful, discriminatory, or infringing actions are denied in a structured way.
