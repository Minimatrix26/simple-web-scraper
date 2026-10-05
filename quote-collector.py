import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

START_URL = "https://quotes.toscrape.com/page/1/"
HEADERS = {"User-Agent": "PaginatedQuoteCollector/1.0 (learning project)"}
OUTPUT_FILE = "quotes.csv"
TAG_OUTPUT_FILE = "quotes_love.csv"
TARGET_TAG = "love"

def fetch_soup(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")

def parse_quotes(soup, page_url):
    quotes = []

    for card in soup.select("div.quote"):
        tag_names = [
            tag.get_text(strip=True)
            for tag in card.select("div.tags a.tag")
        ]

        quotes.append(
            {
                "text": card.select_one("span.text").get_text(strip=True),
                "author": card.select_one("small.author").get_text(strip=True),
                "tags": ", ".join(tag_names),
                "source_url": page_url,
            }
        )

    return quotes


def collect_quotes():
    current_url = START_URL
    all_quotes = []
    page_number = 1

    while current_url:
        soup = fetch_soup(current_url)
        page_quotes = parse_quotes(soup, current_url)
        all_quotes.extend(page_quotes)
        print(
            f"Page {page_number}: collected {len(page_quotes)} quotes "
            f"({len(all_quotes)} total)"
        )

        next_link = soup.select_one("li.next a")
        current_url = (
            urljoin(current_url, next_link.get("href", ""))
            if next_link
            else None
        )

        if current_url:
            time.sleep(0.5)

        page_number += 1
    
    return all_quotes

def save_csv(quotes, filename=OUTPUT_FILE):
    fieldnames = ["text", "author", "tags", "source_url"]

    with open(filename, 'w', newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(quotes)

def print_top_authors(quotes, limit=5):
    author_counts = {}

    for quote in quotes:
        author = quote["author"]
        author_counts[author] = author_counts.get(author, 0) + 1

    ranked_authors = sorted(
        author_counts.items(),
        key=lambda item: (-item[1], item[0]),
    )[:limit]

    print(f"\n Top {limit} authors:")
    for author, count in ranked_authors:
        print(f"{count} | {author}")

def filter_quotes_by_tag(quotes, target_tag):
    return [
        quote 
        for quote in quotes
        if target_tag in quote["tags"].split(", ")
    ]

def main():
    try:
       quotes = collect_quotes()
    except requests.RequestException as error:
       print(f"Collection failed: {error}")
       return

    save_csv(quotes)
    print(f"\nSaved {len(quotes)} quotes to {OUTPUT_FILE}.")
    print_top_authors(quotes)

    tagged_quotes = filter_quotes_by_tag(quotes, TARGET_TAG)
    save_csv(tagged_quotes, TAG_OUTPUT_FILE)
    print(
        f"\n Saved {len(tagged_quotes)} quotes tagged "
        f"'{TARGET_TAG}' to {TAG_OUTPUT_FILE}."
    )
    

if __name__ == "__main__":
    main()