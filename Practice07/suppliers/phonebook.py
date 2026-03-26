import psycopg2
import csv
from config import load_config

def execute_query(sql, params=None, fetch=False):
    
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                if fetch:
                    return cur.fetchall()
                conn.commit()
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
 
def insert_from_console():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    sql = """
INSERT INTO phonebook (first_name, phone_number) 
VALUES (%s, %s) 
ON CONFLICT (phone_number) DO NOTHING;
"""
    execute_query(sql, (name, phone))
    print("Контакт добавлен!")


def upload_from_csv(file_name):
    sql = "INSERT INTO phonebook(first_name, phone_number) VALUES(%s, %s)"
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  
            for row in reader:
                execute_query(sql, row)
        print(f"Данные из {file_name} загружены.")
    except FileNotFoundError:
        print("Файл CSV не найден.")


def update_contact(user_id, new_name=None, new_phone=None):
    if new_name:
        execute_query("UPDATE phonebook SET first_name = %s WHERE user_id = %s", (new_name, user_id))
    if new_phone:
        execute_query("UPDATE phonebook SET phone_number = %s WHERE user_id = %s", (new_phone, user_id))
    print("Данные обновлены.")


def search_contacts(name_filter=""):
    sql = "SELECT * FROM phonebook WHERE first_name ILIKE %s"
    results = execute_query(sql, (f'%{name_filter}%',), fetch=True)
    
  
    if results:
        for row in results:
            print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")
    else:
        print("Контакты не найдены или произошла ошибка.")


def delete_contact(target):
    sql = "DELETE FROM phonebook WHERE first_name = %s OR phone_number = %s"
    execute_query(sql, (target, target))
    print(f"Контакт '{target}' удален (если он существовал).")


if __name__ == '__main__':
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Добавить контакт (консоль)")
        print("2. Загрузить из CSV")
        print("3. Обновить контакт")
        print("4. Поиск / Показать всех")
        print("5. Удалить контакт")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            insert_from_console()
        elif choice == '2':
            upload_from_csv('data.csv')
        elif choice == '3':
            uid = input("Введите ID контакта для изменения: ")
            nn = input("Новое имя (пусто - оставить прежним): ")
            np = input("Новый телефон (пусто - оставить прежним): ")
            update_contact(uid, nn or None, np or None)
        elif choice == '4':
            filt = input("Введите имя для поиска (пусто - все): ")
            search_contacts(filt)
        elif choice == '5':
            target = input("Введите имя или номер для удаления: ")
            delete_contact(target)
        elif choice == '0':
            break