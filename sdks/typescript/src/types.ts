export type DecimalString = string;

export type OperatorRole =
  | "exchange"
  | "broker"
  | "bank"
  | "ois_cfa"
  | "ootsfa"
  | "crypto_exchange"
  | "digital_depository"
  | "management_company"
  | "organized_trading_operator"
  | "custodian"
  | "wallet_provider"
  | "payment_provider"
  | "market_maker"
  | "issuer"
  | "qualified_investor_gateway"
  | "compliance_provider"
  | "analytics_provider"
  | "developer_tool"
  | "regulator_observer"
  | "mining_infrastructure_operator";

export type CompatibilityLevel = "L0" | "L1" | "L2" | "L3" | "L4" | "L5";

export type CapabilityId =
  | "discovery"
  | "market_data"
  | "execution_semantics"
  | "event_replay"
  | "synthetic_position"
  | "trading"
  | "wallet_custody"
  | "derivatives"
  | "fix"
  | "cfa_issuance"
  | "cfa_exchange"
  | "crypto_circulation"
  | "digital_ruble"
  | "open_api_consent"
  | "aml_kyc"
  | "tax_reporting"
  | "fx_control"
  | "regulatory_reporting"
  | "audit_export"
  | "entitlements"
  | "strong_authentication"
  | "authorization_policy"
  | "delegated_authority"
  | "sandbox"
  | "conformance";

export type LegalFrameworkId =
  | "259-fz-cfa"
  | "161-fz-digital-ruble"
  | "115-fz-aml"
  | "152-fz-personal-data"
  | "173-fz-currency-control"
  | "258-fz-experimental-legal-regime"
  | "63-fz-electronic-signature"
  | "open-api-cbr-standards"
  | "mining-registry-tax"
  | "ru-crypto-circulation-2026"
  | "platform-rules"
  | "other";

export interface ParticipantProfile {
  profile_id: "ru-dmip";
  profile_version: string;
  jurisdiction: string;
  operator_roles: OperatorRole[];
  compatibility_levels: CompatibilityLevel[];
  capabilities: Array<{
    capability_id: CapabilityId;
    level: CompatibilityLevel;
    status: "supported" | "sandbox_only" | "planned" | "not_supported";
    description?: string;
    extensions?: Record<string, unknown>;
  }>;
  legal_profiles: Array<{
    framework_id: LegalFrameworkId;
    status:
      | "applicable"
      | "requires_registration"
      | "requires_license_or_register"
      | "requires_experimental_regime"
      | "not_applicable"
      | "implementation_responsibility";
    applies_to: CapabilityId[];
    description?: string;
    source_url?: string;
  }>;
  data_governance: {
    client_consent_required: boolean;
    personal_data_policy: "not_applicable" | "implementation_responsibility" | "documented";
    audit_trail_required: boolean;
    retention_policy?: string;
    extensions?: Record<string, unknown>;
  };
  last_updated: string;
  extensions?: Record<string, unknown>;
}

export type ComplianceStatus =
  | "not_required"
  | "pending"
  | "approved"
  | "information_required"
  | "manual_review"
  | "rejected"
  | "blocked"
  | "expired";

export type ConsentStatus = "active" | "pending" | "expired" | "revoked" | "rejected" | "suspended";

export type ReportStatus =
  | "not_started"
  | "preparing"
  | "ready"
  | "submitted"
  | "accepted"
  | "rejected"
  | "cancelled"
  | "expired";

export interface ComplianceProfile {
  profile_id: "ru-dmip-l5";
  level: "L5";
  supported_scopes: string[];
  consent_required: boolean;
  personal_data_public_api_allowed: false;
  status_vocabulary: ComplianceStatus[];
  retention_classes: string[];
  extensions?: Record<string, unknown>;
}

export type ExecutionIntentType =
  | "single_order"
  | "basket"
  | "spread"
  | "hedge"
  | "rebalance"
  | "close_position"
  | "transfer"
  | "reporting_action";

export type ExecutionState =
  | "created"
  | "accepted"
  | "working"
  | "partially_filled"
  | "filled"
  | "cancel_requested"
  | "partially_cancelled"
  | "cancelled"
  | "expired"
  | "rejected"
  | "failed";

export type ExecutionQualityStatus = "fresh" | "stale" | "gap_detected" | "recovered" | "unknown";

export type ExecutionEventType =
  | "intent_created"
  | "intent_accepted"
  | "intent_rejected"
  | "order_acknowledged"
  | "fill_received"
  | "cancel_requested"
  | "cancel_acknowledged"
  | "risk_blocked"
  | "state_reconciled"
  | "replay_gap_detected";

