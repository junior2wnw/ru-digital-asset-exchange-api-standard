# RU-DMIP Python Reference Client

Небольшой читаемый клиент, повторяющий REST-контракт профиля без скрытой бизнес-логики.

```python
from ru_dmip import Client

client = Client(
    "http://127.0.0.1:8080",
    api_key="sandbox-key",
    api_secret="sandbox-secret",
)

print(client.profile())
print(client.execution_capabilities())
print(client.entitlement_capabilities())
```
