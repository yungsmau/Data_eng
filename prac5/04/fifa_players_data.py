from pymongo import MongoClient
import pandas as pd


client = MongoClient("mongodb://localhost:27017/")
db = client["fifa_players"]
collection = db["players"]

data = pd.read_csv("04/players_20.csv")
data_to_dict = data.to_dict(orient="records")

collection.insert_many(data_to_dict)
print("Данные успешно записаны в MongoDB.")
