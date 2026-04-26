import json
import csv
from connect import get_connection

def show_menu():
    print("\n" + "="*40)
    print("📱 PHONEBOOK")
    print("="*40)
    print("1. Search contacts")
    print("2. Filter by group")
    print("3. Sort contacts")
    print("4. Export JSON")
    print("5. Import JSON")
    print("6. Import CSV")
    print("7. Pagination")
    print("8. Add contact")
    print("0. Exit")
    print("="*40)

#  Поиск
def search_contacts(query):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()

    print_contacts(rows)

    conn.close()


# Фильтр по группе
def filter_by_group(group):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))

    for row in cur.fetchall():
        print(row)

    conn.close()


# Сортировка
def sort_contacts(option):
    conn = get_connection()
    cur = conn.cursor()

    if option == "name":
        cur.execute("SELECT * FROM contacts ORDER BY name")
    elif option == "birthday":
        cur.execute("SELECT * FROM contacts ORDER BY birthday")
    elif option == "date":
        cur.execute("SELECT * FROM contacts ORDER BY created_at")

    for row in cur.fetchall():
        print(row)

    conn.close()


# Экспорт в JSON
def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
    """)

    data = cur.fetchall()

    with open("contacts.json", "w") as f:
        json.dump(data, f, default=str)

    conn.close()


# Импорт из JSON
def import_json():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.json") as f:
        data = json.load(f)

    for name, email, birthday, group, phone in data:
        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists. skip/overwrite: ")
            if choice == "skip":
                continue
            else:
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        cur.execute("""
            INSERT INTO contacts(name, email, birthday)
            VALUES (%s, %s, %s)
        """, (name, email, birthday))

    conn.commit()
    conn.close()


# Пагинация
def paginate():
    conn = get_connection()
    cur = conn.cursor()

    page = 0
    limit = 5

    while True:
        cur.execute(
            "SELECT * FROM contacts LIMIT %s OFFSET %s",
            (limit, page * limit)
        )

        rows = cur.fetchall()
        if not rows:
            print("No more data")
            break

        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            page += 1
        elif cmd == "prev" and page > 0:
            page -= 1
        else:
            break

    conn.close()

def import_csv():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.csv", newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"]
            email = row["email"]
            birthday = row["birthday"]
            group = row["group"]
            phone = row["phone"]
            phone_type = row["type"]

            cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
            exists = cur.fetchone()

            if exists:
                choice = input(f"{name} exists. skip/overwrite: ")

                if choice == "skip":
                    continue
                else:
                    cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

            cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
            gid = cur.fetchone()

            if gid is None:
                cur.execute(
                    "INSERT INTO groups(name) VALUES (%s) RETURNING id",
                    (group,)
                )
                gid = cur.fetchone()[0]
            else:
                gid = gid[0]

            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (name, email, birthday, gid))

            contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, phone, phone_type))

    conn.commit()
    conn.close()

    print("CSV import completed ")

def add_contact():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")
    phone = input("Phone: ")
    phone_type = input("Phone type (mobile/home/work): ")

    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    gid = cur.fetchone()

    if gid is None:
        cur.execute(
            "INSERT INTO groups(name) VALUES (%s) RETURNING id",
            (group,)
        )
        gid = cur.fetchone()[0]
    else:
        gid = gid[0]

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (name, email, birthday, gid))

    contact_id = cur.fetchone()[0]
  
    cur.execute("""
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
    """, (contact_id, phone, phone_type))

    conn.commit()
    conn.close()

    print("✅ Contact added")

def print_contacts(rows):
    print("\n" + "-"*60)
    print(f"{'Name':<20} {'Email':<25} {'Phone':<15}")
    print("-"*60)

    for r in rows:
        name = str(r[0])
        email = str(r[1])
        phone = str(r[2]) if len(r) > 2 else ""

        print(f"{name:<20} {email:<25} {phone:<15}")

    print("-"*60)

def main():
    while True:
        show_menu()
        choice = input("Choose option: ")

        if choice == "1":
            query = input("Search: ")
            search_contacts(query)

        elif choice == "2":
            group = input("Group: ")
            filter_by_group(group)

        elif choice == "3":
            option = input("Sort by (name/birthday/date): ")
            sort_contacts(option)

        elif choice == "4":
            export_json()
            print("Export done")

        elif choice == "5":
            import_json()
            print("Import done")

        elif choice == "6":
            import_csv()
            print("CSV imported")

        elif choice == "7":
            paginate()

        elif choice == "8":
            add_contact()

        elif choice == "0":
            print("Bye!")
            break

        else:
            print("Invalid option")




if __name__ == "__main__":
    main()