export type ExecutionRiskConstraintType =
  | "max_notional"
  | "max_quantity"
  | "max_slippage"
  | "max_latency"
  | "reduce_only"
  | "position_limit"
  | "portfolio_exposure"
  | "legal_access"
  | "client_permission"
  | "freshness_required";

export interface ExecutionCapabilityManifest {
  profile_id: "ru-dmip-execution";
  profile_version: string;
  intent_types: ExecutionIntentType[];
  base_states: ExecutionState[];
  event_types: ExecutionEventType[];
  quality_statuses: ExecutionQualityStatus[];
  contracts: {
    acknowledgement_models: Array<"sync" | "async" | "eventual">;
    fill_models: Array<"atomic" | "partial_allowed" | "best_effort">;
    cancel_fill_race_policy: "event_ordering_wins" | "venue_ack_wins" | "requires_reconciliation";
    stale_data_policy: "reject" | "warn" | "require_confirmation" | "implementation_defined";
  };
  risk_constraints: ExecutionRiskConstraintType[];
  replay: {
    supported: boolean;
    sequence_policy: "gapless" | "monotonic_with_gaps" | "snapshot_plus_delta" | "implementation_defined";
    gap_recovery_policy: "resync_snapshot" | "replay_from_sequence" | "manual_reconciliation" | "not_supported";
  };
  idempotency: {
    required_for_commands: boolean;
    window: string;
  };
  venue_specific_logic_boundary: "adapter_only" | "implementation_boundary" | "not_declared";
  extensions?: Record<string, unknown>;
}

export type EntitlementType =
  | "digital_asset_holding"
  | "digital_financial_asset"
  | "claim_right"
  | "monetary_claim"
  | "goods_delivery_claim"
  | "service_claim"
  | "work_performance_claim"
  | "ip_exclusive_right"
  | "ip_usage_right"
  | "revenue_share_right"
  | "governance_right"
  | "voting_right"
  | "access_right"
  | "custody_right"
  | "pledge_or_encumbrance"
  | "beneficial_interest"
  | "nominee_holding"
  | "settlement_right"
  | "other_lawful_right";

export type EntitlementStatus =
  | "draft"
  | "active"
  | "suspended"
  | "encumbered"
  | "pending_transfer"
  | "transferred"
  | "redeemed"
  | "expired"
  | "cancelled"
  | "disputed"
  | "blocked_by_law";

export type EntitlementSubjectType =
  | "individual"
  | "legal_entity"
  | "public_entity"
  | "account"
  | "subaccount"
  | "nominee"
  | "beneficial_owner"
  | "qualified_investor_gateway"
  | "system";

export type AuthenticationMethod =
  | "api_key"
  | "request_signature"
  | "mutual_tls"
  | "oauth2_client_credentials"
  | "oauth2_authorization_code_pkce"
  | "hardware_key"
  | "webauthn"
  | "qualified_electronic_signature"
  | "trusted_federated_identity";

export type AuthenticationAssurance = "low" | "substantial" | "high" | "qualified_signature";

export type AuthorizationModel =
  | "scopes"
  | "rbac"
  | "abac"
  | "purpose_limitation"
  | "delegated_authority"
  | "transaction_policy"
  | "dual_control"
  | "risk_based_step_up"
  | "revocation_check"
  | "consent_check";

export type SecurityControl =
  | "least_privilege"
  | "deny_by_default"
  | "separation_of_duties"
  | "mfa_for_sensitive_operations"
  | "step_up_for_entitlement_transfer"
  | "request_signing"
  | "timestamp_and_nonce"
  | "replay_protection"
  | "idempotency"
  | "tamper_evident_audit_log"
  | "key_rotation"
  | "data_minimization"
  | "masking"
  | "revocation_check"
  | "protected_exports";

export type EntitlementAction =
  | "read"
  | "create"
  | "update"
  | "transfer"
  | "encumber"
  | "release_encumbrance"
  | "redeem"
  | "delegate"
  | "revoke_delegation"
  | "audit_read"
  | "evidence_read"
  | "illegal_or_infringing_action";

export type DecisionReasonCode =
  | "allowed"
  | "blocked_by_law"
  | "missing_legal_basis"
  | "insufficient_authority"
  | "insufficient_authentication_assurance"
  | "missing_scope"
  | "step_up_required"
  | "dual_control_required"
  | "entitlement_status_blocks_action"
  | "encumbrance_blocks_action"
  | "consent_required"
  | "policy_blocked"
  | "infringing_term";

