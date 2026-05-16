# RU Digital Asset Exchange API Standard

Версия: Draft 0.2

Этот документ описывает техническое ядро RU-DAX Interoperability Profile. Это не официальный нормативный акт. Слова `MUST`, `SHOULD` и `MAY` используются только для проверки заявленного уровня API-совместимости:

- `MUST`: обязательно для заявленного уровня совместимости;
- `SHOULD`: настоятельно рекомендуется, отклонение требует объяснения;
- `MAY`: допустимое расширение.

## 1. Цель

Профиль задает единый API-контракт для инфраструктуры цифровых активов, цифровой валюты, цифрового рубля, ЦФА, открытых API и производных инструментов:

- биржи;
- брокеры;
- банки;
- market makers;
- custodians;
- wallet-провайдеры;
- аналитические и надзорные системы;
- разработчики торгового, учетного и риск-менеджмент ПО.
- compliance, RegTech и audit-команды.

Профиль не должен смешивать техническую совместимость и право деятельности. Если операция, инструмент или данные имеют правовое значение, API должен отдавать структурированный признак, а не прятать ограничение в свободном тексте.

## 2. Базовая Архитектура

Площадка, заявляющая совместимость с профилем, предоставляет:

1. `GET /v1/profile` для ролей, capabilities, уровней совместимости и law-aware контуров.
2. REST API для запросов и команд.
3. WebSocket market data для публичных потоков.
4. WebSocket private events для клиентских событий.
5. FIX-compatible profile для профессиональных участников.
6. Единые модели ордеров, сделок, балансов, ошибок, комиссий и лимитов.
7. Sandbox/testnet, совместимый с production-контрактом.
8. Conformance endpoint или публичную инструкцию для прохождения тестов.

## 2.1 Роли Участников

Площадка SHOULD публиковать в `/v1/profile` одну или несколько ролей:

- `exchange`;
- `broker`;
- `bank`;
- `ois_cfa`;
- `ootsfa`;
- `custodian`;
- `wallet_provider`;
- `payment_provider`;
- `market_maker`;
- `issuer`;
- `qualified_investor_gateway`;
- `compliance_provider`;
- `analytics_provider`;
- `developer_tool`;
- `regulator_observer`;
- `mining_infrastructure_operator`.

Роль не подтверждает лицензию, включение в реестр или право осуществлять деятельность. Она только описывает API-поверхность, которую заявляет реализация.

## 3. Идентификаторы

Площадка MUST использовать стабильные идентификаторы:

- `instrument_id`: стабильный id инструмента внутри площадки;
- `client_order_id`: idempotent id клиента;
- `exchange_order_id`: id ордера площадки;
- `trade_id`: id сделки;
- `account_id`: id аккаунта;
- `subaccount_id`: id субаккаунта;
- `asset_id`: id актива;
- `wallet_transaction_id`: id wallet-операции.

`client_order_id` MUST быть уникален в рамках аккаунта и торгового дня или более длинного окна, указанного площадкой.

## 4. Инструменты

Единая модель инструмента MUST покрывать:

- `spot`;
- `margin_spot`;
- `perpetual_future`;
- `dated_future`;
- `option`;
- `swap`;
- `index`;
- `structured_product`.

Каждый инструмент MUST публиковать:

- базовый и котируемый актив;
- статус торговли;
- price tick;
- quantity step;
- min/max order size;
- min notional;
- fee schedule reference;
- risk parameters;
- settlement model для деривативов;
- expiration для срочных инструментов;
- underlying для options и futures.

Инструмент SHOULD публиковать law-aware поля, если они применимы:

- `legal_classification`;
- `regulatory_scope`;
- `investor_access`;
- `payment_use_allowed`;
- `jurisdiction`.

## 5. Ордера

Площадка MUST поддерживать единую модель ордера:

