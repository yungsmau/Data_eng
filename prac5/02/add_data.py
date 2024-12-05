from pymongo import MongoClient
import pickle


client = MongoClient("mongodb://localhost:27017/")
db = client["job_data_db"]
collection = db["jobs"]
collection.create_index("id", unique=True)

with open("02/task_2_item.pkl", "rb") as file:
    data = pickle.load(file)

collection.insert_many(data)
print("Данные записаны в MongoDB")
print(f"Количество записей в коллекции: {collection.count_documents({})}")
