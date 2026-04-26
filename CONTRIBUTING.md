# Contributing

Спасибо за интерес к RU Digital Asset Exchange API Standard.

## Как предлагать изменения

1. Опишите проблему.
2. Предложите контракт API или изменение схемы.
3. Объясните совместимость с текущими клиентами.
4. Добавьте или обновите conformance tests.
5. Обновите документацию.

## Требования к изменениям

- Decimal values должны оставаться строками.
- Новые поля должны быть обратно совместимыми или идти в major version.
- Vendor-specific поля должны жить в `extensions`.
- Ошибки должны использовать стандартный error envelope.
- Новые private commands должны поддерживать idempotency.

## Локальная проверка

```powershell
python -m json.tool schemas/json/instrument.schema.json
python -m json.tool postman/RU-DAX-Standard.postman_collection.json
```

Для полной проверки поднимите mock exchange и запустите conformance tests.
