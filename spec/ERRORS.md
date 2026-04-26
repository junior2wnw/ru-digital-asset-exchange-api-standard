# Error Model

All APIs use a common error envelope.

```json
{
  "error": {
    "code": "ORDER_INSUFFICIENT_BALANCE",
    "message": "Insufficient available balance",
    "category": "business",
    "request_id": "req_01HZZ",
    "details": {}
  }
}
```

## Categories

| Category | Description |
| --- | --- |
| `validation` | Request shape or value is invalid |
| `authentication` | API key, signature, or session is invalid |
| `authorization` | Authenticated actor lacks required scope |
| `rate_limit` | Rate limit exceeded |
| `business` | Valid request cannot be completed under business rules |
| `risk` | Risk engine rejected the request |
| `compliance` | Compliance checks blocked the operation |
| `not_found` | Resource not found |
| `conflict` | Idempotency or state conflict |
| `system` | Internal or unavailable service |

## Standard Codes

| Code | Category | HTTP |
| --- | --- | --- |
| `INVALID_REQUEST` | `validation` | 400 |
| `INVALID_SIGNATURE` | `authentication` | 401 |
| `API_KEY_DISABLED` | `authentication` | 401 |
| `INSUFFICIENT_SCOPE` | `authorization` | 403 |
| `RESOURCE_NOT_FOUND` | `not_found` | 404 |
| `IDEMPOTENCY_CONFLICT` | `conflict` | 409 |
| `RATE_LIMIT_EXCEEDED` | `rate_limit` | 429 |
| `INSTRUMENT_HALTED` | `business` | 422 |
| `ORDER_INSUFFICIENT_BALANCE` | `business` | 422 |
| `ORDER_MIN_NOTIONAL` | `business` | 422 |
| `ORDER_PRICE_TICK_INVALID` | `validation` | 400 |
| `ORDER_QUANTITY_STEP_INVALID` | `validation` | 400 |
| `POSITION_LIMIT_EXCEEDED` | `risk` | 422 |
| `MARGIN_INSUFFICIENT` | `risk` | 422 |
| `WITHDRAWAL_ADDRESS_BLOCKED` | `compliance` | 422 |
| `WITHDRAWAL_LIMIT_EXCEEDED` | `business` | 422 |
| `SERVICE_UNAVAILABLE` | `system` | 503 |

## Requirements

- Error `code` MUST be stable.
- Error `message` SHOULD be safe to show to a user.
- Error `details` MAY contain structured debugging fields.
- Private data MUST NOT be leaked in error messages.

