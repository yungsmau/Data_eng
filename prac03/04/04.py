import xml.etree.ElementTree as ET
import json
import glob
import statistics


def parse_xml(file_path):
    """
    Все уникальные теги:
    clothing-items
    clothing
    id
    name
    category
    size
    color
    material
    price
    rating
    reviews
    new
    exclusive
    sporty
    """

    tree = ET.parse(file_path)
    root = tree.getroot()

    clothing_items = []
    for item in root.findall("clothing"):
        clothing_data = {
            "id": int(item.findtext("id", default="").strip()),
            "name": item.findtext("name", default="").strip(),
            "category": item.findtext("category", default="").strip(),
            "size": item.findtext("size", default="").strip(),
            "color": item.findtext("color", default="").strip(),
            "material": item.findtext("material", default="").strip(),
            "price": int(item.findtext("price", default="0").strip()),
            "rating": float(item.findtext("rating", default="0").strip()),
            "reviews": int(item.findtext("reviews", default="0").strip()),
            "new": item.findtext("new", default="").strip(),
            "exclusive": item.findtext("exclusive", default="").strip(),
            "sporty": item.findtext("sporty", default="").strip(),
        }

        clothing_items.append(clothing_data)

    return clothing_items


all_clothing_data = []
for file_path in glob.glob("04/4/*xml"):
    clothing_data = parse_xml(file_path)
    all_clothing_data.extend(clothing_data)

with open("04/clothing_data.json", "w", encoding="utf-8") as f:
    json.dump(all_clothing_data, f, ensure_ascii=False, indent=4)


# 1. Сортировка по price
sorted_clothing = sorted(all_clothing_data, key=lambda x: x["price"])
with open("04/sorted_clothing.json", "w", encoding="utf-8") as f:
    json.dump(sorted_clothing, f, ensure_ascii=False, indent=4)


# 2. Фильтрация по цвету фиолетовый
filtered_clothing = [
    item for item in all_clothing_data if item["color"] == "Фиолетовый"
]
with open("04/filtered_clothing.json", "w", encoding="utf-8") as f:
    json.dump(filtered_clothing, f, ensure_ascii=False, indent=4)


# 3. Min/max/avg по reviews
reviews_list = [item["reviews"] for item in all_clothing_data]
reviews_stat = {
    "sum": sum(reviews_list),
    "min": min(reviews_list),
    "max": max(reviews_list),
    "average": statistics.mean(reviews_list),
    "median": statistics.median(reviews_list),
    "stdev": statistics.stdev(reviews_list),
}

with open("04/reviews_stat.json", "w", encoding="utf-8") as f:
    json.dump(reviews_stat, f, ensure_ascii=False, indent=4)


# 4. Частота меток по категории
category_frequency = {}
for item in all_clothing_data:
    category = item["category"]
    category_frequency[category] = category_frequency.get(category, 0) + 1

with open("04/category_freq.json", "w", encoding="utf-8") as f:
    json.dump(category_frequency, f, ensure_ascii=False, indent=4)
