# SpreadX TypeScript SDK

Reference TypeScript SDK for the RU-DAX interoperability profile draft.

```ts
import { SpreadXClient } from "@spreadx/sdk";

const client = new SpreadXClient({
  baseUrl: "http://127.0.0.1:8080",
  apiKey: "sandbox-key",
});

console.log(await client.time());
console.log(await client.instruments());
```

The SDK is intentionally tiny and readable. It uses the native `fetch` API and mirrors the REST profile directly.
