# Universal Execution Semantics

Version: Draft 0.5

This profile defines the universal execution layer of RU-DMIP. It is intentionally not a connector layer. It describes the market and execution objects that a regulated venue, broker, bank, infrastructure provider, strategy runtime, or terminal can use without leaking venue-specific implementation details into business logic.

## Purpose

The execution layer exists because a uniform REST shape is not enough. A serious integration also needs the same meaning for:

- order intent;
- execution legs;
- partial fills;
- cancel/fill races;
- acknowledgements;
- event ordering;
- replay;
- synthetic positions;
- risk constraints;
- stale market data;
- idempotent retries.

Connectors, adapters, signing rules, endpoint mapping, and venue-specific error parsing remain outside this profile. They may implement the profile, but they are not the profile.

## Core Rule

Generic systems MUST NOT branch on a venue name.

They SHOULD branch on:

- declared capabilities;
- instrument properties;
- legal and investor-access constraints;
- state-machine transitions;
- risk policy;
- latency/freshness policy;
- execution contract.

Venue-specific logic belongs only in the implementation boundary that translates between a venue and the universal contract.

## Objects

| Object | Role |
| --- | --- |
| `ExecutionCapabilityManifest` | Declares supported intent types, state machines, constraints, replay and event guarantees |
| `ExecutionIntent` | Describes what the client wants to achieve, not which low-level endpoint to call |
| `ExecutionLeg` | One executable component of an intent |
| `ExecutionContract` | Fill, acknowledgement, retry, cancellation, and race-condition semantics |
| `ExecutionEvent` | Ordered lifecycle event with correlation and causation identifiers |
| `SyntheticPosition` | Position assembled from one or more legs across accounts, instruments, or venues |
| `RiskConstraint` | Machine-readable limits and policy guards |
| `MarketDataQuality` | Freshness, sequence, source, and latency metadata used before execution |

## Endpoint

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/v1/execution/capabilities` | Universal execution semantics supported by this implementation |

The endpoint is public by default because it contains product and contract semantics, not private account data. Implementations MAY require authentication if capabilities are client-specific.

## Execution Intent

An execution intent SHOULD include:

- `intent_id`;
- `intent_type`;
- `created_at`;
- `client_ref`, if supplied by the client;
- `legs`;
- `constraints`;
- `execution_contract`;
- `correlation_id`;
- `extensions`.

Supported `intent_type` values:

- `single_order`;
- `basket`;
- `spread`;
- `hedge`;
- `rebalance`;
- `close_position`;
- `transfer`;
- `reporting_action`.

The profile treats `spread` as a first-class intent type. A spread is not a UI trick and not a pair of unrelated orders. It is a structured intent with legs, constraints, price/ratio targets, risk policy, and deterministic events.

## Execution Contract

The execution contract SHOULD declare:

- acknowledgement model: `sync`, `async`, or `eventual`;
- fill model: `atomic`, `partial_allowed`, or `best_effort`;
- cancel/fill race policy;
- retry policy;
- idempotency window;
- quantity semantics: planned, acknowledged, executed, settled;
- timeout policy;
- stale-data policy.

Clients SHOULD display planned quantity, acknowledged quantity, filled quantity, cancelled quantity, and rejected quantity separately.

## State Machine

The default execution state machine:

```text
created -> accepted -> working -> partially_filled -> filled
created -> rejected
accepted -> cancel_requested -> cancelled
working -> cancel_requested -> partially_cancelled
working -> expired
working -> failed
```

Implementations MAY add states through `extensions`, but MUST keep the base states meaningful.

## Event Model

Every execution event MUST include:

- `event_id`;
- `intent_id`;
- `sequence`;
- `event_type`;
- `state`;
- `event_time`;
- `correlation_id`;
- `causation_id`, if caused by another event or command;
- `resource_refs`;
- `details`.

Events MUST be replayable in sequence order. If an implementation cannot guarantee a gapless stream, it MUST declare the gap-recovery policy in the capability manifest.

## Market Data Quality

Before an execution intent is evaluated, market data SHOULD carry:

- `source_time`;
- `received_time`;
- `sequence`;
- `is_snapshot`;
- `is_replay`;
- `latency_ms`;
- `freshness_ms`;
- `quality_status`.

Supported `quality_status` values:

- `fresh`;
- `stale`;
- `gap_detected`;
- `recovered`;
- `unknown`.

Execution systems SHOULD reject or require confirmation when market data is stale beyond the declared policy.

## Synthetic Positions

A synthetic position can combine legs from different instruments, accounts, or venues. It SHOULD include:

- `synthetic_position_id`;
- `legs`;
- `net_exposure`;
- `pnl`;
- `margin_summary`;
- `risk_status`;
- `updated_at`.

This object lets portfolio and risk systems reason about the real exposure created by a strategy or spread without requiring every implementation to share the same internal ledger.

## Conformance

Conformance tests SHOULD verify:

- `/v1/execution/capabilities` exists;
- no capability requires a venue-specific branch in the client;
- state names and event ordering are stable;
- idempotency, replay, and cancel/fill race policies are declared;
- market-data quality states are declared;
- spread and synthetic-position support is declared as `supported`, `planned`, or `not_supported`.
