import requests
from bs4 import BeautifulSoup

url = [
    "https://www.livelib.ru/book/1000261483-master-i-margarita-mihail-bulgakov",
    "https://www.livelib.ru/book/1000476182-geroj-nashego-vremeni-m-yu-lermontov",
    "https://www.livelib.ru/book/1000396456-prestuplenie-i-nakazanie-fjodor-dostoevskij",
    "https://www.livelib.ru/book/1000456756-ottsy-i-deti-nakanune-sbornik-i-s-turgenev",
    "https://www.livelib.ru/book/1000027561-evgenij-onegin-aleksandr-pushkin",
    "https://www.livelib.ru/book/1000256740-vojna-i-mir-lev-tolstoj",
    "https://www.livelib.ru/book/1000012305-mertvye-dushi-nikolaj-gogol",
    "https://www.livelib.ru/book/1000000895-gore-ot-uma-aleksandr-griboedov",
    "https://www.livelib.ru/book/1000428956-dubrovskij-kapitanskaya-dochka-sbornik-aleksandr-pushkin",
    "https://www.livelib.ru/book/1000473797-vechera-na-hutore-bliz-dikanki-sbornik-nikolaj-gogol",
]


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}

# for i in url:
#     response = requests.get(i, headers)

#     name = f"page_content_{url.index(i) + 1}.html"

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, "html.parser")

#         with open(f"05/single_item/{name}", "w", encoding="utf-8") as file:
#             file.write(str(soup.prettify()))

#         print("Успешно сохранено")
#     else:
#         print("Не удалось сохранить")


multiple_items_url = "https://www.livelib.ru/books/top"

response = requests.get(multiple_items_url, headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    with open("05/multiple_items.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    print("Успешно")
else:
    print("Не удалось сохранить")
