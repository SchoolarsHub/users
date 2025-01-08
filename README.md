# Документация API users

## Эндпоинты

![Список эндпоинтов](https://i.imgur.com/fhDfQxH.jpeg)

#### POST /healthcheck
```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/api/v1/healthcheck' \
  -H 'accept: application/json' \
  -d ''
```
```json
{
  "status": 200,
  "result": {
    "status": "OK"
  }
}
```

#### POST /users/create_user
```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/api/v1/users/create_user' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "phone": 0,
  "email": "string",
  "firstname": "string",
  "lastname": "string",
  "middlename": "string"
}'
```
```json
{
  "status": 0,
  "result": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
##### Ошибки
###### 409 Пользователь уже существует
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 422 Invalid contacts
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
#### PUT /users/recovery-user
```bash
curl -X 'PUT' \
  'http://0.0.0.0:8000/api/v1/users/recovery-user' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}'
```
```json
{
  "status": 0,
  "result": "string"
}
```
##### Ошибки
###### 400 Пользователь уже активен
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 404 Пользователь не найден
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 422 Ошибка валидации
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

#### DELETE /users/delete-user-permanently
```bash
curl -X 'DELETE' \
  'http://0.0.0.0:8000/api/v1/users/delete-user-permanently' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}'
```
```json
{
  "status": 0,
  "result": "string"
}
```
##### Ошибки
###### 404 Пользователь не найден
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 422 Ошибка валидации
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

#### DELETE /users/delete-user-temporarily
```bash
curl -X 'DELETE' \
  'http://0.0.0.0:8000/api/v1/users/delete-user-temporarily' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}'
```
```json
{
  "status": 0,
  "result": "string"
}
```
##### Ошибки
###### 400 Пользователь уже временно удален
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 404 Пользователь не найден
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 422 Ошибка валидации
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```
#### PUT /users/change-fullname
```bash
curl -X 'PUT' \
  'http://0.0.0.0:8000/api/v1/users/change-fullname' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "firstname": "string",
  "lastname": "string",
  "middlename": "string"
}'
```
```json
{
  "status": 0,
  "result": "string"
}
```
##### Ошибки
###### 400 Пользователь уже временно удален
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 404 Пользователь не найден
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 422 Ошибка валидации
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```
#### PUT /users/change-contacts
```bash
curl -X 'PUT' \
  'http://0.0.0.0:8000/api/v1/users/change-contacts' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "email": "string",
  "phone": 0
}'
```
```json
{
  "status": 0,
  "result": "string"
}
```
##### Ошибки
###### 400 Пользователь уже временно удален
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 404 Пользователь не найден
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 409 Пользователь уже существует
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 422 Ошибка валидации
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

#### POST /users/link-social-network
```bash
curl -X 'POST' \
  'http://0.0.0.0:8000/api/v1/users/link-social-network' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "social_network": "vk",
  "connection_link": "string",
  "connected_for": "string"
}'
```
```json
{
  "status": 0,
  "result": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
##### Ошибки
###### 400 Пользователь уже временно удален
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 404 Пользователь не найден
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 409 Связанный аккаунт уже существует
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 422 Ссылка для подключения не принадлежит социальной сети
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```

#### DELETE /users/unlink-social-network
```bash
curl -X 'DELETE' \
  'http://0.0.0.0:8000/api/v1/users/unlink-social-network' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "linked_account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}'
```
```json
{
  "status": 0,
  "result": "string"
}
```
##### Ошибки
###### 400 Пользователь уже временно удален
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 404 Пользователь не найден
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 422 Ошибка валидации
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

#### PUT /users/change-social-network-connection-reason
```bash
curl -X 'PUT' \
  'http://0.0.0.0:8000/api/v1/users/change-social-network-connection-reason' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "linked_account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "reason": "string"
}'
```
```json
{
  "status": 0,
  "result": "string"
}
```
##### Ошибки
###### 400 Пользователь уже временно удален
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 404 Пользователь не найден
```json
{
  "status": 0,
  "error": {
    "title": "Error occurred",
    "data": {
      "message": "Domain Error occured"
    }
  }
}
```
###### 422 Ошибка валидации
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```