export interface EntitlementCapabilityManifest {
  profile_id: "ru-dmip-entitlements-auth";
  profile_version: string;
  level: "L5";
  supported_entitlement_types: EntitlementType[];
  entitlement_statuses: EntitlementStatus[];
  subject_types: EntitlementSubjectType[];
  authentication_methods: AuthenticationMethod[];
  minimum_assurance_for_sensitive_actions: AuthenticationAssurance;
  authorization_models: AuthorizationModel[];
  security_controls: SecurityControl[];
  sensitive_actions: EntitlementAction[];
  supported_scopes?: string[];
  prohibited_entitlement_policy: {
    illegal_entitlements_rejected: true;
    infringing_terms_rejected: true;
    discriminatory_terms_rejected: true;
    lawful_basis_required: true;
  };
  evidence_policy: {
    raw_documents_public_api_allowed: false;
    hashes_supported: boolean;
    protected_download_refs_supported: boolean;
  };
  audit_required: true;
  extensions?: Record<string, unknown>;
}

export interface Entitlement {
  entitlement_id: string;
  entitlement_type: EntitlementType;
  status: EntitlementStatus;
  holder_ref: string;
  holder_type: EntitlementSubjectType;
  asset_ref?: string;
  instrument_id?: string;
  contract_ref?: string;
  issuer_ref?: string;
  registry_ref?: string;
  legal_classification: string;
  governing_framework: string;
  quantity?: DecimalString;
  unit?: string;
  restrictions: Array<{
    restriction_type: string;
    status: "active" | "inactive" | "waived" | "expired";
    framework_id?: string;
    description?: string;
  }>;
  encumbrances: Array<{
    encumbrance_type: string;
    status: "active" | "pending_release" | "released" | "disputed";
    beneficiary_ref?: string;
    evidence_ref?: string;
  }>;
  evidence: Array<{
    evidence_type: string;
    evidence_ref: string;
    evidence_hash?: string;
    issuer_ref?: string;
    issued_at?: string;
    verification_status: "not_checked" | "verified" | "failed" | "expired" | "revoked";
    protected_download_ref?: string;
  }>;
  authorization_policy_id: string;
  created_at: string;
  updated_at: string;
  extensions?: Record<string, unknown>;
}

export interface AuthorizationDecisionRequest {
  subject_ref: string;
  subject_type?: EntitlementSubjectType;
  action: EntitlementAction;
  resource_ref: string;
  purpose?: string;
  authentication_assurance?: AuthenticationAssurance;
  scopes?: string[];
  requested_at: string;
  extensions?: Record<string, unknown>;
}

export interface AuthorizationDecision {
  decision_id: string;
  allow: boolean;
  action: EntitlementAction;
  resource_ref: string;
  reason_codes: DecisionReasonCode[];
  required_assurance: AuthenticationAssurance;
  step_up_required?: boolean;
  dual_control_required?: boolean;
  audit_required: boolean;
  decided_at: string;
  extensions?: Record<string, unknown>;
}

export interface ConsentRecord {
  consent_id: string;
  subject_ref: string;
  subject_type: "individual" | "legal_entity" | "account" | "subaccount";
  status: ConsentStatus;
  scopes: string[];
  data_categories: string[];
  purpose: string;
  legal_basis: string;
  granted_at: string;
  expires_at?: string;
  revoked_at?: string;
  extensions?: Record<string, unknown>;
}

export interface AuditEvent {
  audit_event_id: string;
  event_type: string;
  event_time: string;
  actor_type: "user" | "system" | "operator" | "api_key" | "regulator";
  actor_ref: string;
  resource_type: string;
  resource_id: string;
  action: string;
  result: "success" | "failure" | "pending" | "blocked";
  request_id: string;
  retention_class: string;
  extensions?: Record<string, unknown>;
}

export interface RegulatoryReport {
  report_id: string;
  report_type: string;
  framework_id: string;
  period_start: string;
  period_end: string;
  status: ReportStatus;
  generated_at?: string;
  delivery_channel: string;
  protected_download_ref?: string;
  checksum?: string;
  retention_class: string;
  extensions?: Record<string, unknown>;
}

export type InstrumentType =
  | "spot"
  | "margin_spot"
  | "perpetual_future"
  | "dated_future"
  | "option"
  | "swap"
  | "index"
  | "structured_product";

