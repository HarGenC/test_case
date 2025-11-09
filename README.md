Wallet API (FastAPI)

REST API для управления кошельками пользователей.  
Реализованы следующие эндпоинты:
1. Создание кошельков (/api/v1/wallets/create)
2. Изменение баланса (/api/v1/wallets/{wallet_uuid}/operation)
3. Проверка доступных средств (/api/v1/wallets/{wallet_uuid})

Стек используемых технологий:

**Python 3.11+**
**FastAPI**
**SQLAlchemy**
**PostgreSQL**
**Uvicorn**
**Pydantic** 
**Alembic**

.env файл содержит в себя следующие переменные:
DB_HOST - адрес БД
DB_PORT - порт БД
DB_NAME - название БД
DB_USER - имя пользователя
DB_PASS - пароль

DB_HOST_TEST - адрес тестовой БД
DB_PORT_TEST - порт тестовой БД
DB_NAME_TEST - название тестовой БД
DB_USER_TEST - имя тестового пользователя
DB_PASS_TEST - пароль

