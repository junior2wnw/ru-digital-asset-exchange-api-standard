import { SpreadXApiError } from "./errors.js";
import type {
  AuditEvent,
  Balance,
  Candle,
  ComplianceProfile,
  ConsentRecord,
  AuthorizationDecision,
  AuthorizationDecisionRequest,
  ExecutionCapabilityManifest,
  Instrument,
  Order,
  Position,
  RegulatoryReport,
  Entitlement,
  EntitlementCapabilityManifest,
  Trade,
  VenueProfile,
  WalletAsset,
  WalletTransaction,
} from "./types.js";

type JsonObject = Record<string, unknown>;

export interface SpreadXClientOptions {
  baseUrl: string;
  apiKey?: string;
  apiSecret?: string;
  fetchImpl?: typeof fetch;
  secureHeaders?: () => Record<string, string> | Promise<Record<string, string>>;
}

export class SpreadXClient {
  private readonly baseUrl: string;
  private readonly apiKey?: string;
  private readonly apiSecret?: string;
  private readonly fetchImpl: typeof fetch;
  private readonly secureHeaders?: () => Record<string, string> | Promise<Record<string, string>>;

  constructor(options: SpreadXClientOptions) {
    this.baseUrl = options.baseUrl.replace(/\/$/, "");
    this.apiKey = options.apiKey;
    this.apiSecret = options.apiSecret;
    this.fetchImpl = options.fetchImpl ?? fetch;
    this.secureHeaders = options.secureHeaders;
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

  executionCapabilities(): Promise<ExecutionCapabilityManifest> {
    return this.request("GET", "/v1/execution/capabilities");
  }

  entitlementCapabilities(): Promise<EntitlementCapabilityManifest> {
    return this.request("GET", "/v1/entitlements/capabilities");
  }

  async entitlements(): Promise<Entitlement[]> {
    const data = await this.request<{ items: Entitlement[] }>("GET", "/v1/entitlements", { private: true });
    return data.items;
  }

  evaluateEntitlementAuthorization(decisionRequest: AuthorizationDecisionRequest): Promise<AuthorizationDecision> {
    return this.request("POST", "/v1/entitlements/authorization/evaluate", {
      private: true,
      body: decisionRequest as unknown as JsonObject,
    });
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

  complianceProfile(): Promise<ComplianceProfile> {
    return this.request("GET", "/v1/compliance/profile", { private: true });
  }

  async complianceConsents(): Promise<ConsentRecord[]> {
    const data = await this.request<{ items: ConsentRecord[] }>("GET", "/v1/compliance/consents", {
      private: true,
    });
    return data.items;
  }

  async auditEvents(limit = 100): Promise<AuditEvent[]> {
    const data = await this.request<{ items: AuditEvent[] }>("GET", "/v1/compliance/audit-events", {
      private: true,
      query: { limit },
    });
    return data.items;
  }

  async regulatoryReports(): Promise<RegulatoryReport[]> {
    const data = await this.request<{ items: RegulatoryReport[] }>("GET", "/v1/reports/regulatory", {
      private: true,
    });
    return data.items;
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

    const bodyPayload = options.body ? canonicalJson(options.body) : undefined;
    const headers: Record<string, string> = { Accept: "application/json" };
    if (bodyPayload) headers["Content-Type"] = "application/json";
    if (options.private && this.apiKey) headers["X-API-Key"] = this.apiKey;
    if (options.private && this.apiSecret) {
      Object.assign(headers, await signedHeaders(this.apiSecret, method, path, url, bodyPayload ?? ""));
    }
    if (options.private && this.secureHeaders) Object.assign(headers, await this.secureHeaders());
    if (options.idempotencyKey) headers["X-Idempotency-Key"] = options.idempotencyKey;

    const response = await this.fetchImpl(url, {
      method,
      headers,
      body: bodyPayload,
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

function canonicalJson(value: JsonObject): string {
  return JSON.stringify(sortJson(value));
}

function sortJson(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(sortJson);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .sort(([left], [right]) => left.localeCompare(right))
        .map(([key, nested]) => [key, sortJson(nested)]),
    );
  }
  return value;
}

async function signedHeaders(
  apiSecret: string,
  method: string,
  path: string,
  url: URL,
  body: string,
): Promise<Record<string, string>> {
  const timestamp = new Date().toISOString();
  const canonicalQuery = [...url.searchParams.entries()]
    .sort(([leftKey, leftValue], [rightKey, rightValue]) => (
      leftKey === rightKey ? leftValue.localeCompare(rightValue) : leftKey.localeCompare(rightKey)
    ))
    .map(([key, value]) => new URLSearchParams([[key, value]]).toString())
    .join("&");
  const bodyHash = await sha256Hex(body);
  const payload = `${timestamp}${method.toUpperCase()}${path}${canonicalQuery}${bodyHash}`;
  return {
    "X-Timestamp": timestamp,
    "X-Signature": await hmacSha256Hex(apiSecret, payload),
  };
}

async function sha256Hex(input: string): Promise<string> {
  const digest = await subtleCrypto().digest("SHA-256", new TextEncoder().encode(input));
  return toHex(digest);
}

async function hmacSha256Hex(secret: string, payload: string): Promise<string> {
  const crypto = subtleCrypto();
  const key = await crypto.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const signature = await crypto.sign("HMAC", key, new TextEncoder().encode(payload));
  return toHex(signature);
}

function subtleCrypto(): SubtleCrypto {
  const subtle = globalThis.crypto?.subtle;
  if (!subtle) {
    throw new Error("Web Crypto API is required for built-in request signing");
  }
  return subtle;
}

function toHex(buffer: ArrayBuffer): string {
  return [...new Uint8Array(buffer)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}
