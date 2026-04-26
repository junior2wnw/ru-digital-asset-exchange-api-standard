# REST API Profile

Base path: `/v1`.

All timestamps use RFC 3339 UTC. All decimal values use strings.

## Public Endpoints

| Method | Path | Description |
| --- | --- | --- |
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

