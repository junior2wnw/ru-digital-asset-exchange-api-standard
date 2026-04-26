export type DecimalString = string;

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

