# FIX-Compatible Profile

This profile is for professional market participants that require low-latency and institutional connectivity.

The profile is FIX-compatible, not a replacement for venue-specific FIX certification. It standardizes message semantics so REST, WebSocket, and FIX use the same market model.

## Sessions

Recommended session types:

- market data;
- order entry;
- drop copy;
- risk.

## Instrument Mapping

`SecurityID` SHOULD map to `instrument_id`.

`SecurityType` mapping:

| Instrument type | SecurityType |
| --- | --- |
| `spot` | `FOR` or venue-defined digital asset code |
| `perpetual_future` | `FUT` with `MaturityDate` omitted and `ContractMultiplier` present |
| `dated_future` | `FUT` |
| `option` | `OPT` |
| `swap` | `SWAP` |

## Orders

Core message types:

- `D` NewOrderSingle;
- `F` OrderCancelRequest;
- `G` OrderCancelReplaceRequest, optional;
- `8` ExecutionReport;
- `9` OrderCancelReject.

Required mapping:

| Standard field | FIX field |
| --- | --- |
| `client_order_id` | `ClOrdID` |
| `exchange_order_id` | `OrderID` |
| `instrument_id` | `SecurityID` |
| `side` | `Side` |
| `quantity` | `OrderQty` |
| `price` | `Price` |
| `time_in_force` | `TimeInForce` |
| `status` | `OrdStatus` |

## Drop Copy

Drop copy sessions SHOULD publish:

- execution reports;
- trade capture reports;
- fee events;
- position updates;
- funding and settlement events for derivatives.

## Risk

Professional participants SHOULD receive machine-readable risk data:

- position limits;
- margin usage;
- liquidation risk;
- order throttles;
- kill switch state.

## Certification

FIX compatibility MUST be tested against:

- session logon/logout;
- heartbeat and sequence reset;
- new order;
- cancel order;
- partial fill;
- full fill;
- reject;
- drop copy replay;
- risk event delivery.

