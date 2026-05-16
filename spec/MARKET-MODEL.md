# Market Model

The market model is the shared vocabulary for all APIs in this repository.

## Instruments

Every tradable product is an `Instrument`.

Required fields:

| Field | Type | Description |
| --- | --- | --- |
| `instrument_id` | string | Stable venue identifier, for example `BTC-RUB-SPOT` |
| `symbol` | string | Human readable symbol |
| `type` | enum | Product type |
| `base_asset` | string | Base asset |
| `quote_asset` | string | Quote asset or settlement currency |
| `status` | enum | Trading status |
| `price_tick` | decimal string | Minimum price increment |
| `quantity_step` | decimal string | Minimum quantity increment |
| `min_quantity` | decimal string | Minimum order quantity |
| `max_quantity` | decimal string | Maximum order quantity |
| `min_notional` | decimal string | Minimum notional value |
| `fee_schedule_id` | string | Fee schedule reference |
| `risk_profile_id` | string | Risk profile reference |

Supported `type` values:

- `spot`;
- `margin_spot`;
- `perpetual_future`;
- `dated_future`;
- `option`;
- `swap`;
- `index`;
- `structured_product`.

## Legal-Aware Instrument Fields

Technical product type and legal status are separate concepts. A venue SHOULD publish law-aware fields when the instrument can be affected by jurisdiction, investor access, payment restrictions, or experimental legal regimes.

Optional fields:

| Field | Type | Description |
| --- | --- | --- |
| `legal_classification` | enum | `digital_currency`, `digital_financial_asset`, `hybrid_digital_right`, `foreign_digital_right`, `digital_ruble`, `security`, `derivative`, `commodity`, `fiat_currency`, or `other` |
| `regulatory_scope` | enum | `production_ru_registered`, `experimental_legal_regime`, `foreign_market`, `sandbox`, or `implementation_defined` |
| `investor_access` | enum | `retail`, `qualified_investor`, `specially_qualified_investor`, `institutional`, `registered_user`, `not_applicable`, or `implementation_defined` |
| `payment_use_allowed` | boolean | Whether this instrument may be used as a payment leg in the advertised context |
| `jurisdiction` | string | Primary jurisdiction for the advertised product view |

These fields are informational for API clients. They do not replace legal review, investor classification, onboarding, platform rules, registry status, or an experimental legal regime.

Supported `status` values:

- `online`;
- `post_only`;
- `cancel_only`;
- `halted`;
- `settlement_only`;
- `delisted`.

## Derivative Fields

Derivative instruments add:

| Field | Required for | Description |
| --- | --- | --- |
| `underlying` | futures, options, swaps | Underlying asset, basket, or index |
| `settlement_asset` | futures, options, swaps | Asset used for settlement |
| `margin_asset` | leveraged instruments | Asset used for margin |
| `contract_size` | derivatives | Size of one contract |
| `expiry_time` | dated futures, options | Expiration timestamp |
| `strike_price` | options | Option strike |
| `option_type` | options | `call` or `put` |
| `funding_interval` | perpetual futures | Funding interval |
| `settlement_method` | derivatives | `cash`, `physical`, or `hybrid` |

## Orders

Order types:

- `market`;
- `limit`;
- `stop_market`;
- `stop_limit`;
- `take_profit_market`;
- `take_profit_limit`.

Time in force:

- `gtc`;
- `ioc`;
- `fok`;
- `gtd`;
- `post_only`.

Side:

- `buy`;
- `sell`.

Position intent:

- `open`;
- `close`;
- `reduce_only`;
- `close_position`.

Order lifecycle:

```text
accepted -> open -> partially_filled -> filled
accepted -> rejected
open -> cancel_pending -> cancelled
open -> expired
```

## Trades

A trade is an execution event. It is immutable after publication.

Required fields:

- `trade_id`;
- `instrument_id`;
- `exchange_order_id`;
- `side`;
- `price`;
- `quantity`;
- `quote_quantity`;
- `fee`;
- `liquidity_role`;
- `trade_time`.

`liquidity_role` values:

- `maker`;
- `taker`;
- `auction`;
- `liquidation`;
- `settlement`.

## Balances

Balances use decimal strings to avoid floating point errors.

Required fields:

- `asset_id`;
- `available`;
- `reserved`;
- `locked`;
- `total`;
- `credit`;
- `debt`;

Invariant:

```text
total = available + reserved + locked + credit - debt
```

Venues MAY use a more precise internal ledger, but public API values MUST preserve this invariant after rounding.

## Positions

Derivative positions include:

- `instrument_id`;
- `side`;
- `quantity`;
- `entry_price`;
- `mark_price`;
- `liquidation_price`;
- `unrealized_pnl`;
- `realized_pnl`;
- `initial_margin`;
- `maintenance_margin`;
- `leverage`;
- `margin_mode`.

`margin_mode` values:

- `isolated`;
- `cross`;
- `portfolio`.

## Fees

Fee model:

- maker fee;
- taker fee;
- withdrawal fee;
- funding payment;
- settlement fee;
- liquidation fee;
- custody fee, if applicable.

Fees MUST be returned as explicit objects, not embedded in free-form text.

## Limits

Limit categories:

- rate limits;
- order count limits;
- order size limits;
- notional limits;
- position limits;
- leverage limits;
- withdrawal limits;
- transfer limits.

Every limit response SHOULD include:

- current usage;
- maximum allowed;
- reset time, if applicable;
- scope.
