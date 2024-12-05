from pymongo import MongoClient
import pandas as pd
import json


client = MongoClient("mongodb://localhost:27017/")
db = client["fifa_players"]
collection = db["players"]

# --- Выборка: ---
# 1. По имени игрока
query_1 = collection.find({"short_name": "De Gea"}, {"_id": 0})

# 2. Из определенного клуба
query_2 = collection.find(
    {"club": "FC Barcelona"},
    {
        "_id": 0,
        "short_name": 1,
        "overall": 1,
        "value_eur": 1,
        "age": 1,
        "player_position": 1,
    },
)

# 3. Игроки, моложе 25 лет
query_3 = collection.find(
    {"age": {"$lt": 25}}, {"_id": 0, "short_name": 1, "age": 1, "value_eur": 1}
)

# 4. Игроки с рейтингом > 85
query_4 = collection.find(
    {"overall": {"$gt": 85}},
    {"_id": 0, "short_name": 1, "overall": 1, "age": 1, "value_eur": 1},
)

# 5. Игроки конкретной национальности
query_5 = collection.find(
    {"nationality": "Brazil"},
    {"_id": 0, "short_name": 1, "overall": 1, "age": 1, "value_eur": 1},
)


# --- Выборка с агрегацией: ---
# 1. Средняя выборка для всех игроков
query_6 = collection.aggregate(
    [{"$group": {"_id": None, "avg_overall": {"$avg": "$overall"}}}]
)

# 2. Максимальная зарплата среди всех игроков
query_7 = collection.aggregate(
    [{"$group": {"_id": None, "max_wage": {"$max": "$wage_eur"}}}]
)

# 3. Суммарная рыночная стоимость игроков в клубе
query_8 = collection.aggregate(
    [
        {"$match": {"club": "Juventus"}},
        {"$group": {"_id": None, "total_value": {"$sum": "$value_eur"}}},
    ]
)

# 4. Кол-во игроков по каждой национальности
query_9 = collection.aggregate(
    [
        {"$group": {"_id": "$nationality", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
)

# 5. Средний возраст игроков в клубе
query_10 = collection.aggregate(
    [
        {"$match": {"club": "Real Madrid"}},
        {"$group": {"_id": None, "avg_age": {"$avg": "$age"}}},
    ]
)


# --- Выборка с агрегацией: ---
# 1. Обновление зарплаты игрока
collection.update_one({"short_name": "L. Messi"}, {"$set": {"wage_eur": 1000000}})

# 2. Обновление национальности для всех игроков одно клуба
collection.update_many({"club": "FC Barcelona"}, {"$set": {"nationality": "Spain"}})

# 3. Удаление игроков с ростом < 160
collection.delete_many({"height_cm": {"$lt": 160}})

# 4. Увеличение рейтинга всех игроков моложе 25
collection.update_many({"age": {"$lt": 25}}, {"$inc": {"overall": 1}})

# 5. Удаление игроков с общим рейтингом ниже 50
collection.delete_many({"overall": {"$lt": 50}})
