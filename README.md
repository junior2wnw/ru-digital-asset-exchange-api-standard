# RU Digital Market Interoperability Profile

**RU-DMIP** is an open, testable API profile for digital market infrastructure.

Он задает общий контракт для подключения торговых площадок, банков, брокеров, операторов цифровых активов, кастодиальных и учетных систем, поставщиков данных и разработчиков. В центре проекта не конкретная платформа, а повторно используемая семантика: как обнаружить возможности участника, передать команду, проследить исполнение, проверить полномочия и подтвердить совместимость.

> Статус: **Draft 0.5 для технической оценки и пилотов**. Проект не является нормативным актом, лицензией, заключением о допустимости продукта или позицией государственного органа.

## Что решает профиль

Без общего контракта каждая интеграция заново определяет идентификаторы, статусы, ошибки, подпись запросов, правила повторов, события исполнения, кошельковые операции и отчетные данные. RU-DMIP выносит повторяющуюся часть в открытые спецификации и проверяет ее автоматически.

| Контур | Общий контракт | Проверка |
| --- | --- | --- |
| Discovery | роли, capabilities, версии и правовые границы | `/v1/profile` и L0 tests |
| Market data | инструменты, стакан, сделки и свечи | REST schemas и L1 tests |
| Trading & execution | заявки, idempotency, состояния, события и replay | L2 tests |
| Wallet & custody | активы, адреса, ввод, вывод и transfers | L3 tests |
| Derivatives | позиции, маржа, funding и settlement | L4 tests |
| Compliance | согласия, audit events и report descriptors | L5 tests |
| Entitlements | правомочия, доказательства и authorization decisions | L5 tests |

Профиль не требует одинаковой внутренней архитектуры. Реализация публикует поддерживаемые возможности, а клиент строит поведение по контракту и capabilities, а не по имени поставщика.

## Что уже есть

- OpenAPI и JSON Schema;
- REST, WebSocket и FIX-compatible спецификации;
- Python и TypeScript reference clients;
- локальный reference sandbox;
- Postman collection;
- 28 conformance-проверок уровней L0-L5;
- отдельные профили исполнения, безопасности, compliance и правомочий;
- правовые границы для применения в российском контуре.

## Проверка за 10 минут

Требуются Python 3.10+ и Node.js 20+.

Терминал 1:

```powershell
cd mock-exchange
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install .
uvicorn ru_dmip_mock.app:app --port 8080
```

Терминал 2:

```powershell
cd tests/conformance
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install .
pytest --base-url http://127.0.0.1:8080 --api-key sandbox-key --api-secret sandbox-secret
```

Для ручной проверки импортируйте
[`postman/RU-DMIP.postman_collection.json`](postman/RU-DMIP.postman_collection.json).

Python:

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

TypeScript:

```ts
import { RuDmipClient } from "@ru-dmip/sdk";

const client = new RuDmipClient({
  baseUrl: "http://127.0.0.1:8080",
  apiKey: "sandbox-key",
  apiSecret: "sandbox-secret",
});

console.log(await client.profile());
console.log(await client.executionCapabilities());
```

## Как оценить для пилота

Не нужно принимать весь профиль целиком. Достаточно выбрать один сквозной сценарий, сопоставить его с действующей моделью участника и зафиксировать:

1. какие сущности и статусы уже совпадают;
2. где контракт неоднозначен или избыточен;
3. какие проверки можно автоматизировать;
4. что должно остаться внутри реализации;
5. дает ли общий контракт экономию при следующем подключении.

Готовый формат сессии, сценарии и критерии результата описаны в
[`docs/PILOT.ru.md`](docs/PILOT.ru.md).

## Принципы

1. **Capabilities before assumptions.** Клиент сначала узнает возможности реализации.
2. **Stable semantics.** Статусы и события имеют одинаковый смысл у разных участников.
3. **Secure by default.** Приватные действия подписываются, ограничиваются scopes и журналируются.
4. **Law-aware, not law-substituting.** API показывает правовые границы, но не создает разрешение на деятельность.
5. **Data minimization.** В обычных ответах используются ссылки, хеши и статусы вместо лишних документов и персональных данных.
6. **Testable compatibility.** Заявленный уровень подтверждается conformance report.
7. **Incremental adoption.** Участник внедряет только нужные роли и уровни.

## Структура репозитория

| Раздел | Содержание |
| --- | --- |
| [`docs/`](docs/) | обзор, позиционирование, пилот, безопасность, правовая рамка и roadmap |
| [`spec/`](spec/) | нормативная техническая семантика профиля |
| [`schemas/`](schemas/) | OpenAPI и JSON Schema |
| [`mock-exchange/`](mock-exchange/) | reference sandbox |
| [`tests/conformance/`](tests/conformance/) | исполняемые проверки совместимости |
| [`sdks/`](sdks/) | Python и TypeScript reference clients |
| [`postman/`](postman/) | коллекция для ручного исследования API |

Исторические материалы обращений находятся в `submissions/`; они не являются частью технического контракта и не подтверждают поддержку проекта адресатами.

## Документы для разных задач

- [Технический стандарт](docs/STANDARD.ru.md)
- [Краткое позиционирование](docs/POSITIONING.ru.md)
- [White paper](docs/WHITEPAPER.ru.md)
- [Пилот и критерии оценки](docs/PILOT.ru.md)
- [Профили участников](docs/PARTICIPANT_PROFILES.ru.md)
- [Безопасность](docs/SECURITY.md)
- [Правовая рамка РФ](docs/RU_LEGAL_ALIGNMENT.ru.md)
- [Roadmap](docs/ROADMAP.md)
- [Governance](docs/GOVERNANCE.md)

## Участие

Замечание полезно, если оно содержит конкретный сценарий, несовместимость или риск. Для изменения контракта укажите problem statement, предлагаемые поля или поведение, влияние на обратную совместимость, безопасность, правовую границу и conformance tests. Подробности — в [CONTRIBUTING.md](CONTRIBUTING.md).

## Лицензия

Apache-2.0. Спецификации, схемы, reference implementations и тесты можно проверять, расширять и использовать при соблюдении условий лицензии.
