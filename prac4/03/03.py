import sqlite3
import pandas as pd
import json
import statistics
from collections import Counter

conn = sqlite3.connect("03/music_data.db")
cursor = conn.cursor()

# Создание таблицы с ограничением UNIQUE
create_table_query = """
CREATE TABLE IF NOT EXISTS music (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist TEXT,
    song TEXT,
    duration_ms INTEGER,
    year INTEGER,
    tempo REAL,
    genre TEXT,
    energy REAL,
    key INTEGER,
    loudness REAL,
    explicit BOOLEAN,
    popularity INTEGER,
    danceability REAL,
    UNIQUE (artist, song, year)
);
"""
cursor.execute(create_table_query)

# Чтение и вставка из CSV
csv_data = pd.read_csv("03/_part_1.csv", delimiter=";")
insert_query = """
INSERT OR IGNORE INTO music (artist, song, duration_ms, year, tempo, genre, energy, key, loudness)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
"""
for _, row in csv_data.iterrows():
    cursor.execute(
        insert_query,
        (
            row["artist"],
            row["song"],
            int(row["duration_ms"]),
            int(row["year"]),
            float(row["tempo"]),
            row["genre"],
            float(row["energy"]) if pd.notnull(row["energy"]) else None,
            int(row["key"]) if pd.notnull(row["key"]) else None,
            float(row["loudness"]) if pd.notnull(row["loudness"]) else None,
        ),
    )

# Чтение и вставка из JSON
with open("03/_part_2.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)
insert_json_query = """
INSERT OR IGNORE INTO music (artist, song, duration_ms, year, tempo, genre, explicit, popularity, danceability)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
"""
for item in json_data:
    cursor.execute(
        insert_json_query,
        (
            item["artist"],
            item["song"],
            int(item["duration_ms"]),
            int(item["year"]),
            float(item["tempo"]),
            item["genre"],
            bool(item["explicit"]) if "explicit" in item else None,
            int(item["popularity"]) if "popularity" in item else None,
            float(item["danceability"]) if "danceability" in item else None,
        ),
    )

# замена значений жанра set() на unknown
update_query = """
UPDATE music
SET genre = 'unknown'
WHERE genre = 'set()';
"""

cursor.execute(update_query)
conn.commit()


VAR = 5
# 1. Первые отсортированные строки по duration_ms
query_1 = f"""
SELECT * FROM music
ORDER BY duration_ms
LIMIT {VAR + 10}
"""

duration_df = pd.read_sql_query(query_1, conn)
duration_df.to_json(
    "03/sorted_duration.json", orient="records", force_ascii=False, indent=4
)
print("Первый запрос сохранен в 'sorted_duration.json'.")


# 2. Статистика по duration_ms
query_2 = f"""
SELECT duration_ms FROM music;
"""
duration_df = pd.read_sql_query(query_2, conn)
duration_list = duration_df["duration_ms"].tolist()

duration_stat = {
    "sum": sum(duration_list),
    "min": min(duration_list),
    "max": max(duration_list),
    "average": statistics.mean(duration_list),
    "median": statistics.median(duration_list),
    "stdev": statistics.stdev(duration_list),
}

with open("03/duration_stat.json", "w", encoding="utf-8") as f:
    json.dump(duration_stat, f, ensure_ascii=False, indent=4)

print("Первый запрос сохранен в 'duration_stat.json'.")


# 3. Частота по genre
query_3 = """
SELECT genre FROM music;
"""

freq_df = pd.read_sql_query(query_3, conn)
genres = []
for genre_list in freq_df["genre"].dropna():
    genres.extend(genre_list.split(", "))

genre_counts = Counter(genres)

with open("03/genre_freq.json", "w", encoding="utf-8") as f:
    json.dump(genre_counts, f, ensure_ascii=False, indent=4)

print("Третий запрос сохранен в 'genre_freq.json'.")


# 4. Отфильтрованные строки
query_4 = f"""
SELECT * FROM music
WHERE year > 2010
ORDER BY popularity DESC
LIMIT {VAR + 15}
"""

fil_df = pd.read_sql_query(query_4, conn)
fil_df.to_json("03/filtered_music.json", orient="records", force_ascii=False, indent=4)
print("Третий запрос сохранен в 'genre_freq.json'.")


conn.close()
