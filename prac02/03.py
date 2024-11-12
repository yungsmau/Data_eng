import pandas as pd
import json
import msgpack
import os


with open("85/third_task.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

df = pd.DataFrame(data)

aggregated_data = df.groupby("name")["price"].agg(["mean", "max", "min"]).reset_index()
aggregated_data.rename(
    columns={"mean": "avg_price", "max": "max_price", "min": "min_price"}, inplace=True
)

aggregated_dict = aggregated_data.to_dict(orient="records")

with open("answers/aggregated_03.json", "w", encoding="utf-8") as f:
    json.dump(aggregated_dict, f, ensure_ascii=False, indent=4)

with open("answers/aggregated_data_03.msgpack", "wb") as f:
    packed_data = msgpack.packb(aggregated_dict, use_bin_type=True)
    f.write(packed_data)

json_size = os.path.getsize("answers/aggregated_03.json")
msgpack_size = os.path.getsize("answers/aggregated_data_03.msgpack")

print(f"Размер JSON файла: {json_size} байт")
print(f"Размер Msgpack файла: {msgpack_size} байт")
print(f"Разница в размере: {json_size - msgpack_size} байт")
