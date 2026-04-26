# Governance

Цель governance: сделать стандарт открытым, нейтральным и пригодным для регулирования.

## Роли

**Maintainers** отвечают за целостность спецификации, совместимость и release process.

**Implementers** внедряют стандарт в биржах, брокерах, SDK и инфраструктурных системах.

**Reviewers** проверяют security, legal, market structure и developer experience.

## Изменения

Каждое существенное изменение проходит через proposal:

1. Problem statement.
2. Proposed contract.
3. Backward compatibility.
4. Security impact.
5. Conformance impact.
6. Migration path.

## Версионирование

Стандарт использует SemVer:

- patch: исправления текста, не меняющие контракт;
- minor: совместимые расширения;
- major: breaking changes.

## Расширения

Vendor-specific расширения допустимы только через `extensions`. Они не должны менять смысл обязательных полей.

## Compatibility badges

Площадка может заявлять уровень:

- `RU-DAX L0`;
- `RU-DAX L1`;
- `RU-DAX L2`;
- `RU-DAX L3`;
- `RU-DAX L4`.

Заявление уровня должно подтверждаться conformance report.

