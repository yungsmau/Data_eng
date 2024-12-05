from pymongo import MongoClient
import json


client = MongoClient("mongodb://localhost:27017/")
db = client["job_data_db"]
collection = db["jobs"]


def save_to_json(pipeline, filename):
    results = list(collection.aggregate(pipeline))

    with open(f"02/answers/{filename}", "w", encoding="utf-8") as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    print(f"Результаты сохранены в {filename}")


# 1.
pipeline_1 = [
    {
        "$group": {
            "_id": None,
            "min_salary": {"$min": "salary"},
            "avg_salary": {"$avg": "$salary"},
            "max_salary": {"$max": "$salary"},
        }
    }
]

save_to_json(pipeline_1, "min_avg_max_salary.json")

# 2.
pipeline_2 = [{"$group": {"_id": "$job", "count": {"$count": {}}}}]

save_to_json(pipeline_2, "count_by_job.json")

# 3.
pipeline_3 = [
    {
        "$group": {
            "_id": "$city",
            "min_salary": {"$min": "$salary"},
            "avg_salary": {"$avg": "$salary"},
            "max_salary": {"$max": "$salary"},
        }
    }
]

save_to_json(pipeline_3, "min_avg_max_salary_by_city.json")

# 4.
pipeline_4 = [
    {
        "$group": {
            "_id": "$job",
            "min_salary": {"$min": "$salary"},
            "avg_salary": {"$avg": "$salary"},
            "max_salary": {"$max": "$salary"},
        }
    }
]

save_to_json(pipeline_4, "min_avg_max_salary_by_job.json")

# 5.
pipeline_5 = [
    {
        "$group": {
            "_id": "$city",
            "min_age": {"$min": "$age"},
            "avg_age": {"$avg": "$age"},
            "max_age": {"$max": "$age"},
        }
    }
]

save_to_json(pipeline_5, "min_avg_max_age_by_city.json")

# 6.
pipeline_6 = [
    {
        "$group": {
            "_id": "$job",
            "min_age": {"$min": "$age"},
            "avg_age": {"$avg": "$age"},
            "max_age": {"$max": "$age"},
        }
    }
]

save_to_json(pipeline_6, "min_avg_max_age_by_job.json")

# 7.
pipeline_7 = [
    {"$group": {"_id": None, "min_age": {"$min": "$age"}}},
    {
        "$lookup": {
            "from": "your_collection_name",
            "let": {"min_age": "$min_age"},
            "pipeline": [
                {"$match": {"$expr": {"$eq": ["$age", "$$min_age"]}}},
                {"$group": {"_id": None, "max_salary": {"$max": "$salary"}}},
            ],
            "as": "max_salary_at_min_age",
        }
    },
    {"$unwind": "$max_salary_at_min_age"},
]

save_to_json(pipeline_7, "max_salary_at_min_age.json")

# 8.
pipeline_8 = [
    {"$group": {"_id": None, "max_age": {"$max": "$age"}}},
    {
        "$lookup": {
            "from": "your_collection_name",
            "let": {"max_age": "$max_age"},
            "pipeline": [
                {"$match": {"$expr": {"$eq": ["$age", "$$max_age"]}}},
                {"$group": {"_id": None, "min_salary": {"$min": "$salary"}}},
            ],
            "as": "min_salary_at_max_age",
        }
    },
    {"$unwind": "$min_salary_at_max_age"},
]

save_to_json(pipeline_8, "min_salary_at_max_age.json")

# 9.
pipeline_9 = [
    {"$match": {"salary": {"$gt": 50000}}},
    {
        "$group": {
            "_id": "$city",
            "min_age": {"$min": "$age"},
            "avg_age": {"$avg": "$age"},
            "max_age": {"$max": "$age"},
        }
    },
    {"$sort": {"avg_age": -1}},
]

save_to_json(pipeline_9, "age_by_city_salary_over_50k.json")

# 10.
pipeline_10 = [
    {
        "$match": {
            "$or": [{"age": {"$gt": 18, "$lt": 25}}, {"age": {"$gt": 50, "$lt": 65}}]
        }
    },
    {
        "$group": {
            "_id": {
                "city": "$city",
                "job": "$job",
                "age_range": {"$cond": [{"$lt": ["$age", 25]}, "18-25", "50-65"]},
            },
            "min_salary": {"$min": "$salary"},
            "avg_salary": {"$avg": "$salary"},
            "max_salary": {"$max": "$salary"},
        }
    },
]

save_to_json(pipeline_10, "salary_by_age_ranges.json")
