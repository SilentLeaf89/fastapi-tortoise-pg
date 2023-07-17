## Тестовое задание по созданию API сервиса по расчёту стоимости страхования в зависимости от типа груза и объявленной стоимости (ОС).

[Текст задания](TASKS.md)

### Используемый стэк
- FastAPI
- Tortoise ORM
- Aerich
- PostgreSQL
- pytest

### Перед тем, как начать
Создайте файлы с переменными окружения:
- `.env` с таким же наполнением как и файл `.env.example`
- `.env.tests` в директории [tests](/tests) с таким же наполнением как и файл `.env.tests.example`.

### Запуск сервиса*
```
make dev
```
*Но можно начать и с `make build`. О командах make подробнее ниже.

### в `dev` среде API доступно по url:
- [openapi](http://127.0.0.1:8080/api/openapi/)

### Воспользуйтесь API
- раздел `Rate` реализует CRUD для тарифа страхования, можно добавить как один тариф за раз, так и использовать множественный ввод. Для это используйте `add/single` и `add/multiple` соответственно.
В качестве примера можете воспользоваться следующими Request body:
```
# /api/v1/rate/add/single
{
  "date": "2023-07-17",
  "cargo_type": "Aluminium",
  "rate": 0.007
}
```
или
```
# /api/v1/rate/add/multiple
{
  "2023-07-15": [
    {
      "cargo_type": "Steel",
      "rate": 0.025
    }
  ],
  "2023-07-16": [
    {
      "cargo_type": "Copper",
      "rate": 0.015
    }
  ],
  "2023-07-17": [
    {
      "cargo_type": "Aluminium",
      "rate": 0.007
    }
  ]
}
```

- раздел `Calculate` следует использовать после добавления тарифов в Rate с соответствующими комбинациями `"дата-тип груза"`, иначе Вы закономерно получите 404. Также предусмотрен расчет как одной позиции, так и множественный ввод. Для одиночной позиции используйте поля для заполнения. Во втором случае используйте предложенный формат данных, например:
```
{
  "2023-07-15": [
    {
      "cargo_type": "Steel",
      "declared_value": 1000000
    }
  ],
  "2023-07-16": [
    {
      "cargo_type": "Copper",
      "declared_value": 1000000
    }
  ],
  "2023-07-17": [
    {
      "cargo_type": "Aluminium",
      "declared_value": 1000000
    }
  ]
}
```
, где `declared_value` определяет объявленную стоимость груза.

- раздел `History` покажет Вам историю зарегистрированных событий (проведенных расчетов через `Calculate`). Используйте пагинацию, чтобы получать необходимые данные, ведь их может быть очень много.

### Тестирование кода
Для проведения тестирования выполните `make test`. Подробнее можно узнать в [Readme](/tests/README.MD)

### В Makefile также доступны следующие команды
- `make dev`        - запустить все контейнеры в dev режиме (без тестов)
- `make build`  - собрать все сервисы
- `make stop`   - остановить все сервисы
- `make logs`   - лог запущенного docker compose
- `make remove` - удалить все некорректно остановленные сервисы
- `make test`   - запуск контейнера с тестами

### Возможно Вы используете `docker-compose`, вместо `docker compose`
В этом случае подправьте в makefile переменную COMPOSE.
