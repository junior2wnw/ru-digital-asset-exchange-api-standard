# Security Profile

Этот документ описывает базовый security profile для совместимой реализации. Он задает минимальные проверяемые свойства, но не заменяет threat model, требования регулятора, сертификацию средств защиты или внутренний контур управления риском.

## Модель Угроз

До production-запуска реализация MUST описать как минимум:

- кражу учетных данных и секретов;
- replay, подмену и повтор команд;
- превышение полномочий и ошибочное делегирование;
- компрометацию клиентского устройства или интеграционного сервиса;
- утечку персональных, финансовых и иных защищенных данных;
- злоупотребление выводом, переводом, выпуском, передачей или погашением прав;
- нарушение целостности журнала и невозможность восстановить цепочку событий;
- отказ внешнего провайдера идентификации, подписи, хранения или исполнения.

## Transport

- Production MUST использовать TLS 1.3 или актуальный регуляторно допустимый профиль.
- Sandbox SHOULD использовать тот же контракт и максимально близкий security profile.
- Секреты MUST NOT передаваться в query string.
- Высокорисковые межсистемные интеграции SHOULD использовать взаимную аутентификацию каналов.
- Если применимое право или модель угроз требуют сертифицированных средств криптографической защиты, выбор алгоритмов и средств остается обязанностью реализации и не выводится из conformance RU-DMIP.

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

Приватные REST-запросы MUST подписываться по строке:

```text
timestamp + method + path + canonical_query + sha256(body)
```

`canonical_query` формируется из всех пар query-параметров. Повторяющиеся параметры сохраняются; имена и значения кодируются в UTF-8 и percent-encoding по RFC 3986, пробел передается как `%20`, после чего закодированные пары сортируются побайтово сначала по имени, затем по значению. Подпись вычисляется как HMAC-SHA256 от этой строки с секретом ключа API. Sandbox использует пару `sandbox-key` / `sandbox-secret`; production MUST использовать собственные секреты, ротацию ключей и защищенное хранение.

HMAC - совместимый базовый механизм reference sandbox, а не единственный допустимый production-механизм. Реализация MAY объявить асимметричную подпись или иной согласованный профиль через capabilities. Для действий высокой значимости SHOULD применяться hardware-backed key storage, короткоживущие credentials, step-up authentication или раздельное подтверждение.

Заголовки:

- `X-API-Key`;
- `X-Timestamp`;
- `X-Signature`;
- `X-Idempotency-Key` для команд;
- `X-Request-ID` опционально.

## Replay Protection

Реализация MUST отклонять запросы с timestamp вне допустимого окна. Рекомендуемое окно: 30 секунд. Для команд высокой значимости одного timestamp недостаточно: SHOULD использоваться nonce или одноразовый идентификатор с серверным replay cache.

## Idempotency

Команды создания ордеров, отмены ордеров, создания депозитных адресов, выводов и transfers MUST поддерживать idempotency.

Повтор запроса с тем же idempotency key MUST возвращать тот же результат или ссылку на уже созданный ресурс.

Повторное использование ключа для другой команды или другого тела запроса MUST возвращать стабильную ошибку конфликта и не выполнять действие.

## WebSocket Auth

Private WebSocket sessions SHOULD использовать challenge-response:

1. Клиент открывает соединение.
2. Сервер отправляет challenge.
3. Клиент подписывает challenge API secret.
4. Сервер подтверждает session scopes.

## Audit Trail

Реализация MUST хранить аудит:

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
- `fx_control.references.read`;
- `entitlements.read`;
- `entitlements.evidence.read`;
- `entitlements.authorization.evaluate`.

Публичные endpoint не должны раскрывать персональные данные, банковскую тайну, KYC-документы, внутренние scoring rules, сведения ограниченного доступа или защищенные отчетные файлы. Если клиенту нужна выгрузка, API SHOULD отдавать protected reference, checksum, retention class и delivery channel, а не сам файл в публичном контуре.

## Правомочия И Авторизация (`Entitlements And Authorization`)

Чувствительные действия с правомочиями (`entitlements`) MUST быть deny-by-default. Для передачи, обременения, погашения, делегирования и чтения доказательств SHOULD применяться:

- request signing;
- timestamp and nonce replay protection;
- MFA or hardware-backed authentication;
- step-up authentication;
- scoped authorization;
- delegated authority checks;
- revocation checks;
- dual control for high-risk actions;
- tamper-evident audit log.

Bearer-only доступ без дополнительной проверки SHOULD NOT быть достаточным для чувствительных действий с правомочиями (`entitlements`).

## Incident Compatibility

Реализация SHOULD публиковать machine-readable status endpoint или status feed, чтобы клиенты могли отличать плановое ограничение от аварии.

Incident response SHOULD включать отзыв и ротацию credentials, сохранение доказательств, контролируемое ограничение операций, восстановление последовательности событий и уведомления в сроки, установленные применимыми требованиями.
