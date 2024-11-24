from bs4 import BeautifulSoup
import json
import glob
import statistics


def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    books = []

    for book in soup.find_all("li", class_="book-item__item"):
        book_cover = (
            book.find("a", class_="book-item__link")
            .find("img")["data-pagespeed-lazy-src"]
            .strip()
        )

        book_rating = float(
            book.find("div", class_="book-item__rating")
            .string.replace(",", ".")
            .strip()
        )

        book_title = book.find("a", class_="book-item__title").string.strip()

        book_author = book.find("a", class_="book-item__author").string.strip()

        book_read = int(
            book.find("a", class_="icon-added-grey")["title"].split()[0].strip()
        )

        book_want = int(
            book.find("a", class_="icon-read-grey")["title"].split()[0].strip()
        )

        book_reviews = int(
            book.find("a", class_="icon-review-grey")["title"].split()[0].strip()
        )

        book_quotes = int(
            book.find("a", class_="icon-quote-grey")["title"].split()[0].strip()
        )

        isbn = (
            book.find("td", string=lambda t: t and "ISBN:" in t)
            .find_next_sibling("td")
            .string.strip()
        )

        year = int(
            book.find("td", string=lambda t: t and "Год издания:" in t)
            .find_next_sibling("td")
            .string.strip()
        )

        publisher = (
            book.find("table", class_="book-item-edition")
            .find("a", class_="lists-edition__link")
            .string.strip()
        )

        language = (
            book.find("td", string=lambda t: t and ("Язык:" in t or "Языки:" in t))
            .find_next_sibling("td")
            .string.strip()
        )

        books.append(
            {
                "book_cover": book_cover,
                "book_rating": book_rating,
                "book_title": book_title,
                "book_author": book_author,
                "book_read": book_read,
                "book_want": book_want,
                "book_reviews": book_reviews,
                "book_quotes": book_quotes,
                "isbn": isbn,
                "year": year,
                "publisher": publisher,
                "language": language,
            }
        )

    return books


all_books = []
file_path = "05/multiple_items/multiple_items.html"
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()
    books = parse_html(html_content)
    all_books.extend(books)

with open("05/multiple_items/multiple_books_data.json", "w", encoding="utf-8") as f:
    json.dump(all_books, f, ensure_ascii=False, indent=4)


# 1. Сортировка по году
sorted_books = sorted(all_books, key=lambda x: x["year"])
with open("05/multiple_items/sorted_m_books.json", "w", encoding="utf-8") as f:
    json.dump(sorted_books, f, ensure_ascii=False, indent=4)


# 2. Фильтрация по rating
filtered_books = [b for b in all_books if b["book_rating"] >= 4.8]
with open("05/multiple_items/filtered_m_books.json", "w", encoding="utf-8") as f:
    json.dump(filtered_books, f, ensure_ascii=False, indent=4)


# 3. Статистика для read
read = [b["book_read"] for b in all_books]
read_stats = {
    "sum": sum(read),
    "min": min(read),
    "max": max(read),
    "average": statistics.mean(read),
    "median": statistics.median(read),
    "stdev": statistics.stdev(read),
}
with open("05/multiple_items/read_stats.json", "w", encoding="utf-8") as f:
    json.dump(read_stats, f, ensure_ascii=False, indent=4)


# 4. Частота по author
author_freq = {}
for book in all_books:
    author = book["book_author"]
    author_freq[author] = author_freq.get(author, 0) + 1

with open("05/multiple_items/authors_freq.json", "w", encoding="utf-8") as f:
    json.dump(author_freq, f, ensure_ascii=False, indent=4)
