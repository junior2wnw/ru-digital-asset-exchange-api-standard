export type DecimalString = string;

export type OperatorRole =
  | "exchange"
  | "broker"
  | "bank"
  | "ois_cfa"
  | "ootsfa"
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
  | "trading"
  | "wallet_custody"
  | "derivatives"
  | "fix"
  | "cfa_issuance"
  | "cfa_exchange"
  | "digital_ruble"
  | "open_api_consent"
  | "aml_kyc"
  | "tax_reporting"
  | "fx_control"
  | "regulatory_reporting"
  | "audit_export"
  | "sandbox"
  | "conformance";

export type LegalFrameworkId =
  | "259-fz-cfa"
  | "161-fz-digital-ruble"
  | "115-fz-aml"
  | "152-fz-personal-data"
  | "173-fz-currency-control"
  | "258-fz-experimental-legal-regime"
  | "open-api-cbr-standards"
  | "mining-registry-tax"
  | "platform-rules"
  | "other";

export interface VenueProfile {
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
