# WebSocket Profile

The standard defines two WebSocket channels:

- public market data;
- private account events.

## Public Market Data

Endpoint:

```text
wss://api.example.com/v1/ws/market
```

Subscription message:

```json
{
  "op": "subscribe",
  "channel": "orderbook",
  "instrument_id": "BTC-RUB-SPOT",
  "depth": 50
}
```

Required channels:

- `ticker`;
- `trades`;
- `orderbook`;
- `candles`;
- `index_price`, if derivatives are supported;
- `mark_price`, if derivatives are supported;
- `funding_rate`, if perpetual futures are supported.

## Sequencing

Order book streams MUST include:

- `sequence`;
- `prev_sequence`;
- `snapshot` or `delta`;
- `instrument_id`;
- `event_time`.

Clients MUST resync if `prev_sequence` does not match the local sequence.

## Private Events

Endpoint:

```text
wss://api.example.com/v1/ws/private
```

Required channels:

- `orders`;
- `trades`;
- `balances`;
- `positions`;
- `wallet`;
- `risk`, if derivatives are supported.

Authentication SHOULD use challenge-response:

```json
{
  "op": "auth",
  "api_key": "public_key",
  "timestamp": "2026-04-27T00:00:00Z",
  "signature": "base64_signature"
}
```

## Event Envelope

All events use a common envelope:

```json
{
  "type": "event",
  "channel": "orders",
  "event_id": "evt_01HZZ",
  "sequence": 10001,
  "event_time": "2026-04-27T00:00:00Z",
  "data": {}
}
```

## Heartbeats

Server SHOULD send heartbeat every 15 seconds:

```json
{
  "type": "heartbeat",
  "server_time": "2026-04-27T00:00:00Z"
}
```

Client SHOULD reconnect if no heartbeat or event is received for 45 seconds.

