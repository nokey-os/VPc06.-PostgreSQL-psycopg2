# Импорт драйвера для работы с PostgreSQL
from db import Database


if __name__ == "__main__":

    # ==================== ПРОВЕРКА ПОДКЛЮЧЕНИЯ ====================
    print("=" * 50)
    print("ПРОВЕРКА ПОДКЛЮЧЕНИЯ")
    print("=" * 50)

    with Database() as db:
        print("Драйвер успешно подключён к PostgreSQL.\n")

        # ==================== СОЗДАНИЕ ТАБЛИЦ ====================
        print("=" * 50)
        print("СОЗДАНИЕ ТАБЛИЦ")
        print("=" * 50)

        db.create_table()

        # ==================== DEMO CRUD ====================
        print("\n" + "=" * 50)
        print("DEMO CRUD-ОПЕРАЦИИ")
        print("=" * 50)

        # --- CREATE: вставка данных ---
        print("\n--- CREATE: добавление пользователей ---")
        id1 = db.insert_user("Алиса", "alice@example.com")
        id2 = db.insert_user("Боб", "bob@example.com")
        id3 = db.insert_user("Чарли", "charlie@example.com")

        # Массовая вставка
        db.insert_many_users([
            ("Давид", "david@example.com"),
            ("Ева", "eva@example.com"),
        ])

        # --- READ: чтение данных ---
        print("\n--- READ: все пользователи ---")
        for user in db.get_all_users():
            print(f"  {user}")

        print(f"\n--- READ: поиск по ID {id1} ---")
        print(f"  {db.get_user_by_id(id1)}")

        print("\n--- READ: поиск по email ---")
        print(f"  {db.get_user_by_email('bob@example.com')}")

        print("\n--- READ: поиск по имени 'ал' ---")
        for user in db.search_users_by_name("ал"):
            print(f"  {user}")

        # --- UPDATE: обновление данных ---
        print("\n--- UPDATE: обновление пользователя ---")
        db.update_user(id1, name="Алиса Петрова", email="alice.petrova@example.com")
        print(f"  После обновления: {db.get_user_by_id(id1)}")

        # --- DELETE: удаление данных ---
        print("\n--- DELETE: удаление пользователя ---")
        db.delete_user(id3)

        # ==================== УТИЛИТАРНЫЕ МЕТОДЫ ====================
        print("\n" + "=" * 50)
        print("УТИЛИТАРНЫЕ МЕТОДЫ")
        print("=" * 50)

        print(f"\n--- Количество пользователей: {db.count_users()} ---")

        print("\n--- Поиск пользователей по шаблону 'д' ---")
        for user in db.search_users_by_name("д"):
            print(f"  {user}")

        # ==================== ТРАНЗАКЦИИ ====================
        print("\n" + "=" * 50)
        print("ТРАНЗАКЦИИ")
        print("=" * 50)

        print("\n--- Демонстрация транзакции: добавление + откат ---")
        count_before = db.count_users()
        db.cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            ("Временный", "temp@example.com")
        )
        print(f"  До отката: {db.count_users()} пользователей")
        db.conn.rollback()
        print(f"  После отката: {db.count_users()} пользователей (запись откачена)")

        print("\n--- Демонстрация транзакции: добавление + коммит ---")
        db.cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            ("Финальный", "final@example.com")
        )
        db.commit()
        print(f"  После коммита: {db.count_users()} пользователей (запись сохранена)")

        # ==================== ИТОГОВЫЙ СПИСОК ====================
        print("\n" + "=" * 50)
        print("ИТОГОВЫЙ СПИСОК")
        print("=" * 50)

        for user in db.get_all_users():
            print(f"  {user}")

        # ==================== ОЧИСТКА ====================
        # Раскомментируйте строку ниже, чтобы удалить всех пользователей
        # db.delete_all_users()
