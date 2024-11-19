import pandas as pd

# удаление колонки
df = pd.read_csv("04/fourth_task.txt")
df = df.drop(columns=["status"])
# фильтрация
df = df[df["price"] > 2451]
df.to_csv("04/new_csv.txt", index=False)


# среднее значение price
average = df["price"].mean()
# максимум и минимум quantity
max = df["quantity"].max()
min = df["quantity"].min()

with open("04/fourth.txt", "w") as new_file:
    new_file.write(f"Среднее арифметическое price: {average}\n")
    new_file.write(f"Max quantity: {max}\n")
    new_file.write(f"Min quantity: {min}")
