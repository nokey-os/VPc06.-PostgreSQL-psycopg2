# Импорт стандартного модуля для работы с переменными окружения
import os
# Импорт функции загрузки переменных из .env файла
from dotenv import load_dotenv
# Импорт адаптера PostgreSQL для Python
import psycopg2
# Импорт класса ошибок psycopg2 для обработки исключений БД
from psycopg2 import Error


# Загрузка переменных окружения из файла .env в текущий процесс
load_dotenv()


def test_connection():
    """Тестовая функция проверки подключения к PostgreSQL."""
    # Инициализация переменной соединения как None для безопасного закрытия в finally
    connection = None
    try:
        # Установка подключения к базе данных с параметрами из .env
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),          # Хост PostgreSQL (по умолчанию localhost)
            port=os.getenv("DB_PORT", "5432"),               # Порт PostgreSQL (по умолчанию 5432)
            database=os.getenv("DB_NAME", "postgres"),       # Имя базы данных (по умолчанию postgres)
            user=os.getenv("DB_USER", "postgres"),           # Пользователь PostgreSQL (по умолчанию postgres)
            password=os.getenv("DB_PASSWORD"),               # Пароль из переменной окружения
        )

        # Создание курсора для выполнения SQL-запросов
        cursor = connection.cursor()

        # Запрос версии PostgreSQL для проверки подключения
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"Подключение успешно! Версия PostgreSQL: {db_version[0]}")

        # Запрос имени текущей базы данных и пользователя
        cursor.execute("SELECT current_database(), current_user;")
        db_info = cursor.fetchone()
        print(f"База данных: {db_info[0]}, Пользователь: {db_info[1]}")

        # Закрытие курсора после выполнения запросов
        cursor.close()
    except Error as e:
        # Обработка ошибок, связанных с PostgreSQL
        print(f"Ошибка подключения: {e}")
    finally:
        # Закрытие соединения независимо от результата выполнения
        if connection:
            connection.close()
            print("Соединение закрыто.")


if __name__ == "__main__":
    # Запуск тестовой функции проверки подключения
    test_connection()
