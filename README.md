# Paginated Quote Collector

A simple Python web scraper that crawls the public [Quotes to Scrape](https://quotes.toscrape.com/) website, collects quotes from every paginated page, saves them to CSV, and filters quotes tagged with a target keyword (`love`).

This project is intended as a small learning exercise in web scraping, pagination handling, HTML parsing, and export workflows.

## Features

- Scrapes quote data from every page in the pagination sequence
- Parses each quote's:
  - text
  - author
  - tags
  - source page URL
- Saves all collected quotes to `quotes.csv`
- Saves quotes matching a chosen tag to `quotes_love.csv`
- Prints a top-authors summary for quick review
- Uses polite request pacing via a short delay between page fetches

## Project Structure

```text
paginated-quote-collector/
├── quote-collector.py
├── requirements.txt
├── quotes.csv
├── quotes_love.csv
├── README.md
└── .venv/
```

## Requirements

Python 3.10+ is recommended.

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run the scraper:

```bash
python quote-collector.py
```

The script will:

1. Fetch pages from `https://quotes.toscrape.com/page/1/`
2. Continue through each next page until the end
3. Save all results to `quotes.csv`
4. Filter quotes tagged as `love`
5. Save those to `quotes_love.csv`
6. Print a summary of the most frequent authors

## Output Files

### `quotes.csv`
Contains all collected quotes with the following columns:

- `text`
- `author`
- `tags`
- `source_url`

### `quotes_love.csv`
Contains only quotes whose tags include `love`.

## Notes

- This project targets a demo website intended for learning and testing web scraping.
- Always check a site's `robots.txt` and terms of use before scraping in production or at scale.
- The script includes a small delay between requests to reduce load and behave more politely.

## Dependencies

- `requests`
- `beautifulsoup4`

## License

This project is provided for educational purposes and does not include a formal license unless you add one.
