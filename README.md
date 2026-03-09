### directory_scraper_pro

Professional, reusable scraping toolkit for directory-style websites built with **async Playwright**, **BeautifulSoup4**, and **pandas**.

The script collects the following fields (when available):
- **Name**
- **Email**
- **Location**
- **Website URL**
- **Company name**

All scraping is done asynchronously with Playwright, parsed with BeautifulSoup, and exported to CSV and Excel.

---

## Features

- **Async scraping**: Uses Playwright's async API for fast, reliable scraping.
- **Pagination support**: Follows "next page" links using a configurable CSS selector.
- **Configurable selectors**: Centralized selectors in `scraper/config.py` (overridable via `.env`).
- **Functional style**: Pure functions and modules, no custom classes.
- **Export to CSV and Excel**: Uses `pandas` (CSV + `.xlsx`).
- **Logging to file**: Logs go to `logs/app.log` (and also to console).
- **Retry on error**: Simple async retry wrapper around page fetches.
- **Delay between requests**: Configurable global delay between page loads.
- **Headless mode option**: Toggle via `.env` or CLI.
- **Timeout handling**: Configurable page load timeout.

---

## Project structure

```text
directory_scraper_pro/
├── scraper/
│   ├── config.py       # Configuration & selectors
│   ├── browser.py      # Async Playwright helpers
│   ├── parser.py       # BeautifulSoup parsing logic
│   ├── paginator.py    # Pagination helpers
│   ├── exporter.py     # CSV / Excel export
│   ├── utils.py        # Logging, retries, directory setup
│   ├── scraper.py      # High-level scraping pipeline
│
├── data/               # Output CSV / Excel files
├── logs/               # Log files
├── .env                # Environment-based configuration
├── main.py             # CLI entrypoint
├── requirements.txt
├── README.md
```

---

## Installation

This project is configured to use **uv** for dependency management.

1. **Create and activate a virtual environment (recommended)**:

```bash
uv venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux / macOS
```

2. **Install dependencies with uv**:

```bash
uv sync
uv run playwright install
```

> `uv run playwright install` is required once to download the browser binaries.

---

## How to run

Basic usage from the project root:

```bash
python main.py --url https://example.com/directory --pages 5
```

Arguments:

- **`--url`**: Starting URL of the directory (optional; defaults to `BASE_URL` from `.env` or `scraper/config.py`).
- **`--pages`**: Maximum number of pages to scrape (optional; defaults to `MAX_PAGES` from `.env` or `scraper/config.py`).
- **`--headless`**: Override headless mode: `true` or `false` (optional).
- **`--output-prefix`**: Optional prefix for generated file names (without extension).

Example:

```bash
python main.py --url https://example.com/companies --pages 3 --headless true --output-prefix companies_example
```

After running, you will find:

- CSV file in `data/*.csv`
- Excel file in `data/*.xlsx`
- Logs in `logs/app.log`

---

## How to change selectors

You can configure selectors in **two ways**:

### 1. Edit `scraper/config.py`

In `SELECTORS`:

```python
SELECTORS = {
    "item": ".directory-item",
    "name": ".directory-item .name",
    "email": ".directory-item .email",
    "location": ".directory-item .location",
    "website": ".directory-item a.website",
    "company": ".directory-item .company",
}

PAGINATION_SELECTOR = "a.next"
```

Adjust the CSS selectors to match the structure of your target website.

### 2. Use `.env` overrides

In `.env`:

```text
SELECTOR_ITEM=.directory-item
SELECTOR_NAME=.directory-item .name
SELECTOR_EMAIL=.directory-item .email
SELECTOR_LOCATION=.directory-item .location
SELECTOR_WEBSITE=.directory-item a.website
SELECTOR_COMPANY=.directory-item .company
PAGINATION_SELECTOR=a.next
```

These environment variables override the defaults in `config.py` without changing the code.

---

## Example output

Example CSV/Excel rows will look like:

```text
name,email,location,website,company
John Doe,john@example.com,New York,https://johndoe.com,John Doe Consulting
Jane Smith,jane@acme.com,London,https://acme.com,Acme Ltd
...
```

If some fields are not available on the page, they will appear as empty strings.

---

## Why Playwright?

- **Modern browser automation**: Playwright can handle JavaScript-heavy, dynamic websites that traditional HTTP clients struggle with.
- **Reliability**: Better control over navigation, timeouts, and waiting conditions.
- **Cross-browser support**: Chromium, Firefox, and WebKit (this project uses Chromium by default).

---

## Why async?

- **Concurrency**: Async Playwright allows non-blocking operations, so page loads and delays do not freeze the entire script.
- **Scalability**: Easier to extend to multiple concurrent browsers or pages in the future.
- **Responsiveness**: Async patterns work well with timeouts, retries, and graceful cancellation.

---

## Notes

- Keep scraping **polite**: respect `robots.txt`, terms of service, and local laws.
- Add additional fields by expanding `SELECTORS` and enhancing `scraper/parser.py`.
- You can integrate this library into larger data pipelines by importing `scraper.scraper.scrape_directory` in your own Python code.

