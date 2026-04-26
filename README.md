# RU Digital Asset Exchange API Standard

Draft открытого API-профиля для совместимой инфраструктуры цифровых активов, цифровой валюты и производных инструментов.

Проект решает простую задачу: дать рынку общий технический язык. Не монополию SDK, не “обязать всех пользоваться одной библиотекой”, не официальную позицию регулятора, а проверяемый открытый профиль: спецификации, схемы, SDK, mock exchange и conformance tests.

## Короткая Формула

Если государство или рынок выбирают курс на единый открытый API, то:

1. закон или акт регулятора фиксирует принцип совместимости;
2. технические требования утверждаются после отраслевого и юридического обсуждения;
3. открытый draft, SDK и тесты становятся готовой отправной точкой для пилота;
4. участники рынка внедряют совместимость не по презентации, а по conformance tests.

Этот репозиторий не является нормативным актом и не связан с Банком России, Госдумой или иной государственной организацией. Это независимая open-source инициатива и технический draft.

## Что Внутри

| Раздел | Назначение |
| --- | --- |
| `docs/` | White paper, позиционирование, безопасность, governance, roadmap |
| `spec/` | Технические профили REST, WebSocket, FIX, market model, wallet model |
| `schemas/` | OpenAPI и JSON Schema для машинной совместимости |
| `sdks/python/` | Python SDK как reference client |
| `sdks/typescript/` | TypeScript SDK как reference client |
| `mock-exchange/` | Reference mock exchange для sandbox и локальных тестов |
| `tests/conformance/` | Conformance test suite для проверки совместимости |
| `postman/` | Postman collection для ручной проверки |
| `docs/GITHUB_ACTIONS_CI.example.yml` | Шаблон CI для включения после выдачи GitHub `workflow` scope |

## Как Это Называть

Техническое название:

**RU Digital Asset Exchange API Standard**

Более точное позиционирование:

**RU-DAX Interoperability Profile**

Reference implementation:

**SpreadX SDK**

Так разделяются три вещи: стандарт, профиль совместимости и конкретная библиотека.

## Область Покрытия

Профиль не ограничивается spot API. Он проектируется с запасом на полный жизненный цикл биржевой и брокерской инфраструктуры:

- spot trading;
- margin trading;
- perpetual futures;
- dated futures;
- options;
- swaps и другие деривативы;
- единая модель ордеров, сделок, балансов, комиссий, лимитов и ошибок;
- wallet, deposits, withdrawals, address book, travel rule metadata;
- custody, subaccounts, internal transfers, audit trail;
- market data через REST и WebSocket;
- private events через WebSocket;
- FIX-compatible profile для профессиональных участников;
- sandbox/testnet;
- conformance tests;
- reference mock exchange.

## Принципы

1. Простота интеграции важнее внутренней сложности площадки.
2. Один инструментальный словарь должен покрывать spot, futures, options, swaps и новые продукты.
3. Ошибки, комиссии, лимиты и статусы должны быть машинно читаемыми.
4. Sandbox должен повторять production-контракт.
5. Совместимость доказывается тестами, а не декларацией.
6. SDK помогает внедрять профиль, но не становится обязательной монополией.
7. Любое нормативное использование требует правовой экспертизы и отраслевого пилота.

## Быстрый Старт

Терминал 1: mock exchange.

```powershell
cd mock-exchange
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install .
uvicorn spreadx_mock.app:app --reload --port 8080
```

Терминал 2: conformance tests.

```powershell
cd tests/conformance
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install .
pytest --base-url http://127.0.0.1:8080 --api-key sandbox-key
```

Python SDK:

```python
from spreadx import Client

client = Client("http://127.0.0.1:8080", api_key="sandbox-key")
print(client.time())
print(client.instruments())
print(client.balances())
```

TypeScript SDK:

```ts
import { SpreadXClient } from "@spreadx/sdk";

const client = new SpreadXClient({
  baseUrl: "http://127.0.0.1:8080",
  apiKey: "sandbox-key",
});

console.log(await client.time());
console.log(await client.instruments());
```

Windows note: если репозиторий лежит в пути с кириллицей, используйте обычный `pip install .`, а не editable install `pip install -e .`. Это снижает риск проблем с `.pth` файлами в некоторых настройках Windows/Python.

## Уровни Совместимости

| Уровень | Название | Проверяемая область |
| --- | --- | --- |
| L0 | Discovery | `/v1/time`, `/v1/instruments`, стандартные ошибки |
| L1 | Market Data | order book, trades, candles, WebSocket market streams |
| L2 | Trading | ордера, сделки, комиссии, лимиты, idempotency |
| L3 | Wallet & Custody | депозиты, выводы, адреса, transfers, subaccounts |
| L4 | Derivatives & FIX | positions, margin, funding, settlement, FIX-compatible profile |

## Правовая И Рыночная Линия

Сильная формула не в том, чтобы просить монополию для библиотеки. Сильная формула в том, чтобы предложить открытую совместимость:

| Цель | Реалистичность | Эффект |
| --- | --- | --- |
| Принцип единого открытого API в публичной политике | Средняя | Высокий |
| Технические требования в акте регулятора | Средняя/высокая | Очень высокий |
| SDK как open-source reference implementation | Высокая | Максимальный вход на рынок |

Практический путь:

1. Подготовить нейтральный draft и reference implementation.
2. Провести техническое обсуждение с биржами, брокерами, банками и разработчиками.
3. Провести юридическую и security-экспертизу.
4. Запустить пилот с conformance report.
5. Только после этого предлагать регуляторную формулировку.

## Кому Это Может Быть Полезно

- биржам и брокерам;
- банкам и финтех-компаниям;
- custodians и wallet-провайдерам;
- market makers;
- разработчикам торгового, учетного и риск-менеджмент ПО;
- отраслевым ассоциациям;
- регуляторным и аналитическим командам.

## Статус

Статус репозитория: **Draft 0.1**.

Это рабочий технический draft. До промышленного или нормативного использования нужны независимая правовая экспертиза, security review, отраслевое обсуждение и пилот с несколькими участниками рынка.

## Лицензия

Apache-2.0. Спецификации, SDK, mock exchange и тесты можно использовать, проверять, дорабатывать и внедрять в коммерческих и исследовательских проектах при соблюдении условий лицензии.
