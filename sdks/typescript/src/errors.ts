export class SpreadXApiError extends Error {
  readonly code: string;
  readonly category?: string;
  readonly requestId?: string;
  readonly status: number;
  readonly details: Record<string, unknown>;

  constructor(args: {
    code: string;
    message: string;
    status: number;
    category?: string;
    requestId?: string;
    details?: Record<string, unknown>;
  }) {
    super(`${args.code}: ${args.message}`);
    this.name = "SpreadXApiError";
    this.code = args.code;
    this.category = args.category;
    this.requestId = args.requestId;
    this.status = args.status;
    this.details = args.details ?? {};
  }
}

