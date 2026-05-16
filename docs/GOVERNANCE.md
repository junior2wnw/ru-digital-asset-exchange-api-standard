# Governance

Цель governance: сделать стандарт открытым, нейтральным и пригодным для регулирования.

## Роли

**Maintainers** отвечают за целостность спецификации, совместимость и release process.

**Implementers** внедряют стандарт в биржах, брокерах, SDK и инфраструктурных системах.

**Reviewers** проверяют security, legal, market structure и developer experience.

**Legal reviewers** проверяют, что текст и API-контракт не создают ложного впечатления о праве деятельности, доступности продукта или допустимости обработки данных.

## Изменения

Каждое существенное изменение проходит через proposal:

1. Problem statement.
2. Proposed contract.
3. Backward compatibility.
4. Security impact.
5. Legal and data-governance impact.
6. Conformance impact.
7. Migration path.

## Версионирование

Стандарт использует SemVer:

- patch: исправления текста, не меняющие контракт;
- minor: совместимые расширения;
- major: breaking changes.

## Расширения

Vendor-specific расширения допустимы только через `extensions`. Они не должны менять смысл обязательных полей.

## Compatibility badges

Площадка может заявлять уровень:

- `RU-DMIP L0`;
- `RU-DMIP L1`;
- `RU-DMIP L2`;
- `RU-DMIP L3`;
- `RU-DMIP L4`;
- `RU-DMIP L5`.

Заявление уровня должно подтверждаться conformance report.

Для новых cross-market материалов SHOULD использоваться `RU-DMIP`. `RU-DAX` остается допустимым alias для exchange/trading core.
