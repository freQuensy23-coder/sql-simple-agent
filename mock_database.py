import sqlite3
from faker import Faker
import random

# Инициализация Faker
fake = Faker()

# Создание подключения к SQLite
conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

# Создание таблиц
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    address TEXT
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    position TEXT,
    salary REAL,
    hire_date TEXT
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL,
    stock INTEGER
);
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);
"""
)


# Функции для вставки данных
def populate_users(count=500):
    users = [
        (fake.name(), fake.email(), fake.phone_number(), fake.address())
        for _ in range(count)
    ]
    cursor.executemany(
        "INSERT INTO users (name, email, phone, address) VALUES (?, ?, ?, ?);", users
    )


def populate_employees(count=200):
    employees = [
        (
            fake.name(),
            fake.job(),
            round(random.uniform(30000, 120000), 2),
            fake.date_this_decade(),
        )
        for _ in range(count)
    ]
    cursor.executemany(
        "INSERT INTO employees (name, position, salary, hire_date) VALUES (?, ?, ?, ?);",
        employees,
    )


def populate_products(count=500):
    products = [
        (
            fake.word().capitalize(),
            round(random.uniform(5, 500), 2),
            random.randint(0, 1000),
        )
        for _ in range(count)
    ]
    cursor.executemany(
        "INSERT INTO products (name, price, stock) VALUES (?, ?, ?);", products
    )


def populate_orders(count=1000):
    user_ids = [row[0] for row in cursor.execute("SELECT id FROM users").fetchall()]
    product_ids = [
        row[0] for row in cursor.execute("SELECT id FROM products").fetchall()
    ]
    orders = [
        (
            random.choice(user_ids),
            random.choice(product_ids),
            random.randint(1, 10),
            fake.date_this_year(),
        )
        for _ in range(count)
    ]
    cursor.executemany(
        "INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?);",
        orders,
    )


# Наполнение данными
populate_users(500)
populate_employees(200)
populate_products(500)
populate_orders(1000)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("База данных создана и заполнена данными.")
