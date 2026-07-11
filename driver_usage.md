# PostgreSQL Driver for Python

Драйвер (модуль-обёртка) для работы с PostgreSQL через `psycopg2`.
Подключение к базе данных настраивается через переменные окружения в файле `.env`.

## Установка

```bash
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

## Быстрый старт

```python
from db import Database

with Database() as db:
    db.create_table()
    db.insert_user("Иван", "ivan@example.com")
    users = db.get_all_users()
    print(users)
```

## Методы драйвера

### Подключение

| Метод | Описание |
|---|---|
| `connect()` | Устанавливает подключение к PostgreSQL |
| `close()` | Закрывает соединение |
| `commit()` | Фиксирует изменения (COMMIT) |

Драйвер поддерживает контекстный менеджер — подключение и закрытие происходят автоматически.

### CREATE

| Метод | Описание |
|---|---|
| `create_table()` | Создаёт таблицу users (если не существует) |
| `insert_user(name, email)` | Добавляет пользователя, возвращает ID |
| `insert_many_users(users)` | Массовая вставка списка кортежей (name, email) |

### READ

| Метод | Описание |
|---|---|
| `get_user_by_id(id)` | Получение пользователя по ID |
| `get_user_by_email(email)` | Получение пользователя по email |
| `get_all_users()` | Список всех пользователей |
| `search_users_by_name(pattern)` | Регистронезависимый поиск по имени |
| `count_users()` | Количество пользователей |

### UPDATE

| Метод | Описание |
|---|---|
| `update_user(id, name, email)` | Обновление полей (передавайте только те, которые нужно изменить) |

### DELETE

| Метод | Описание |
|---|---|
| `delete_user(id)` | Удаление пользователя по ID |
| `delete_all_users()` | Удаление всех пользователей |

## Структура таблицы users

| Поле | Тип | Описание |
|---|---|---|
| id | SERIAL PRIMARY KEY | Автоматический счётчик |
| name | VARCHAR(100) NOT NULL | Имя пользователя |
| email | VARCHAR(100) UNIQUE NOT NULL | Email (уникальный) |
| created_at | TIMESTAMP | Дата создания (заполняется автоматически) |

## Использование во внешнем проекте

Скопируйте файл `db.py` и `.env` в свой проект, установите зависимости:

```bash
pip install psycopg2-binary python-dotenv
```

Импортируйте и используйте:

```python
from db import Database

with Database() as db:
    db.create_table()
    db.insert_user("Имя", "email@test.com")
```
