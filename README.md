# VPc06. PostgreSQL + psycopg2

Драйвер для работы с PostgreSQL на Python через `psycopg2`. CRUD-операции, транзакции, подключение через переменные окружения.

## Технологии

- Python 3.10+
- PostgreSQL 17
- psycopg2-binary
- python-dotenv

## Установка

```bash
git clone https://github.com/nokey-os/VPc06.-PostgreSQL-psycopg2.git
cd VPc06.-PostgreSQL-psycopg2
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Настройка

Создайте файл `.env` в корне проекта:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=ваш_пароль
```

## Запуск

```bash
python main.py
```

## Структура проекта

```
.
├── .env                  # Переменные окружения (не коммитится)
├── .gitignore
├── requirements.txt      # Зависимости
├── db.py                 # Драйвер — класс Database с CRUD-методами
├── main.py               # Пример использования драйвера
├── driver_usage.md       # Инструкция к драйверу
├── test_connection.py    # Тест подключения к PostgreSQL
└── test_db.py            # Тест методов драйвера
```

## Драйвер (db.py)

Класс `Database` — обёртка над psycopg2 с методами CRUD для таблицы `users`.

### Использование

```python
from db import Database

with Database() as db:
    db.create_table()
    db.insert_user("Иван", "ivan@example.com")
    users = db.get_all_users()
    print(users)
```

### Методы

| Группа | Метод | Описание |
|--------|-------|----------|
| CREATE | `insert_user(name, email)` | Добавление пользователя |
| CREATE | `insert_many_users(users)` | Массовая вставка |
| READ | `get_user_by_id(id)` | Поиск по ID |
| READ | `get_user_by_email(email)` | Поиск по email |
| READ | `get_all_users()` | Все пользователи |
| READ | `search_users_by_name(pattern)` | Поиск по имени |
| READ | `count_users()` | Количество записей |
| UPDATE | `update_user(id, name, email)` | Обновление данных |
| DELETE | `delete_user(id)` | Удаление по ID |
| DELETE | `delete_all_users()` | Удаление всех |

### Таблица users

| Поле | Тип | Описание |
|------|-----|----------|
| id | SERIAL PRIMARY KEY | Автоинкремент |
| name | VARCHAR(100) NOT NULL | Имя |
| email | VARCHAR(100) UNIQUE NOT NULL | Email |
| created_at | TIMESTAMP | Дата создания |
