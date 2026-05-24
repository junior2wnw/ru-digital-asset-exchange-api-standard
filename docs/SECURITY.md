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
- `compliance`;
- `reporting`;
- `entitlements.read`;
- `entitlements.write`;
- `entitlements.transfer`;
- `entitlements.authorization.evaluate`;
- `audit`;
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
- изменение withdrawal address book;
- изменение consent records;
- создание, изменение, передача, обременение, погашение и делегирование прав;
- authorization decisions по чувствительным действиям;
- compliance decisions;
- создание и выгрузка отчетных наборов.

## L5 Protected Data

L5 Compliance & Reporting endpoints MUST be private. Они SHOULD использовать отдельные scopes:

- `consent.read`;
- `compliance.status.read`;
- `audit.events.read`;
- `reports.regulatory.read`;
- `fx_control.references.read`.
- `entitlements.read`;
- `entitlements.evidence.read`;
- `entitlements.authorization.evaluate`.

Публичные endpoint не должны раскрывать персональные данные, банковскую тайну, KYC-документы, внутренние scoring rules, сведения ограниченного доступа или защищенные отчетные файлы. Если клиенту нужна выгрузка, API SHOULD отдавать protected reference, checksum, retention class и delivery channel, а не сам файл в публичном контуре.

## Entitlements And Authorization

Чувствительные действия с entitlements MUST быть deny-by-default. Для передачи, обременения, погашения, делегирования и чтения доказательств SHOULD применяться:

- request signing;
- timestamp and nonce replay protection;
- MFA or hardware-backed authentication;
- step-up authentication;
- scoped authorization;
- delegated authority checks;
- revocation checks;
- dual control for high-risk actions;
- tamper-evident audit log.

Bearer-only доступ без дополнительной проверки SHOULD NOT быть достаточным для чувствительных действий с entitlements.

## Incident Compatibility

Площадка SHOULD публиковать machine-readable status endpoint или status feed, чтобы клиенты могли отличать плановое ограничение от аварии.
