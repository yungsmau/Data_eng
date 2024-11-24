from bs4 import BeautifulSoup
import json
import glob
import statistics


def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    products = []

    for product_div in soup.find_all("div", class_="pad"):
        id = int(product_div.find("a", class_="add-to-favorite")["data-id"].strip())

        url = product_div.find_all("a")[1]["href"].strip()

        img = product_div.find("img")["src"].strip()

        name = product_div.find("span").string.strip()

        price = int(
            product_div.find("price").string.replace("₽", "").replace(" ", "").strip()
        )

        bonus = int(product_div.find("strong").string.split()[-2].strip())

        characteristics = {}
        for li in product_div.find_all("li"):
            chat_type = li.get("type")
            chat_value = li.string.strip()
            characteristics[chat_type] = chat_value

        products.append(
            {
                "id": id,
                "url": url,
                "img": img,
                "name": name,
                "price": price,
                "bonus": bonus,
                "characteristics": characteristics,
            }
        )

    return products


all_products = []
for file_path in glob.glob("02/2/*html"):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
        products = parse_html(html_content)
        all_products.extend(products)

with open("02/products_data.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=4)


# Анализ
# 1. Сортировка по price
sorted_products = sorted(all_products, key=lambda x: x["price"])
with open("02/sorted_products.json", "w", encoding="utf-8") as f:
    json.dump(sorted_products, f, ensure_ascii=False, indent=4)


# 2. Фильтрация по sim >= 3
filtered_products = [
    p
    for p in all_products
    if "sim" in p["characteristics"]
    and int(p["characteristics"]["sim"].split()[0]) >= 3
]
with open("02/filtered_products.json", "w", encoding="utf-8") as f:
    json.dump(filtered_products, f, ensure_ascii=False, indent=4)


# 3. Min/max/avg по price
prices = [p["price"] for p in all_products]
price_stats = {
    "sum": sum(prices),
    "min": min(prices),
    "max": max(prices),
    "average": statistics.mean(prices),
    "median": statistics.median(prices),
    "stdev": statistics.stdev(prices),
}

with open("02/price_stats.json", "w", encoding="utf-8") as f:
    json.dump(price_stats, f, ensure_ascii=False, indent=4)


# 4. Частота по ram
ram_frequency = {}
filtered_ram = [p for p in all_products if "ram" in p["characteristics"]]
for product in filtered_ram:
    ram = product["characteristics"]["ram"]
    ram_frequency[ram] = ram_frequency.get(ram, 0) + 1

with open("02/ram_frequency.json", "w", encoding="utf-8") as f:
    json.dump(ram_frequency, f, ensure_ascii=False, indent=4)
