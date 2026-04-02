import psycopg2
import csv
from config import load_config

def execute_query(sql, params=None, fetch=False, is_procedure=False):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                if fetch:
                    return cur.fetchall()
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")

#1
def insert_or_update_from_console():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    sql = "CALL upsert_contact(%s, %s)"
    execute_query(sql, (name, phone))
    print(f"Контакт {name} обработан (добавлен или обновлен).")

#2
def search_contacts_advanced(pattern=""):
    sql = "SELECT * FROM find_contacts(%s)"
    results = execute_query(sql, (pattern,), fetch=True)
    
    if results:
        for row in results:
            print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")
    else:
        print("Ничего не найдено.")

#3
def show_paged_contacts():
    limit = input("Сколько контактов вывести на странице? ")
    offset = input("Сколько контактов пропустить? ")
    sql = "SELECT * FROM get_phonebook_paged(%s::int, %s::int)"
    results = execute_query(sql, (int(limit), int(offset)), fetch=True)
    
    if results:
        for row in results:
            print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")

#4
def upload_from_csv_bulk(file_name):
    names = []
    phones = []
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                names.append(row[0])
                phones.append(row[1])
        
        sql = "SELECT * FROM bulk_insert_contacts(%s, %s)"
        rejected = execute_query(sql, (names, phones), fetch=True)
        
        print(f"Загрузка завершена.")
        if rejected:
            print("Некоторые контакты были отклонены (неверный формат):")
            for r in rejected:
                print(f"Имя: {r[0]}, Тел: {r[1]}")
                
    except FileNotFoundError:
        print("Файл CSV не найден.")
  #5      
def delete_contact_advanced():
    target = input("Введите имя или номер для удаления: ")
    sql = "CALL delete_contact_by_name_or_phone(%s)"
    execute_query(sql, (target,))
    print(f"Запрос на удаление '{target}' выполнен.")

if __name__ == '__main__':
    while True:
        print("\n--- PhoneBook Menu ")
        print("1. Добавить/Обновить контакт")
        print("2. Загрузить из CSV")
        print("3. Поиск по шаблону")
        print("4. Просмотр по страницам")
        print("5. Удалить контакт")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            insert_or_update_from_console()
        elif choice == '2':
            upload_from_csv_bulk('data.csv')
        elif choice == '3':
            filt = input("Введите часть имени или телефона для поиска: ")
            search_contacts_advanced(filt)
        elif choice == '4':
            show_paged_contacts() 
        elif choice == '5':
            delete_contact_advanced()
        elif choice == '0':
            break