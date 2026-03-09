from __future__ import annotations

"""
Configuration for the directory scraper.

Edit the selectors below to match the target directory website.
Environment variables (from `.env`) can override some values:
- BASE_URL
- MAX_PAGES
- DELAY
- HEADLESS
"""

from pathlib import Path
import os
from typing import Dict, Any


BASE_URL: str = os.getenv(
    "BASE_URL",
    # Example Yellow Pages search URL (edit search_terms/geo_location_terms as needed)
    "https://www.yellowpages.com/search?search_terms=plumber&geo_location_terms=New+York%2C+NY",
)

# Basic CSS selectors for the directory layout.
# Pre-configured for YellowPages.com search result pages.
SELECTORS: Dict[str, str] = {
    # Each business card
    "item": os.getenv("SELECTOR_ITEM", "div.result"),
    # Business name (and Yellow Pages detail link)
    "name": os.getenv("SELECTOR_NAME", "a.business-name"),
    # Yellow Pages listings rarely contain direct emails; this will often be empty.
    "email": os.getenv("SELECTOR_EMAIL", ""),
    # Location: full address block (street + city/zip).
    # Yellow Pages typically uses .street-address and .locality; we can target the parent.
    "location": os.getenv("SELECTOR_LOCATION", "div.info div.info-primary"),
    # External website link (if present).
    "website": os.getenv("SELECTOR_WEBSITE", "a.track-visit-website"),
    # Company name is the same as business name on Yellow Pages.
    "company": os.getenv("SELECTOR_COMPANY", "a.business-name"),
}

# Selector used to locate the "next page" link or button.
PAGINATION_SELECTOR: str = os.getenv("PAGINATION_SELECTOR", "a.next")

# Wait for this selector before scraping (for JS-rendered content). Empty = no wait.
WAIT_FOR_SELECTOR: str = os.getenv("WAIT_FOR_SELECTOR", "div.result")

# Maximum number of pages to scrape (can be overridden via CLI).
MAX_PAGES: int = int(os.getenv("MAX_PAGES", "5"))

# Delay (in seconds) between page requests.
DELAY: float = float(os.getenv("DELAY", "2.0"))

# Headless mode for Playwright browser.
HEADLESS: bool = os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes", "on"}

# Default timeout (in milliseconds) for page loads.
PAGE_LOAD_TIMEOUT_MS: int = int(os.getenv("PAGE_LOAD_TIMEOUT_MS", "30000"))

# Project paths
ROOT_DIR: Path = Path(__file__).resolve().parents[2]
DATA_DIR: Path = ROOT_DIR / "data"
LOG_DIR: Path = ROOT_DIR / "logs"


def as_dict() -> Dict[str, Any]:
    """
    Return the current configuration as a dictionary.

    Useful for debugging and logging.
    """
    return {
        "BASE_URL": BASE_URL,
        "SELECTORS": SELECTORS,
        "PAGINATION_SELECTOR": PAGINATION_SELECTOR,
        "WAIT_FOR_SELECTOR": WAIT_FOR_SELECTOR,
        "MAX_PAGES": MAX_PAGES,
        "DELAY": DELAY,
        "HEADLESS": HEADLESS,
        "PAGE_LOAD_TIMEOUT_MS": PAGE_LOAD_TIMEOUT_MS,
        "DATA_DIR": str(DATA_DIR),
        "LOG_DIR": str(LOG_DIR),
    }

