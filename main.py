import sqlite3

DB_PATH = r"d:\vscode projects\logika_sql_education\lesson1\m3l3\shop.db"

def connect():
    return sqlite3.connect(DB_PATH)

def total_sales(cursor):
    cursor.execute("""
        SELECT SUM(p.price * o.quantity) AS total_sales
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
    """)
    total = cursor.fetchone()[0]
    print(f"🔸 Загальний обсяг продажів: {round(total, 2)} грн")

def customer_order_counts(cursor):
    cursor.execute("""
        SELECT c.first_name, c.last_name, COUNT(o.order_id) AS order_count
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id
    """)
    print("🔹 Кількість замовлень по клієнтам:")
    for row in cursor.fetchall():
        print(f"- {row[0]} {row[1]}: {row[2]} замовлень")

def avg_order_amount(cursor):
    cursor.execute("""
        SELECT AVG(p.price * o.quantity) AS avg_order_amount
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
    """)
    avg = cursor.fetchone()[0]
    print(f"🔸 Середній чек замовлення: {round(avg, 2)} грн")

def most_popular_category(cursor):
    cursor.execute("""
        SELECT p.category, COUNT(*) AS order_count
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        GROUP BY p.category
        ORDER BY order_count DESC
        LIMIT 1
    """)
    result = cursor.fetchone()
    print(f"🔸 Найпопулярніша категорія: {result[0]} (замовлень: {result[1]})")

def product_count_per_category(cursor):
    cursor.execute("""
        SELECT category, COUNT(*) AS products_count
        FROM products
        GROUP BY category
    """)
    print("🔹 Кількість товарів по категоріях:")
    for row in cursor.fetchall():
        print(f"- {row[0]}: {row[1]} товарів")

def increase_phone_prices(cursor):
    cursor.execute("""
        UPDATE products
        SET price = price * 1.10
        WHERE category = 'Phones'
    """)
    print("✅ Ціни в категорії 'Phones' збільшено на 10%.")

def main():
    conn = connect()
    cursor = conn.cursor()

    while True:
        print("\n📦 Меню:")
        print("1. Загальний обсяг продажів")
        print("2. Кількість замовлень по клієнтах")
        print("3. Середній чек замовлення")
        print("4. Найпопулярніша категорія")
        print("5. Кількість товарів по категоріях")
        print("6. Збільшити ціни в категорії 'Phones' на 10%")
        print("7. Вийти")

        choice = input("Ваш вибір (1-7): ")

        if choice == "1":
            total_sales(cursor)
        elif choice == "2":
            customer_order_counts(cursor)
        elif choice == "3":
            avg_order_amount(cursor)
        elif choice == "4":
            most_popular_category(cursor)
        elif choice == "5":
            product_count_per_category(cursor)
        elif choice == "6":
            increase_phone_prices(cursor)
        elif choice == "7":
            save = input("Зберегти зміни? (y/n): ").lower()
            if save == "y":
                conn.commit()
                print("✅ Зміни збережено.")
            else:
                conn.rollback()
                print("❌ Зміни скасовано.")
            break
        else:
            print("❌ Невірна опція. Спробуйте ще раз.")

    conn.close()

if __name__ == "__main__":
    main()
