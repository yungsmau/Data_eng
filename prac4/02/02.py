import sqlite3
import pandas as pd
import msgpack


conn = sqlite3.connect("01/items.db")
cursor = conn.cursor()

prizes_table_query = f"""
CREATE TABLE IF NOT EXISTS prizes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    place INTEGER,
    prize INTEGER,
    FOREIGN KEY (name) REFERENCES tournaments (name)
);
"""

cursor.execute(prizes_table_query)

with open("02/subitem.msgpack", "rb") as f:
    prizes_data = msgpack.unpack(f, raw=False)

insert_query = """
INSERT INTO prizes (name, place, prize)
    VALUES (?, ?, ?);
"""

for item in prizes_data:
    cursor.execute(insert_query, (item["name"], item["place"], item["prise"]))

conn.commit()

# 1. Получение турниров с доп. информацией
query_1 = """
SELECT tournaments.name, tournaments.city, prizes.place, prizes.prize
FROM tournaments
JOIN prizes ON tournaments.name = prizes.name;
"""

tour_with_pr = pd.read_sql_query(query_1, conn)
tour_with_pr.to_csv("02/tournaments_with_prizes.csv", index=False, encoding="utf-8")
print("Результаты первого запроса сохранены в 'tournaments_with_prizes.csv'")

# 2. Суммарный приз для каждого города
query_2 = """
SELECT tournaments.city, SUM(prizes.prize) as total_prize
FROM tournaments
JOIN prizes ON tournaments.name = prizes.name
GROUP BY tournaments.city;
"""

sum_by_city = pd.read_sql_query(query_2, conn)
sum_by_city.to_json(
    "02/city_prizes.json", orient="records", force_ascii=False, indent=4
)
print("Результаты второго запроса сохранены в 'city_prizes.json'")

# 3. Турниры с призовым фондом больше 1 миллиона
query_3 = """
SELECT tournaments.name, tournaments.city, prizes.place, prizes.prize
FROM tournaments
JOIN prizes ON tournaments.name = prizes.name
WHERE prizes.prize > 1000000
ORDER BY prizes.prize DESC; 
"""

total_prize = pd.read_sql_query(query_3, conn)
total_prize.to_json(
    "02/high_prize_tournaments.json", orient="records", force_ascii=False, indent=4
)
print("Результаты третьего запроса сохранены в 'high_prize_tournaments.json'.")
