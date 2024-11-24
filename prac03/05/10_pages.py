from bs4 import BeautifulSoup
import json
import statistics
import glob


def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    for book in soup.find("div", class_="ll-layout"):
        book_title = soup.find("h1", class_="bc-header__book-title").string.strip()

        book_author = soup.find("a", class_="bc-header__book-author-link")["title"]

        book_cover = soup.find("img", class_="book-cover__image")[
            "data-pagespeed-lazy-src"
        ].strip()

        rating = float(
            soup.find("button", class_="bc-rating__btn")
            .string.replace(",", ".")
            .strip()
        )

        bookread = int(
            soup.find("a", {"data-type": "bookread"})
            .find("span", class_="bc-stat__qty")
            .string.replace("\xa0", "")
            .strip()
        )

        bookwish = int(
            soup.find("a", {"data-type": "bookwish"})
            .find("span", class_="bc-stat__qty")
            .string.replace("\xa0", "")
            .strip()
        )

        reviews = int(
            soup.find("a", {"title": "0 рецензий"})
            .find("span", class_="bc-stat__qty")
            .string.replace("\xa0", "")
            .strip()
        )

        liked_book = int(
            soup.find("a", class_="bc-smiley-rating__link_type_funny").string.strip()
        )

        neutral_book = int(
            soup.find("a", class_="bc-smiley-rating__link_type_neutral").string.strip()
        )
        disliked_book = int(
            soup.find("a", class_="bc-smiley-rating__link_type_sad").string.strip()
        )

    return {
        "book_title": book_title,
        "book_author": book_author,
        "book_cover": book_cover,
        "rating": rating,
        "read": bookread,
        "wish_to_read": bookwish,
        "reviews": reviews,
        "liked_the_book": liked_book,
        "neutral_to_the_book": neutral_book,
        "disliked_book": disliked_book,
    }


all_books = []
for file_path in glob.glob("05/single_item/*html"):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
        books = parse_html(html_content)
        all_books.append(books)

with open("05/single_item/books.json", "w", encoding="utf-8") as f:
    json.dump(all_books, f, ensure_ascii=False, indent=4)


# 1. Сортировка по rating
sorted_books = sorted(all_books, key=lambda x: x["rating"])
with open("05/single_item/sorted_ratings.json", "w", encoding="utf-8") as f:
    json.dump(sorted_books, f, ensure_ascii=False, indent=4)


# 2. Фильтрация по likes >= 30000
filtered_books = [b for b in all_books if b["liked_the_book"] >= 30000]
with open("05/single_item/filtered_books.json", "w", encoding="utf-8") as f:
    json.dump(filtered_books, f, ensure_ascii=False, indent=4)

# 3. Статистика для одног поляй
reviews = [b["reviews"] for b in all_books]
reviews_stats = {
    "sum": sum(reviews),
    "min": min(reviews),
    "max": max(reviews),
    "average": statistics.mean(reviews),
    "median": statistics.median(reviews),
    "stdev": statistics.stdev(reviews),
}
with open("05/single_item/reviews_stats.json", "w", encoding="utf-8") as f:
    json.dump(reviews_stats, f, ensure_ascii=False, indent=4)

# 4. Частота меток по author
author_freq = {}
for book in all_books:
    author = book["book_author"]
    author_freq[author] = author_freq.get(author, 0) + 1

with open("05/single_item/authors_freq.json", "w", encoding="utf-8") as f:
    json.dump(author_freq, f, ensure_ascii=False, indent=4)
