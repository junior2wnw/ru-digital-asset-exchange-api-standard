# RU-DMIP TypeScript Reference Client

Клиент на native `fetch`, напрямую отражающий REST-контракт профиля.

```ts
import { RuDmipClient } from "@ru-dmip/sdk";

const client = new RuDmipClient({
  baseUrl: "http://127.0.0.1:8080",
  apiKey: "sandbox-key",
  apiSecret: "sandbox-secret",
});

console.log(await client.profile());
console.log(await client.executionCapabilities());
console.log(await client.entitlementCapabilities());
```
