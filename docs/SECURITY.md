# Security Profile

Этот документ описывает базовый security profile для совместимой площадки.

## Transport

- Production MUST использовать TLS 1.3 или актуальный регуляторно допустимый профиль.
- Sandbox SHOULD использовать тот же контракт и максимально близкий security profile.
- Секреты MUST NOT передаваться в query string.

## API Keys

Ключи MUST иметь scopes:

- `read`;
- `trade`;
- `wallet`;
- `transfer`;
- `fix`;
- `admin`.

Ключи SHOULD поддерживать:

- IP allowlist;
- expiration;
- rotation;
- subaccount binding;
- read-only mode;
- withdrawal address restrictions.

## REST Signature

Private REST request SHOULD подписываться по строке:

```text
timestamp + method + path + canonical_query + sha256(body)
```

Заголовки:

- `X-API-Key`;
- `X-Timestamp`;
- `X-Signature`;
- `X-Idempotency-Key` для команд;
- `X-Request-ID` опционально.

## Replay Protection

Площадка MUST отклонять запросы с timestamp вне допустимого окна. Рекомендуемое окно: 30 секунд.

## Idempotency

Команды создания ордеров, отмены ордеров, выводов и transfers MUST поддерживать idempotency.

Повтор запроса с тем же idempotency key MUST возвращать тот же результат или ссылку на уже созданный ресурс.

## WebSocket Auth

Private WebSocket sessions SHOULD использовать challenge-response:

1. Клиент открывает соединение.
2. Сервер отправляет challenge.
3. Клиент подписывает challenge API secret.
4. Сервер подтверждает session scopes.

## Audit Trail

Площадка MUST хранить аудит:

- создание и отмена ордеров;
- изменение статуса ордера;
- сделки;
- начисление комиссий;
- funding and settlement;
- депозиты;
- выводы;
- internal transfers;
- изменение API keys;
- изменение withdrawal address book.

## Incident Compatibility

Площадка SHOULD публиковать machine-readable status endpoint или status feed, чтобы клиенты могли отличать плановое ограничение от аварии.