export interface Instrument {
  instrument_id: string;
  symbol: string;
  type: InstrumentType;
  base_asset: string;
  quote_asset: string;
  status: "online" | "post_only" | "cancel_only" | "halted" | "settlement_only" | "delisted";
  price_tick: DecimalString;
  quantity_step: DecimalString;
  min_quantity: DecimalString;
  max_quantity: DecimalString;
  min_notional: DecimalString;
  fee_schedule_id: string;
  risk_profile_id: string;
  legal_classification?:
    | "digital_currency"
    | "digital_financial_asset"
    | "hybrid_digital_right"
    | "foreign_digital_right"
    | "digital_ruble"
    | "security"
    | "derivative"
    | "commodity"
    | "fiat_currency"
    | "other";
  regulatory_scope?:
    | "production_ru_registered"
    | "experimental_legal_regime"
    | "foreign_market"
    | "sandbox"
    | "implementation_defined";
  investor_access?:
    | "retail"
    | "qualified_investor"
    | "specially_qualified_investor"
    | "institutional"
    | "registered_user"
    | "not_applicable"
    | "implementation_defined";
  payment_use_allowed?: boolean;
  jurisdiction?: string;
  underlying?: string;
  settlement_asset?: string;
  margin_asset?: string;
  contract_size?: DecimalString;
  expiry_time?: string;
  strike_price?: DecimalString;
  option_type?: "call" | "put";
  funding_interval?: string;
  settlement_method?: "cash" | "physical" | "hybrid";
  extensions?: Record<string, unknown>;
}

export interface PriceLevel {
  price: DecimalString;
  quantity: DecimalString;
}

export interface Order {
  exchange_order_id: string;
  client_order_id?: string;
  instrument_id: string;
  side: "buy" | "sell";
  type: "market" | "limit" | "stop_market" | "stop_limit" | "take_profit_market" | "take_profit_limit";
  status: "accepted" | "open" | "partially_filled" | "filled" | "cancel_pending" | "cancelled" | "expired" | "rejected";
  quantity: DecimalString;
  filled_quantity: DecimalString;
  price?: DecimalString;
  average_price?: DecimalString;
  time_in_force?: "gtc" | "ioc" | "fok" | "gtd" | "post_only";
  position_intent?: "open" | "close" | "reduce_only" | "close_position";
  created_at: string;
  updated_at: string;
}

export interface Trade {
  trade_id: string;
  instrument_id: string;
  exchange_order_id: string;
  client_order_id?: string;
  side: "buy" | "sell";
  price: DecimalString;
  quantity: DecimalString;
  quote_quantity: DecimalString;
  fee: { asset_id: string; amount: DecimalString };
  liquidity_role: "maker" | "taker" | "auction" | "liquidation" | "settlement";
  trade_time: string;
  settlement_time?: string;
}

export interface Balance {
  asset_id: string;
  available: DecimalString;
  reserved: DecimalString;
  locked: DecimalString;
  total: DecimalString;
  credit: DecimalString;
  debt: DecimalString;
  updated_at?: string;
}

export interface Position {
  instrument_id: string;
  side: "long" | "short" | "flat";
  quantity: DecimalString;
  entry_price: DecimalString;
  mark_price: DecimalString;
  liquidation_price?: DecimalString;
  unrealized_pnl: DecimalString;
  realized_pnl: DecimalString;
  initial_margin: DecimalString;
  maintenance_margin: DecimalString;
  leverage: DecimalString;
  margin_mode: "isolated" | "cross" | "portfolio";
  updated_at?: string;
}

export interface Candle {
  open_time: string;
  close_time: string;
  open: DecimalString;
  high: DecimalString;
  low: DecimalString;
  close: DecimalString;
  volume: DecimalString;
}

export interface WalletAsset {
  asset_id: string;
  networks: Array<{
    network_id: string;
    deposit_enabled: boolean;
    withdrawal_enabled: boolean;
    min_confirmations?: number;
    withdrawal_fee?: DecimalString;
  }>;
}

export interface WalletTransaction {
  wallet_transaction_id: string;
  type: "deposit" | "withdrawal" | "transfer";
  asset_id: string;
  amount: DecimalString;
  status: string;
  created_at: string;
  updated_at: string;
  network_id?: string;
  fee?: DecimalString;
  address?: string;
  memo?: string;
  tx_hash?: string;
  confirmations?: number;
  from_account_id?: string;
  to_account_id?: string;
  travel_rule?: Record<string, unknown>;
}
