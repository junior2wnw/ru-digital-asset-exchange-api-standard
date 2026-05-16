# REST API Profile

Base path: `/v1`.

All timestamps use RFC 3339 UTC. All decimal values use strings.

## Public Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/v1/profile` | Venue roles, compatibility levels, capabilities, and legal profiles |
| `GET` | `/v1/time` | Server time |
| `GET` | `/v1/instruments` | List instruments |
| `GET` | `/v1/instruments/{instrument_id}` | Instrument details |
| `GET` | `/v1/market/orderbook` | Order book snapshot |
| `GET` | `/v1/market/trades` | Recent public trades |
| `GET` | `/v1/market/candles` | OHLCV candles |
| `GET` | `/v1/fees` | Public fee schedules |
| `GET` | `/v1/limits` | Public and authenticated limits |

## Private Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/v1/account/balances` | Account balances |
| `GET` | `/v1/account/positions` | Derivative positions |
| `GET` | `/v1/orders` | List orders |
| `POST` | `/v1/orders` | Create order |
| `DELETE` | `/v1/orders/{order_id}` | Cancel order |
| `GET` | `/v1/trades` | Private trade history |
| `GET` | `/v1/wallet/assets` | Assets and networks |
| `POST` | `/v1/wallet/deposit-addresses` | Create or get deposit address |
| `GET` | `/v1/wallet/deposits` | Deposit history |
| `POST` | `/v1/wallet/withdrawals` | Create withdrawal |
| `GET` | `/v1/wallet/withdrawals` | Withdrawal history |
| `POST` | `/v1/transfers` | Internal transfer |
| `GET` | `/v1/compliance/profile` | L5 compliance and reporting profile |
| `GET` | `/v1/compliance/consents` | Consent records and data-sharing scopes |
| `GET` | `/v1/compliance/audit-events` | Normalized audit events |
| `GET` | `/v1/reports/regulatory` | Regulatory report descriptors |

## Venue Profile

`GET /v1/profile` is the machine-readable entry point for every market participant.

It MUST return:

- `profile_id` and `profile_version`;
- primary `jurisdiction`;
- supported `operator_roles`;
- advertised `compatibility_levels`;
- feature `capabilities` with status `supported`, `sandbox_only`, `planned`, or `not_supported`;
- `legal_profiles` that explain applicable law-aware boundaries;
- `data_governance` for consent, personal data, retention, and audit trail responsibility.

The profile does not grant legal permission. It only declares the technical and operational contract a venue is willing to expose.

## L5 Compliance and Reporting

L5 endpoints are private. They standardize metadata and status vocabularies, not the disclosure of protected data.

Implementations MUST apply the same authentication and replay-protection rules as other private endpoints. Production implementations SHOULD add role-based authorization for:

- consent records;
- AML/KYC status reads;
- audit event feeds;
- regulatory report descriptors;
- protected export references;
- currency-control document references.

Clients MUST treat L5 responses as operational and compliance metadata. A conformance response does not prove that an organization has a license, registry status, investor classification, platform approval, regulator acceptance, or permission for a specific operation.

## Headers

Public requests:

- `Accept: application/json`;
- `X-Request-ID`, optional.

Private requests:

- `X-API-Key`;
- `X-Timestamp`;
- `X-Signature`;
- `X-Idempotency-Key` for commands;
- `X-Request-ID`, optional.

## Pagination

List endpoints SHOULD support cursor pagination:

Request:

```text
?limit=100&cursor=abc
```

Response:

```json
{
  "items": [],
  "next_cursor": "def"
}
```

## Filtering

Time range filters use:

- `from_time`;
- `to_time`;
- `limit`;
- `cursor`.

Trading filters use:

- `instrument_id`;
- `status`;
- `side`;
- `type`.

## Idempotency

The following operations MUST support `X-Idempotency-Key`:

- create order;
- cancel order;
- create withdrawal;
- create transfer;
- create deposit address, if address creation is asynchronous.

## Rate Limits

Responses SHOULD include:

- `X-RateLimit-Limit`;
- `X-RateLimit-Remaining`;
- `X-RateLimit-Reset`;
- `Retry-After` for HTTP 429.

## Error Format

All non-2xx responses MUST use the standard error envelope:

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "category": "rate_limit",
    "request_id": "req_01HZZ",
    "details": {
      "retry_after_ms": 1000
    }
  }
}
```
