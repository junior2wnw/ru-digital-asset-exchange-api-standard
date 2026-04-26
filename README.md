# RU Digital Asset Exchange API Standard

Открытый стандарт единого API для регулируемого рынка цифровой валюты РФ.

Короткая формула проекта:

> Закон говорит: у рынка должен быть единый открытый API.  
> Банк России утверждает требования.  
> Рынок получает готовый стандарт, SDK, схемы, sandbox и conformance tests.

Проект не предлагает монополию конкретной библиотеки. Он предлагает открытый стандарт и reference implementation, которую биржи, брокеры, банки, регуляторные интеграторы и разработчики могут использовать сразу.

## Что внутри

| Раздел | Назначение |
| --- | --- |
| `docs/` | White paper, стандарт, безопасность, governance, roadmap |
| `spec/` | Нормативные профили REST, WebSocket, FIX, market model, wallet model |
| `schemas/` | OpenAPI и JSON Schema для машинной совместимости |
| `sdks/python/` | Python SDK reference implementation |
| `sdks/typescript/` | TypeScript SDK reference implementation |
| `mock-exchange/` | Reference mock exchange для sandbox и локальных тестов |
| `tests/conformance/` | Conformance test suite для проверки бирж и брокеров |
| `postman/` | Postman collection для быстрого ручного тестирования |
| `docs/GITHUB_ACTIONS_CI.example.yml` | Готовый шаблон CI для включения после выдачи GitHub `workflow` scope |

## Названия стандарта

Рекомендуемое официальное название:

**RU Digital Asset Exchange API Standard**

Допустимый продуктовый профиль:

**SpreadX Unified Crypto Market API**

## Область покрытия

Стандарт проектируется не только для простого spot API. Он покрывает полный жизненный цикл рынка:

- spot trading;
- margin trading;
- perpetual futures;
- dated futures;
- options;
- swaps и другие деривативы;
- единые ордера, сделки, балансы, комиссии, лимиты и ошибки;
- wallet, deposits, withdrawals, address book, travel rule metadata;
- custody, subaccounts, transfers, audit trail;
- market data через REST и WebSocket;
- private events через WebSocket;
- FIX-compatible profile для профессиональных участников;
- sandbox/testnet;
- conformance tests;
- reference mock exchange.

## Принципы

1. Простота для разработчика важнее внутренней сложности биржи.
2. Одна модель инструмента должна описывать spot, futures, options и другие продукты.
3. Каждая ошибка должна быть машинно читаемой и одинаково трактуемой.
4. Sandbox обязан быть совместим с production API.
5. Conformance tests важнее презентаций: совместимость доказывается тестами.
6. SDK является reference implementation, а не обязательной монополией.
7. Стандарт должен быть пригоден для закона, акта ЦБ и промышленного внедрения.

## Быстрый старт

Запуск mock exchange:

```powershell
cd mock-exchange
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install .
uvicorn spreadx_mock.app:app --reload --port 8080
```

Проверка conformance tests:

```powershell
cd tests/conformance
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install .
pytest --base-url http://127.0.0.1:8080
```

Python SDK:

```python
from spreadx import Client

client = Client("http://127.0.0.1:8080")
print(client.time())
print(client.instruments())
```

TypeScript SDK:

```ts
import { SpreadXClient } from "@spreadx/sdk";

const client = new SpreadXClient({ baseUrl: "http://127.0.0.1:8080" });
console.log(await client.time());
console.log(await client.instruments());
```

## Уровни совместимости

| Уровень | Название | Требование |
| --- | --- | --- |
| L0 | Discovery | `/v1/time`, `/v1/instruments`, стандартные ошибки |
| L1 | Market Data | order book, trades, candles, WebSocket market streams |
| L2 | Trading | ордера, сделки, комиссии, лимиты, idempotency |
| L3 | Wallet & Custody | депозиты, выводы, адреса, transfers, subaccounts |
| L4 | Derivatives & FIX | positions, margin, funding, settlement, FIX-compatible profile |

## Правовая стратегия

Самая сильная формула:

| Цель | Реалистичность | Выгода |
| --- | --- | --- |
| Единый API в законе | Средняя | Высокая |
| Единый API в акте ЦБ | Высокая | Очень высокая |
| SDK как open-source reference implementation | Высокая | Максимальная для входа на рынок |

Лучший путь:

1. Закон фиксирует принцип: у регулируемого рынка должен быть единый открытый API.
2. Банк России утверждает технические требования.
3. Открытый стандарт и SDK становятся готовой reference implementation.
4. Биржи и брокеры внедряют совместимость, потому что тесты и SDK уже готовы.

## Адресаты

- Комитет Госдумы по финансовому рынку;
- Банк России;
- Минфин;
- Минцифры;
- Росфинмониторинг;
- РАКИБ;
- Ассоциация ФинТех;
- потенциальные российские биржи, брокеры, банки и инфраструктурные провайдеры.

## Статус

Статус репозитория: **Draft 0.1**.

Это рабочая спецификация и reference implementation. До использования в нормативных актах нужны правовая экспертиза, отраслевое обсуждение, security review и пилот с несколькими участниками рынка.

## Лицензия

Apache-2.0. Стандарт, SDK, mock exchange и тесты можно использовать, проверять, дорабатывать и внедрять в коммерческих и государственных проектах при соблюдении условий лицензии.
