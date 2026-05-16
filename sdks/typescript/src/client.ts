import { SpreadXApiError } from "./errors.js";
import type {
  Balance,
  Candle,
  Instrument,
  Order,
  Position,
  Trade,
  VenueProfile,
  WalletAsset,
  WalletTransaction,
} from "./types.js";

type JsonObject = Record<string, unknown>;

export interface SpreadXClientOptions {
  baseUrl: string;
  apiKey?: string;
  fetchImpl?: typeof fetch;
}

export class SpreadXClient {
  private readonly baseUrl: string;
  private readonly apiKey?: string;
  private readonly fetchImpl: typeof fetch;

  constructor(options: SpreadXClientOptions) {
    this.baseUrl = options.baseUrl.replace(/\/$/, "");
    this.apiKey = options.apiKey;
    this.fetchImpl = options.fetchImpl ?? fetch;
  }

  time(): Promise<{ server_time: string }> {
    return this.request("GET", "/v1/time");
  }

  profile(): Promise<VenueProfile> {
    return this.request("GET", "/v1/profile");
  }

  async instruments(filter?: { type?: string }): Promise<Instrument[]> {
    const data = await this.request<{ items: Instrument[] }>("GET", "/v1/instruments", { query: filter });
    return data.items;
  }

  instrument(instrumentId: string): Promise<Instrument> {
    return this.request("GET", `/v1/instruments/${encodeURIComponent(instrumentId)}`);
  }

  orderbook(instrumentId: string, depth = 50): Promise<{ instrument_id: string; sequence: number; bids: unknown[]; asks: unknown[]; event_time: string }> {
    return this.request("GET", "/v1/market/orderbook", {
      query: { instrument_id: instrumentId, depth },
    });
  }

  async publicTrades(instrumentId: string, limit = 100): Promise<Trade[]> {
    const data = await this.request<{ items: Trade[] }>("GET", "/v1/market/trades", {
      query: { instrument_id: instrumentId, limit },
    });
    return data.items;
  }

  async candles(instrumentId: string, interval: string, limit = 100): Promise<Candle[]> {
    const data = await this.request<{ items: Candle[] }>("GET", "/v1/market/candles", {
      query: { instrument_id: instrumentId, interval, limit },
    });
    return data.items;
  }

  async balances(): Promise<Balance[]> {
    const data = await this.request<{ items: Balance[] }>("GET", "/v1/account/balances", { private: true });
    return data.items;
  }

  async positions(): Promise<Position[]> {
    const data = await this.request<{ items: Position[] }>("GET", "/v1/account/positions", { private: true });
    return data.items;
  }

  async orders(filter?: { instrument_id?: string; status?: string }): Promise<Order[]> {
    const data = await this.request<{ items: Order[] }>("GET", "/v1/orders", {
      private: true,
      query: filter,
    });
    return data.items;
  }

  createOrder(order: JsonObject, idempotencyKey?: string): Promise<Order> {
    return this.request("POST", "/v1/orders", {
      private: true,
      body: order,
      idempotencyKey,
    });
  }

  cancelOrder(orderId: string, idempotencyKey?: string): Promise<Order> {
    return this.request("DELETE", `/v1/orders/${encodeURIComponent(orderId)}`, {
      private: true,
      idempotencyKey,
    });
  }

  async privateTrades(filter?: { instrument_id?: string; limit?: number }): Promise<Trade[]> {
    const data = await this.request<{ items: Trade[] }>("GET", "/v1/trades", {
      private: true,
      query: filter,
    });
    return data.items;
  }

  async walletAssets(): Promise<WalletAsset[]> {
    const data = await this.request<{ items: WalletAsset[] }>("GET", "/v1/wallet/assets", { private: true });
    return data.items;
  }

  createDepositAddress(assetId: string, networkId: string, idempotencyKey?: string): Promise<{ asset_id: string; network_id: string; address: string; memo?: string }> {
    return this.request("POST", "/v1/wallet/deposit-addresses", {
      private: true,
      body: { asset_id: assetId, network_id: networkId },
      idempotencyKey,
    });
  }

  async deposits(): Promise<WalletTransaction[]> {
    const data = await this.request<{ items: WalletTransaction[] }>("GET", "/v1/wallet/deposits", { private: true });
    return data.items;
  }

  async withdrawals(): Promise<WalletTransaction[]> {
    const data = await this.request<{ items: WalletTransaction[] }>("GET", "/v1/wallet/withdrawals", { private: true });
    return data.items;
  }

  createWithdrawal(withdrawal: JsonObject, idempotencyKey?: string): Promise<WalletTransaction> {
    return this.request("POST", "/v1/wallet/withdrawals", {
      private: true,
      body: withdrawal,
      idempotencyKey,
    });
  }

  createTransfer(transfer: JsonObject, idempotencyKey?: string): Promise<WalletTransaction> {
    return this.request("POST", "/v1/transfers", {
      private: true,
      body: transfer,
      idempotencyKey,
    });
  }

  private async request<T>(
    method: string,
    path: string,
    options: {
      private?: boolean;
      query?: Record<string, unknown>;
      body?: JsonObject;
      idempotencyKey?: string;
    } = {},
  ): Promise<T> {
    const url = new URL(`${this.baseUrl}${path}`);
    for (const [key, value] of Object.entries(options.query ?? {})) {
      if (value !== undefined && value !== null) {
        url.searchParams.set(key, String(value));
      }
    }

    const headers: Record<string, string> = { Accept: "application/json" };
    if (options.body) headers["Content-Type"] = "application/json";
    if (options.private && this.apiKey) headers["X-API-Key"] = this.apiKey;
    if (options.idempotencyKey) headers["X-Idempotency-Key"] = options.idempotencyKey;

    const response = await this.fetchImpl(url, {
      method,
      headers,
      body: options.body ? JSON.stringify(options.body) : undefined,
    });

    const data = (await response.json()) as JsonObject;
    if (!response.ok) {
      const error = (data.error ?? {}) as JsonObject;
      throw new SpreadXApiError({
        code: String(error.code ?? "HTTP_ERROR"),
        message: String(error.message ?? response.statusText),
        status: response.status,
        category: error.category ? String(error.category) : undefined,
        requestId: error.request_id ? String(error.request_id) : undefined,
        details: (error.details as Record<string, unknown>) ?? {},
      });
    }
    return data as T;
  }
}
