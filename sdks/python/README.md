# SpreadX Python SDK

Reference Python SDK for the RU Digital Market Interoperability Profile draft.

```python
from spreadx import Client

client = Client("http://127.0.0.1:8080", api_key="sandbox-key")
print(client.time())
print(client.profile())
print(client.compliance_profile())
print(client.instruments())
print(client.create_order(
    instrument_id="BTC-RUB-SPOT",
    side="buy",
    type="limit",
    quantity="0.01",
    price="5000000",
))
```

The SDK intentionally stays small. It is a readable reference client for implementers and can grow into a production client without changing the public model.