- `market`;
- `limit`;
- `stop_market`;
- `stop_limit`;
- `take_profit_market`;
- `take_profit_limit`;
- `post_only`;
- `ioc`;
- `fok`;
- `reduce_only` для деривативов;
- `close_position` для деривативов.

Статусы:

- `accepted`;
- `open`;
- `partially_filled`;
- `filled`;
- `cancel_pending`;
- `cancelled`;
- `expired`;
- `rejected`.

## 6. Сделки

Сделка MUST содержать:

- `trade_id`;
- `instrument_id`;
- `exchange_order_id`;
- `client_order_id`, если применимо;
- `side`;
- `price`;
- `quantity`;
- `quote_quantity`;
- `fee`;
- `liquidity_role`;
- `trade_time`;
- `settlement_time`, если применимо.

## 7. Балансы И Позиции

Баланс актива MUST разделять:

- `available`;
- `reserved`;
- `locked`;
- `total`;
- `credit`;
- `debt`.

Для деривативов позиция MUST содержать:

- `instrument_id`;
- `side`;
- `quantity`;
- `entry_price`;
- `mark_price`;
- `liquidation_price`, если применимо;
- `unrealized_pnl`;
- `realized_pnl`;
- `initial_margin`;
- `maintenance_margin`;
- `leverage`;
- `margin_mode`.

## 8. Wallet И Custody

Площадка MUST предоставлять единые операции:

- список активов и сетей;
- депозитные адреса;
- историю депозитов;
- создание вывода;
- историю выводов;
- внутренние transfers;
- subaccounts;
- address book;
- статусы wallet-операций;
- fee estimate;
- travel rule metadata, если требуется применимым правом.

## 9. Ошибки

Каждая ошибка MUST возвращаться в формате:

```json
{
  "error": {
    "code": "ORDER_INSUFFICIENT_BALANCE",
    "message": "Insufficient available balance",
    "category": "business",
    "request_id": "req_01HZZ...",
    "details": {}
  }
}
```

Код ошибки MUST быть стабильным и машинно читаемым.

## 10. Комиссии И Лимиты

Площадка MUST публиковать:

- maker/taker fees;
- withdrawal fees;
- funding rules;
- settlement fees;
- rate limits;
- order limits;
- position limits;
- notional limits;
- leverage limits.

## 11. Безопасность

Private REST requests MUST включать:

- API key;
- timestamp;
- request signature;
- optional nonce;
- idempotency key для команд.

Площадка SHOULD поддерживать:

- IP allowlist;
- scoped keys;
- read-only keys;
- trading-only keys;
- wallet-only keys;
- institutional keys with FIX session mapping.

## 12. Расширения

Площадки MAY добавлять vendor-specific fields через объект `extensions`, не нарушая базовую схему.

Пример:

```json
{
  "instrument_id": "BTC-RUB-SPOT",
  "type": "spot",
  "extensions": {
    "venue_feature": "custom_value"
  }
}
```

Клиенты MUST игнорировать неизвестные поля, если они не меняют смысл обязательных полей.

## 13. Правовая Совместимость РФ

Для реализации в российском правовом контуре площадка SHOULD явно отделять:

- ЦФА, цифровую валюту, цифровой рубль, иностранные цифровые права, ценные бумаги, деривативы и обычные fiat balances;
- sandbox-возможность от production-допуска;
- технический статус операции от AML/KYC, валютного контроля, investor access и правил площадки;
- публичные market data от клиентских, персональных и охраняемых данных.

Минимальные law-aware capabilities:

- `aml_kyc`;
- `open_api_consent`;
- `digital_ruble`;
- `cfa_issuance`;
- `cfa_exchange`;
- `fx_control`;
- `tax_reporting`;
- `audit_export`;
- `regulatory_reporting`.

Если capability зависит от регистрации, лицензии, реестра, правил площадки или ЭПР, `/v1/profile` MUST показывать это через `legal_profiles.status`, а не через маркетинговое описание.
