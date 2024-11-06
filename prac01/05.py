import pandas as pd

tables = pd.read_html("85/fifth_task.html", encoding="utf-8")
df = tables[0]

df.to_csv("answers/fifth_html.csv", index=False, encoding="utf-8")
print("Таблица была записана в fifth_html.csv")