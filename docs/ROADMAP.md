# Roadmap

Roadmap описывает проверяемые результаты, а не календарные обещания. Версия переходит в следующий статус только после появления соответствующих схем, reference behavior и conformance evidence.

## Current: Draft 0.5

Реализовано:

- discovery profile для ролей, capabilities и legal/data-governance boundaries;
- REST market data, trading, wallet и reference endpoints;
- universal execution semantics;
- compliance and reporting profile;
- entitlements and authorization profile;
- OpenAPI и JSON Schema;
- Python и TypeScript reference clients;
- reference sandbox и Postman collection;
- conformance suite уровней L0-L5;
- компактный pilot protocol со сценариями и критериями результата;
- российская law-aware рамка.

Текущие ограничения:

- WebSocket и FIX в основном описаны спецификацией, но покрыты тестами не полностью;
- нет второй независимой реализации;
- нет публичного формата подписанного conformance report;
- не проведены независимые legal и security review;
- нет подтвержденного отраслевого pilot report.

## 0.6 Pilot Ready

- Добавить reusable gap-report template к опубликованному pilot protocol.
- Добавить один внешний fixture или adapter example.
- Сформировать machine-readable conformance report.
- Добавить negative-path tests для подписи, replay, scope и protected-data leakage.
- Автоматизировать полный verify flow в CI.
- Проверить один сквозной сценарий с внешним участником на синтетических данных.

## 0.7 Event Completeness

- Завершить WebSocket snapshot/delta profile.
- Добавить sequence, replay и gap-recovery tests.
- Нормализовать private events для order, trade, wallet и authorization lifecycles.
- Проверить cancel/fill race и out-of-order delivery.
- Добавить operational status and incident feed.

## 0.8 Role Profiles

- Уточнить профили для банков, брокеров, организаторов торгов, ОИС/операторов обмена, цифровых депозитариев, custodians и analytics providers.
- Добавить role-specific capability requirements.
- Связать reporting descriptors с ролью и правовым контуром.
- Добавить migration guidance для существующих API.

## 0.9 Independent Implementation

- Подключить вторую независимую implementation.
- Измерить повторное использование клиентской логики.
- Опубликовать обезличенный gap report.
- Зафиксировать обязательные и необязательные extensions.
- Провести независимый security review.
- Провести профильную legal review.

## 1.0 Candidate

- Не менее двух независимых implementations.
- Воспроизводимые conformance reports.
- Стабильная governance procedure.
- Политика совместимости и deprecation.
- Security review report.
- Legal boundary review.
- Pilot evidence для минимум двух разных ролей.

## После 1.0

- дополнительные transport bindings;
- расширенные institutional/FIX профили;
- новые asset and entitlement types через proposal process;
- подписанные conformance attestations;
- tooling для сравнения capabilities и migration gaps.
