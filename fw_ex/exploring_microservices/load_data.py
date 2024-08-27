import requests
import sqlite3


# Create and configure SQLite databases
def create_and_configure_db():
    # Create products database and table
    conn = sqlite3.connect("./data/products.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    print("Completed creating the product table")
    conn.commit()
    conn.close()

    # Create orders database and table
    conn = sqlite3.connect("./data/orders.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES Product(id)
        )
    """)
    print("Completed creating the product table")
    conn.commit()
    conn.close()


def load_data():
    # Paths to the SQLite databases
    PRODUCT_DB_PATH = "./data/products.db"
    ORDER_DB_PATH = "./data/orders.db"

    # Dummy data for products
    products = [
        {"name": "Laptop", "price": 999.99},
        {"name": "Smartphone", "price": 499.99},
        {"name": "Tablet", "price": 299.99},
        {"name": "Headphones", "price": 79.99},
        {"name": "Monitor", "price": 199.99},
    ]

    # Load product data into the products.db SQLite database
    print("Loading product data...")
    conn = sqlite3.connect(PRODUCT_DB_PATH)
    c = conn.cursor()
    for product in products:
        c.execute(
            """
            INSERT INTO Product (name, price) VALUES (?, ?)
        """,
            (product["name"], product["price"]),
        )
    conn.commit()

    # Fetch and print all products to confirm
    c.execute("SELECT * FROM Product")
    all_products = c.fetchall()
    print("Get Products Response:", all_products)
    conn.close()

    # Dummy data for orders
    orders = [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 1},
        {"product_id": 3, "quantity": 3},
        {"product_id": 4, "quantity": 5},
        {"product_id": 5, "quantity": 4},
    ]

    # Load order data into the orders.db SQLite database
    print("Loading order data...")
    conn = sqlite3.connect(ORDER_DB_PATH)
    c = conn.cursor()
    for order in orders:
        c.execute(
            """
            INSERT INTO Orders (product_id, quantity) VALUES (?, ?)
        """,
            (order["product_id"], order["quantity"]),
        )
    conn.commit()

    # Fetch and print all orders to confirm
    c.execute("SELECT * FROM Orders")
    all_orders = c.fetchall()
    print("Get Orders Response:", all_orders)
    conn.close()


if __name__ == "__main__":
    create_and_configure_db()
    load_data()
