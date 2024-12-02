import sqlite3
import pandas as pd
import json
import re
import logging


logging.basicConfig(
    filename="04/error_log.txt",
    level=logging.WARNING,
    format="%(levelname)s - %(message)s",
    filemode="w",
)

conn = sqlite3.connect("04/products.db")
cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    price REAL CHECK (price >= 0),
    quantity INTEGER CHECK (quantity >= 0),
    category TEXT,
    fromCity TEXT,
    isAvailable BOOLEAN,
    views INTEGER CHECK (views >= 0),
    update_count INTEGER DEFAULT 0
);
"""

cursor.execute(create_table_query)

product_data = pd.read_pickle("04/_product_data.pkl")
product_data = pd.DataFrame(product_data)
product_data["update_count"] = 0

for index, row in product_data.iterrows():
    cursor.execute(
        """
        INSERT OR REPLACE INTO products (name, price, quantity, category, fromCity, isAvailable, views, update_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """,
        (
            row["name"],
            row["price"],
            row["quantity"],
            row["category"],
            row["fromCity"],
            row["isAvailable"],
            row["views"],
            row["update_count"],
        ),
    )


# Чтение обновлений из файла
with open("04/_update_data.text", "r", encoding="utf-8") as f:
    update_lines = f.read().strip().split("=====")

updates = []
for block in update_lines:
    block = block.strip()
    name = re.search(r"name::(.+)", block)
    method = re.search(r"method::(.+)", block)
    param = re.search(r"param::(.+)", block)

    if name and method:
        updates.append(
            {
                "name": name.group(1).strip(),
                "method": method.group(1).strip(),
                "param": param.group(1).strip() if param else None,
            }
        )


for update in updates:
    name = update["name"]
    method = update["method"]
    param = update["param"]

    try:
        # Проверка на существование товара
        cursor.execute("SELECT * FROM products WHERE name = ?", (name,))
        product = cursor.fetchone()
        if not product:
            logging.warning(f"Товар '{name}' не найден, пропускаем")
            continue

        # Обработка обновлений
        if method == "price_abs":
            if param is not None:
                param = float(param)
                if param >= 0:
                    cursor.execute(
                        """
                        UPDATE products
                        SET price = ?,
                            update_count = update_count + 1
                        WHERE name = ?;
                        """,
                        (param, name),
                    )
        elif method == "price_percent":
            if param is not None:
                param = float(param)
                cursor.execute(
                    """
                    UPDATE products
                    SET price = price * (1 + ?),
                        update_count = update_count + 1
                    WHERE name = ? and price * (1 + ?) >= 0;
                    """,
                    (param, name, param),
                )
        elif method == "quantity_add":
            if param is not None:
                param = int(param)
                cursor.execute(
                    """
                    UPDATE products
                    SET quantity = quantity + ?,
                        update_count = update_count + 1
                    WHERE name = ? AND quantity + ? >= 0;
                    """,
                    (param, name, param),
                )
        elif method == "quantity_sub":
            if param is not None:
                param = int(param)
                cursor.execute(
                    """
                    UPDATE products
                    SET quantity = quantity - ?,
                        update_count = update_count + 1
                    WHERE name = ? AND quantity - ? >= 0;
                    """,
                    (param, name, param),
                )
        elif method == "available":
            if param is not None:
                param = param.strip().lower() == "true"
                cursor.execute(
                    """
                    UPDATE products
                    SET isAvailable = ?,
                        update_count = update_count + 1
                    WHERE name = ?;
                    """,
                    (param, name),
                )
        elif method == "remove":
            cursor.execute(
                """
                DELETE FROM products
                WHERE name = ?;
                """,
                (name,),
            )

    except Exception as e:
        logging.error(f"Ошибка при обновлении '{name}': {e}")
        conn.rollback()
        continue

conn.commit()

# 1. 10 самых обновлеямых товаров
query_top_updates = """
SELECT name, update_count
FROM products
ORDER BY update_count DESC
LIMIT 10;
"""

top_updates = pd.read_sql_query(query_top_updates, conn)
top_updates.to_json(
    "04/top_updates.json", orient="records", force_ascii=False, indent=4
)
print("Первый запрос сохранен в 'top_updates.json'")


# 2. Анализ цен товаров
query_price_analysis = """
SELECT 
    category,
    SUM(price) AS total_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price,
    AVG(price) AS avg_price,
    COUNT(*) AS product_count
FROM products
GROUP BY category;
"""

price_analysis = pd.read_sql_query(query_price_analysis, conn)
price_analysis.to_json(
    "04/price_analysis.json", orient="records", force_ascii=False, indent=4
)
print("Второй запрос сохранен в 'price_analysis.json'")


# 3. Анализ остатка товаров
query_quantity_analysis = """
SELECT 
    category,
    SUM(quantity) AS total_quantity,
    MIN(quantity) AS min_quantity,
    MAX(quantity) AS max_quantity,
    AVG(quantity) AS avg_quantity,
    COUNT(*) AS product_count
FROM products
GROUP BY category;
"""

quantity_analysis = pd.read_sql_query(query_quantity_analysis, conn)
quantity_analysis.to_json(
    "04/quantity_analysis.json", orient="records", force_ascii=False, indent=4
)
print("Третий запрос сохранен в 'quantity_analysis.json'")


# 4. quantity > 1000, isAv = True
query_custom = """
SELECT name, category, quantity, price, isAvailable
FROM products
WHERE quantity > 1000 AND isAvailable = 1
ORDER BY quantity DESC;
"""

custom_query = pd.read_sql_query(query_custom, conn)
custom_query.to_json(
    "04/custom_query.json", orient="records", force_ascii=False, indent=4
)
print("Четвертый запрос сохранен в 'custom_query.json'")

conn.close()
