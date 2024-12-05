from pymongo import MongoClient
import json


client = MongoClient("mongodb://localhost:27017/")
db = client["job_data_db"]
collection = db["jobs"]
collection.create_index("id", unique=True)
print("Соединение успешно!")

with open("01/task_1_item.json", "r", encoding="utf-8") as f:
    data = json.load(f)


if isinstance(data, list):
    collection.insert_many(data)
else:
    collection.insert_one(data)

print("Данные записаны в MongoDB")
print(f"Количество записей в коллекции: {collection.count_documents({})}")
