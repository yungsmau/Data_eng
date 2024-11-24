from bs4 import BeautifulSoup
import json
import statistics
import glob


# С условием, что в html есть все нужные данные
def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    city = (
        soup.find("span", string=lambda t: t and "Город" in t)
        .string.split(":")[-1]
        .strip()
    )

    title = (
        soup.find(
            "h1",
            class_="title",
        )
        .string.split(":")[-1]
        .strip()
    )

    build_id = int(soup.find("h1", class_="title")["id"])

    address = (
        soup.find("p", class_="address-p")
        .string.split("Индекс:")[0]
        .split("Улица:")[-1]
        .strip()
    )

    postal_code = int(
        soup.find("p", class_="address-p").string.split("Индекс:")[-1].strip()
    )

    floors = int(soup.find("span", class_="floors").string.split(":")[-1].strip())

    year = int(soup.find("span", class_="year").string.split()[-1].strip())

    parking = (
        soup.find("span", string=lambda t: t and "Парковка:" in t)
        .string.split(":")[-1]
        .strip()
    )
    # parking_in_01 = (
    #     1
    #     if soup.find("span", string=lambda t: t and "Парковка:" in t)
    #     .string.split(":")[-1]
    #     .strip()
    #     == "есть"
    #     else 0
    # )

    rating = float(
        soup.find("span", string=lambda t: t and "Рейтинг:" in t)
        .string.split(":")[-1]
        .strip()
    )

    views = int(
        soup.find("span", string=lambda t: t and "Просмотры:" in t)
        .string.split(":")[-1]
        .strip()
    )

    img_url = soup.find("img")["src"]

    return {
        "city": city,
        "title": title,
        "id": build_id,
        "address": address,
        "postal_code": postal_code,
        "floors": floors,
        "year": year,
        "parking": parking,
        "rating": rating,
        "views": views,
        "img_url": img_url,
    }


buildings = []
for file_path in glob.glob("01/1/*html"):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
        building_data = parse_html(html_content)
        buildings.append(building_data)

with open("01/buildings_data.json", "w", encoding="utf-8") as f:
    json.dump(buildings, f, ensure_ascii=False, indent=4)


# Анализ
# 1. Сортировка по году
sorted_by_year = sorted(buildings, key=lambda x: x["year"])
with open("01/sorted_by_year.json", "w", encoding="utf-8") as f:
    json.dump(sorted_by_year, f, ensure_ascii=False, indent=4)


# 2. Фильтрация по паркингу
filtered_by_parking = [b for b in buildings if b["parking"] == "есть"]
with open("01/filtered_by_parking.json", "w", encoding="utf-8") as f:
    json.dump(filtered_by_parking, f, ensure_ascii=False, indent=4)


# 3. Min/max/avg по views
views_list = [b["views"] for b in buildings]
views_stat = {
    "sum": sum(views_list),
    "min": min(views_list),
    "max": max(views_list),
    "average": statistics.mean(views_list),
    "median": statistics.median(views_list),
    "stdev": statistics.stdev(views_list),
}
with open("01/views_stat.json", "w", encoding="utf-8") as f:
    json.dump(views_stat, f, ensure_ascii=False, indent=4)


# 4. Частота меток по city
city_frequency = {}
for building in buildings:
    city = building["city"]
    city_frequency[city] = city_frequency.get(city, 0) + 1

with open("01/city_frequency.json", "w", encoding="utf-8") as f:
    json.dump(city_frequency, f, ensure_ascii=False, indent=4)
