import requests
import pandas as pd

response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
data = response.json()

df = pd.DataFrame(data["bpi"]).T
df.to_html("06/new_html_from_json.html", border=1, justify="center")

print("Таблица сохранена в new_html_from_json.html")
