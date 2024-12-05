from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["job_data_db"]
collection = db["jobs"]


# 1.
def delete_by_salary():
    result = collection.delete_many(
        {"$or": [{"salary": {"$lt": 25000}}, {"salary": {"$gt": 175000}}]}
    )
    print(
        f"Удалено {result.deleted_count} документов с зарплатой < 25000 или > 175000."
    )


# 2.
def increment_age():
    result = collection.update_many({}, {"$inc": {"age": 1}})
    print(f"Возраст увеличен на 1 для {result.modified_count} документов.")


# 3.
def increase_salary_for_jobs(jobs):
    result = collection.update_many({"job": {"$in": jobs}}, {"$mul": {"salary": 1.05}})
    print(f"Зарплата увеличена на 5% для {result.modified_count} документов.")


# 4.
def increase_salary_for_cities(cities):
    result = collection.update_many(
        {"city": {"$in": cities}}, {"$mul": {"salary": 1.07}}
    )
    print(f"Зарплата увеличена на 7% для {result.modified_count} документов.")


# 5.
def increase_salary_for_complex_query(city, jobs, age_range):
    result = collection.update_many(
        {
            "city": city,
            "job": {"$in": jobs},
            "age": {"$gte": age_range[0], "$lte": age_range[1]},
        },
        {"$mul": {"salary": 1.10}},
    )
    print(
        f"Заработная плата увеличена на 10% для {result.modified_count} документов по сложному предикату."
    )


# 6.
def delete_by_predicate():
    predicate = {"year": {"$lt": 2000}}
    result = collection.delete_many(predicate)
    print(f"Удалено {result.deleted_count} документов по году, раньше 2000.")


delete_by_salary()
increment_age()
increase_salary_for_jobs(["Инженер", "Программист"])
increase_salary_for_cities(["Кордова", "Санхенхо"])
increase_salary_for_complex_query("Санкт-Петербург", ["Медсестра"], (25, 40))
delete_by_predicate()
