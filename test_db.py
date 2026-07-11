from db import Database

with Database() as db:
    db.create_table()

    id1 = db.insert_user("Алиса", "alice@example.com")
    id2 = db.insert_user("Боб", "bob@example.com")

    print("\nВсе пользователи:")
    for user in db.get_all_users():
        print(f"  {user}")

    print(f"\nПо ID {id1}: {db.get_user_by_id(id1)}")
    print(f"По email: {db.get_user_by_email('bob@example.com')}")
    print(f"Поиск 'али': {db.search_users_by_name('али')}")
    print(f"Всего: {db.count_users()}")

    db.update_user(id1, name="Алиса Иванова")

    print("\nПосле обновления:")
    print(db.get_user_by_id(id1))

    db.delete_user(id2)

    print("\nИтого:")
    for user in db.get_all_users():
        print(f"  {user}")
