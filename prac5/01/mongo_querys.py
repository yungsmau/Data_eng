from pymongo import MongoClient
import json


client = MongoClient("mongodb://localhost:27017/")
db = client["job_data_db"]
collection = db["jobs"]


# 1. Первые 10 записей, отсортированных по убыванию по полю salary;
def sort_by_salary(collection):
    sort_field = [("salary", -1)]
    result = list(collection.find({}, {"_id": 0}).sort(sort_field).limit(10))

    return result


with open("01/query_results/sorted_salary.json", "w", encoding="utf-8") as f:
    json.dump(sort_by_salary(collection), f, ensure_ascii=False, indent=4)


# 2. Первые 15 записей, отфильтрованных по предикату age  <  30, отсортировать по убыванию по полю salary
def sort_salary_by_age(collection):
    query_filter = {"age": {"$lt": 30}}
    sort_field = [("salary", -1)]
    result = list(collection.find(query_filter, {"_id": 0}).sort(sort_field).limit(15))

    return result


with open("01/query_results/sorted_salary_by_age.json", "w", encoding="utf-8") as f:
    json.dump(sort_salary_by_age(collection), f, ensure_ascii=False, indent=4)


# 3. 10 записей по СПБ: инженер, программист, архитектор; age
def specific_jobs(collection):
    query = {
        "city": "Санкт-Петербург",
        "job": {"$in": ["Инженер", "Программист", "Архитектор"]},
    }
    sort_field = [("age", 1)]
    result = list(collection.find(query, {"_id": 0}).sort(sort_field).limit(10))

    return result


with open("01/query_results/specific_jobs.json", "w", encoding="utf-8") as f:
    json.dump(specific_jobs(collection), f, ensure_ascii=False, indent=4)


# 4. Вывод количества записей, получаемых в результате следующей фильтрации (age в произвольном диапазоне, year в [2019,2022], 50 000 < salary <= 75 000 || 125 000 < salary < 150 000).
def super_qeury(collection):
    query = {
        "age": {"$gte": 25, "$lte": 40},
        "year": {"$gte": 2019, "$lte": 2022},
        "$or": [
            {"salary": {"$gt": 50000, "$lte": 75000}},
            {"salary": {"$gt": 125000, "$lt": 150000}},
        ],
    }

    return collection.count_documents(query)


with open("01/query_results/count.json", "w", encoding="utf-8") as f:
    json.dump({"count": super_qeury(collection)}, f, ensure_ascii=False, indent=4)