#### GET /users/{user_id}
```bash
curl -X 'GET' \
  'http://0.0.0.0:8000/api/v1/users/3fa85f64-5717-4562-b3fc-2c963f66afa6' \
  -H 'accept: application/json'
```
```json
{
  "status": 0,
  "result": {
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "status": "active",
    "created_at": "2025-01-07T13:32:33.394Z",
    "firstname": "string",
    "lastname": "string",
    "middlename": "string",
    "linked_accounts": [
      {
        "linked_account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "social_network": "vk",
        "connected_for": "string",
        "connection_link": "string",
        "connected_at": "2025-01-07T13:32:33.394Z"
      }
    ]
  }
}
```
##### Ошибки
###### 422 Ошибка валидации
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```
## Зависимости

### Инфраструктура 

- [Postgres](https://www.postgresql.org/docs/current/index.html) — База данных
- [RabbitMQ](https://www.rabbitmq.com/) — Очередь, используемая для публикации событий
- [Docker](https://docs.docker.com/) — Для развертывания

### Стек Grafana 

- [Grafana](https://grafana.com/docs/grafana/latest/) —  Веб-просмотр логов
- [Loki](https://grafana.com/docs/loki/latest/) — Платформа для хранения и запросов логов
- [Prometheus](https://prometheus.io/docs/introduction/overview/) — Система мониторинга для сбора метрик и алертинга.
- [Jaeger](https://www.jaegertracing.io/) — Инструмент для распределенного трассирования, помогающий отслеживать производительность микросервисов.
- [Promtail](https://grafana.com/docs/loki/latest/clients/promtail/) — Агент, который собирает логи и отправляет их в Loki.

###  Основные библиотеки python 

- [FastAPI](https://fastapi.tiangolo.com/) — Асинхронный веб-фреймворк;
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) — ORM для работы с базами данных;
- [asyncpg](https://asyncpg.org/) — Асинхронный драйвер для PostgreSQL;
- [dishka](https://github.com/reagento/dishka)— Библиотека для работы с конфигурациями и параметрами приложения;
- [pre-commit](https://pre-commit.com/) — Инструмент для управления хуками Git;
- [pytest](https://pytest.org/) — Фреймворк для тестирования на Python;
- [uvicorn](https://www.uvicorn.org/) — Асинхронный сервер для запуска приложений на основе ASGI;
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) — Инструмент для миграции схемы базы данных;
- [faststream](https://faststream.dev/) — Библиотека для работы с асинхронными потоками и очередями;
- [gunicorn](https://gunicorn.org/)  — WSGI HTTP сервер для UNIX;
- [adaptix](https://github.com/reagento/adaptix) — Библиотека для простой сериализации и сопоставления моделей.

### CI/CD

#### Триггеры
- События:
  - Когда происходит push в ветки `main` или `dev`.
  - При создании pull request в ветки `main` или `dev`.

#### Задания (jobs)

##### build
- Среда выполнения: `ubuntu-latest`.
- Шаги:
  - Checkout кода: Загрузка кода из репозитория с помощью `actions/checkout@v4`.
  - Установка `uv`: Установка `uv` с кэшированием зависимостей, используя `astral-sh/setup-uv@v4`. Кэширование зависит от файла `uv.lock`.
  - Настройка Python: Настройка Python с версией, указанной в файле `.python-version`, через `actions/setup-python@v5`.
  - Установка проекта: Выполнение команды `uv sync --all-extras --dev` для установки зависимостей проекта.

##### lint
- Зависимость: Это задание зависит от успешного завершения задания `build`.
- Среда выполнения: `ubuntu-latest`.
- Шаги:
  - Checkout кода: Загрузка кода из репозитория с помощью `actions/checkout@v4`.
  - Настройка Python: Настройка Python с той же версией, что указывается в файле `.python-version`, используя `actions/setup-python@v5`.
  - Установка `Ruff`: Установка линтера `Ruff` с помощью `astral-sh/ruff-action@v2`.
  - Запуск `Ruff`: Выполнение линтинга с помощью команды `ruff check --output-format=github .`, которая проверяет код и выводит результаты в формате GitHub.

#### tests
- Зависимость: Это задание также зависит от успешного завершения задания `build`.
- Среда выполнения: `ubuntu-latest`.
- Шаги:
  - Checkout кода: Загрузка кода из репозитория с использованием `actions/checkout@v4`.
  - Настройка Python: Настройка Python с той же версией, указанной в `.python-version`, через `actions/setup-python@v5`.
  - Установка `uv`: Установка `uv` аналогично заданию `build`, с кэшированием зависимостей.
  - Установка проекта: Выполнение команды `uv sync --all-extras --dev` для установки зависимостей проекта.
  - Запуск тестов: Выполнение тестов с использованием `pytest` через команду `uv run pytest`.
