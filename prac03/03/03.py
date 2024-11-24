import xml.etree.ElementTree as ET
import statistics
import json
import glob


def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    name = root.find("name").text.strip()
    constellation = root.find("constellation").text.strip()
    spectral_class = root.find("spectral-class").text.strip()
    radius = int(root.find("radius").text.strip())
    rotation = float(root.find("rotation").text.strip().split()[0])
    age = float(root.find("age").text.strip().split()[0])
    distance = float(root.find("distance").text.strip().split()[0])
    absolute_magnitude = float(root.find("absolute-magnitude").text.strip().split()[0])

    return {
        "name": name,
        "constellation": constellation,
        "spectral-class": spectral_class,
        "radius": radius,
        "rotation": rotation,
        "age": age,
        "distance": distance,
        "absolute-magnitude": absolute_magnitude,
    }


stars_data = []
for file_path in glob.glob("03/3/*xml"):
    star_data = parse_xml(file_path)
    stars_data.append(star_data)

with open("03/stars_data.json", "w", encoding="utf-8") as f:
    json.dump(stars_data, f, ensure_ascii=False, indent=4)


# 1. Сортировка по age
sorted_stars = sorted(stars_data, key=lambda x: x["age"])
with open("03/sorted_stars.json", "w", encoding="utf-8") as f:
    json.dump(sorted_stars, f, ensure_ascii=False, indent=4)


# 2. Фильтрация по созвездию
filtered_stars = [s for s in stars_data if s["constellation"] == "Близнецы"]
with open("03/filtered_stars.json", "w", encoding="utf-8") as f:
    json.dump(filtered_stars, f, ensure_ascii=False, indent=4)


# 3. Max/min/avg по radius
radius_list = [s["radius"] for s in stars_data]
radius_stats = {
    "sum": sum(radius_list),
    "min": min(radius_list),
    "max": max(radius_list),
    "average": statistics.mean(radius_list),
    "median": statistics.median(radius_list),
    "stdev": statistics.stdev(radius_list),
}
with open("03/radius_stats.json", "w", encoding="utf-8") as f:
    json.dump(radius_stats, f, ensure_ascii=False, indent=4)


# 4. Частота меток для spectral-class
spectral_frequency = {}
for star in stars_data:
    spectral_class = star["spectral-class"]
    spectral_frequency[spectral_class] = spectral_frequency.get(spectral_class, 0) + 1

with open("03/spectral_frequency.json", "w", encoding="utf-8") as f:
    json.dump(spectral_frequency, f, ensure_ascii=False, indent=4)
