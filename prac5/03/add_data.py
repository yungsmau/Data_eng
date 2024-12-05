from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["job_data_db"]
collection = db["jobs"]
collection.create_index("id", unique=True)


def parse_txt(path):
    records = []
    with open(path, "r", encoding="utf-8") as file:
        record = {}

        for line in file:
            line = line.strip()
            if line.startswith("job::"):
                record["job"] = line.split("::")[1]
            elif line.startswith("salary::"):
                record["salary"] = int(line.split("::")[1])
            elif line.startswith("id::"):
                record["id"] = int(line.split("::")[1])
            elif line.startswith("city::"):
                record["city"] = line.split("::")[1]
            elif line.startswith("year::"):
                record["year"] = int(line.split("::", 1)[1])
            elif line.startswith("age::"):
                record["age"] = int(line.split("::", 1)[1])

            if len(record) == 6:
                records.append(record)
                record = {}

    return records


def insert_data(path):
    records = parse_txt(path)

    if records:
        result = collection.insert_many(records)
        print(f"Добавлено {len(result.inserted_ids)} записей в коллекцию.")
        print(f"Количество записей в коллекции: {collection.count_documents({})}")


insert_data("03/task_3_item.text")
