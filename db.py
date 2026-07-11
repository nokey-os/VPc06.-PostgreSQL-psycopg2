# Импорт стандартного модуля для работы с переменными окружения
import os
# Импорт функции загрузки переменных из .env файла
from dotenv import load_dotenv
# Импорт адаптера PostgreSQL для Python
import psycopg2
# Импорт класса ошибок psycopg2 для обработки исключений БД
from psycopg2 import Error, sql
# Импорт модуля для работы с кортежами (используется в fetch-методах)
from typing import Optional

# Загрузка переменных окружения из файла .env в текущий процесс
load_dotenv()


class Database:
    """
    Класс-драйвер для работы с PostgreSQL.
    Предоставляет методы CRUD для таблицы users.
    Все параметры подключения считываются из переменных окружения (.env).
    """

    def __init__(self):
        """Инициализация подключения к базе данных."""
        self.conn = None
        self.cursor = None

    # ==================== ПОДКЛЮЧЕНИЕ ====================

    def connect(self):
        """Устанавливает подключение к PostgreSQL и создаёт курсор."""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),          # Хост PostgreSQL
                port=os.getenv("DB_PORT", "5432"),               # Порт PostgreSQL
                database=os.getenv("DB_NAME", "postgres"),       # Имя базы данных
                user=os.getenv("DB_USER", "postgres"),           # Пользователь
                password=os.getenv("DB_PASSWORD"),               # Пароль
            )
            self.cursor = self.conn.cursor()
            print("Подключение к базе данных установлено.")
        except Error as e:
            print(f"Ошибка подключения: {e}")

    def close(self):
        """Закрывает курсор и соединение с базой данных."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Соединение закрыто.")

    def commit(self):
        """Фиксирует изменения в базе данных (COMMIT транзакции)."""
        self.conn.commit()

    # ==================== СОЗДАНИЕ ТАБЛИЦЫ ====================

    def create_table(self):
        """Создаёт таблицу users, если она ещё не существует."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.commit()
            print("Таблица 'users' создана (или уже существует).")
        except Error as e:
            self.conn.rollback()
            print(f"Ошибка создания таблицы: {e}")

    # ==================== CREATE ====================

    def insert_user(self, name: str, email: str) -> Optional[int]:
        """
        Добавляет нового пользователя в таблицу users.

        Args:
            name: Имя пользователя.
            email: Email пользователя (уникальное).

        Returns:
            ID вставленной записи или None при ошибке.
        """
        try:
            self.cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING RETURNING id",
                (name, email)
            )
            self.commit()
            result = self.cursor.fetchone()
            if result is None:
                print(f"Пользователь с email '{email}' уже существует.")
                return None
            user_id = result[0]
            print(f"Пользователь добавлен с ID: {user_id}")
            return user_id
        except Error as e:
            self.conn.rollback()
            print(f"Ошибка добавления пользователя: {e}")
            return None

    def insert_many_users(self, users: list[tuple[str, str]]) -> bool:
        """
        Массовая вставка пользователей.

        Args:
            users: Список кортежей (name, email).

        Returns:
            True при успехе, False при ошибке.
        """
        try:
            self.cursor.executemany(
                "INSERT INTO users (name, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
                users
            )
            self.commit()
            print(f"Добавлено {len(users)} пользователей.")
            return True
        except Error as e:
            self.conn.rollback()
            print(f"Ошибка массовой вставки: {e}")
            return False

    # ==================== READ ====================

    def get_user_by_id(self, user_id: int) -> Optional[tuple]:
        """
        Получает пользователя по ID.

        Args:
            user_id: ID пользователя.

        Returns:
            Кортеж (id, name, email, created_at) или None.
        """
        try:
            self.cursor.execute(
                "SELECT id, name, email, created_at FROM users WHERE id = %s",
                (user_id,)
            )
            return self.cursor.fetchone()
        except Error as e:
            self.conn.rollback()
            print(f"Ошибка чтения пользователя: {e}")
            return None

    def get_user_by_email(self, email: str) -> Optional[tuple]:
        """
        Получает пользователя по email.

        Args:
            email: Email пользователя.

        Returns:
            Кортеж (id, name, email, created_at) или None.
        """
        try:
            self.cursor.execute(
                "SELECT id, name, email, created_at FROM users WHERE email = %s",
                (email,)
            )
            return self.cursor.fetchone()
        except Error as e:
            self.conn.rollback()
            print(f"Ошибка чтения пользователя: {e}")
            return None

    def get_all_users(self) -> list[tuple]:
        """
        Получает всех пользователей из таблицы.

        Returns:
            Список кортежей (id, name, email, created_at).
        """
        try:
            self.cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY id")
            return self.cursor.fetchall()
        except Error as e:
            self.conn.rollback()
            print(f"Ошибка чтения пользователей: {e}")
            return []

    def search_users_by_name(self, name_pattern: str) -> list[tuple]:
        """
        Ищет пользователей по части имени (регистронезависимо).

        Args:
            name_pattern: Часть имени для поиска.

        Returns:
            Список найденных пользователей.
        """
        try:
            self.cursor.execute(
                "SELECT id, name, email, created_at FROM users WHERE name ILIKE %s ORDER BY id",
                (f"%{name_pattern}%",)
            )
            return self.cursor.fetchall()
        except Error as e:
            self.conn.rollback()
            print(f"Ошибка поиска пользователей: {e}")
            return []

    def count_users(self) -> int:
        """
        Возвращает количество пользователей в таблице.

        Returns:
            Число записей в таблице users.
        """
        try:
            self.cursor.execute("SELECT COUNT(*) FROM users")
            return self.cursor.fetchone()[0]
        except Error as e:
            self.conn.rollback()
            print(f"Ошибка подсчёта пользователей: {e}")
            return 0

    # ==================== UPDATE ====================

    def update_user(self, user_id: int, name: str = None, email: str = None) -> bool:
        """
        Обновляет данные пользователя по ID.
        Обновляются только переданные поля (не None).

        Args:
            user_id: ID пользователя.
            name: Новое имя (или None для пропуска).
            email: Новый email (или None для пропуска).

        Returns:
            True если запись обновлена, False при ошибке.
        """
        try:
            updates = []
            values = []
            if name is not None:
                updates.append("name = %s")
                values.append(name)
            if email is not None:
                updates.append("email = %s")
                values.append(email)

            if not updates:
                print("Нет полей для обновления.")
                return False

            values.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            self.cursor.execute(query, values)
            self.commit()

            if self.cursor.rowcount > 0:
                print(f"Пользователь с ID {user_id} обновлён.")
                return True
            else:
                print(f"Пользователь с ID {user_id} не найден.")
                return False
        except Error as e:
            self.conn.rollback()
            print(f"Ошибка обновления пользователя: {e}")
            return False

    # ==================== DELETE ====================

    def delete_user(self, user_id: int) -> bool:
        """
        Удаляет пользователя по ID.

        Args:
            user_id: ID пользователя.

        Returns:
            True если запись удалена, False при ошибке.
        """
        try:
            self.cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.commit()

            if self.cursor.rowcount > 0:
                print(f"Пользователь с ID {user_id} удалён.")
                return True
            else:
                print(f"Пользователь с ID {user_id} не найден.")
                return False
        except Error as e:
            self.conn.rollback()
            print(f"Ошибка удаления пользователя: {e}")
            return False

    def delete_all_users(self) -> bool:
        """
        Удаляет всех пользователей из таблицы.

        Returns:
            True при успехе, False при ошибке.
        """
        try:
            self.cursor.execute("DELETE FROM users")
            self.commit()
            print("Все пользователи удалены.")
            return True
        except Error as e:
            self.conn.rollback()
            print(f"Ошибка удаления пользователей: {e}")
            return False

    # ==================== КОНТЕКСТНЫЙ МЕНЕДЖЕР ====================

    def __enter__(self):
        """Поддержка контекстного менеджера (with)."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрытие соединения при выходе из контекстного менеджера."""
        self.close()
        return False
