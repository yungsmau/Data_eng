import sqlite3
import json
import statistics


conn = sqlite3.connect("01/items.db")
cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS tournaments (
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    begin TEXT,
    system TEXT,
    tours_count INTEGER,
    min_rating INTEGER,
    time_on_game INTEGER
);
"""

cursor.execute(create_table_query)

# чтение данных
with open("01/item.json", "r", encoding="utf-8") as f:
    data = json.load(f)

insert_query = """
INSERT OR IGNORE INTO tournaments (id, name, city, begin, system, tours_count, min_rating, time_on_game)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""

for item in data:
    cursor.execute(
        insert_query,
        (
            item["id"],
            item["name"],
            item["city"],
            item["begin"],
            item["system"],
            item["tours_count"],
            item["min_rating"],
            item["time_on_game"],
        ),
    )

conn.commit()


# 1. Вывод первых (VAR + 10) строк в json
VAR = 10

result_query = f"""
SELECT * from tournaments 
ORDER BY min_rating DESC
LIMIT {VAR + 10}
"""

cursor.execute(result_query)
result = cursor.fetchall()

with open("01/sorted_tournaments.json", "w", encoding="utf-8") as f:
    json.dump(
        [
            dict(zip([column[0] for column in cursor.description], row))
            for row in result
        ],
        f,
        ensure_ascii=False,
        indent=4,
    )

# 2. Статистика по time_on_game
cursor.execute("SELECT time_on_game FROM tournaments")
time = [row[0] for row in cursor.fetchall()]
time_stat = {
    "sum": sum(time),
    "min": min(time),
    "max": max(time),
    "average": statistics.mean(time),
    "median": statistics.median(time),
    "stdev": statistics.stdev(time),
}

with open("01/time_stat.json", "w", encoding="utf-8") as f:
    json.dump(time_stat, f, ensure_ascii=False, indent=4)

# 3. Частота по system
cursor.execute("SELECT system FROM tournaments")
systems = [row[0] for row in cursor.fetchall()]
system_freq = {system: systems.count(system) for system in set(systems)}

with open("01/system_freq.json", "w", encoding="utf-8") as f:
    json.dump(system_freq, f, ensure_ascii=False, indent=4)

# 4. Фильтрация по min_rating, сортировка по time_on_game
filtered_query = f"""
SELECT * FROM tournaments
WHERE min_rating > 2500
ORDER BY time_on_game
LIMIT {VAR + 10};
"""

cursor.execute(filtered_query)
filtered_result = cursor.fetchall()

with open("01/filtered_result.json", "w", encoding="utf-8") as f:
    json.dump(
        [
            dict(zip([column[0] for column in cursor.description], row))
            for row in filtered_result
        ],
        f,
        ensure_ascii=False,
        indent=4,
    )


cursor.close()
