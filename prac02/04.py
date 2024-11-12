import json
import pandas as pd

products_df = pd.read_pickle("85/fourth_task_products.json")
products_df = pd.DataFrame(products_df)
products_df["price"] = products_df["price"].astype(float)

with open("85/fourth_task_updates.json", "r", encoding="utf-8") as f:
    price_updates = json.load(f)

for update in price_updates:
    name = update["name"]
    method = update["method"]
    param = update["param"]

    if name in products_df["name"].values:
        if method == "add":
            products_df.loc[products_df["name"] == name, "price"] += param
        elif method == "sub":
            products_df.loc[products_df["name"] == name, "price"] -= param
        elif method == "percent+":
            products_df.loc[products_df["name"] == name, "price"] *= 1 + param
        elif method == "percent-":
            products_df.loc[products_df["name"] == name, "price"] *= 1 - param


products_df.to_pickle("answers/modified_products_04.pkl")

print("Данные успешно обновлены и сохранены в 'modified_products.pkl'.")
