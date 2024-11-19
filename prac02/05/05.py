import pandas as pd
import json
import msgpack
import os

df = pd.read_csv("05/test.csv")

selected_columns = [
    "tBodyAcc-mean()-X",
    "tBodyAcc-mean()-Y",
    "tBodyAcc-mean()-Z",
    "tBodyAcc-std()-X",
    "tBodyAcc-std()-Y",
    "tBodyAcc-std()-Z",
    "tBodyAcc-mad()-X",
]
df = df[selected_columns]

results = {}
numeric_stats = {}
for column in df.columns:
    numeric_stats[column] = {
        "max": df[column].max(),
        "min": df[column].min(),
        "mean": df[column].mean(),
        "sum": df[column].sum(),
        "std_dev": df[column].std(),
    }

results["numeric_stats"] = numeric_stats

with open("05/data_05.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

df.to_csv("05/data_selected_05.csv")
df.to_json("05/data_selected_05.json", orient="records", lines=True)
df.to_pickle("05/data_selected_05.pkl")

with open("05/data_selected_05.msgpack", "wb") as f:
    packed = msgpack.packb(df.to_dict(orient="records"), use_bin_type=True)
    f.write(packed)


file_sizes = {
    "CSV": os.path.getsize("05/data_selected_05.csv"),
    "JSON": os.path.getsize("05/data_selected_05.json"),
    "MSGpack": os.path.getsize("05/data_selected_05.msgpack"),
    "PKL": os.path.getsize("05/data_selected_05.pkl"),
}

print("Размеры файлов: ")
for format, size in file_sizes.items():
    print(f"{format}: {size / (1024 * 1024):.2f} MB")
