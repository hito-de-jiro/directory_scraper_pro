from __future__ import annotations

"""
High-level scraping pipeline.
"""

from typing import Any, Dict, List, Optional, Tuple
import logging

from playwright.async_api import Page

from . import config
from .browser import create_page, fetch_page_html
from .parser import parse_items
from .paginator import get_next_page_url
from .exporter import export_records
from .utils import async_retry


LOGGER = logging.getLogger(__name__)


async def _scrape_single_page(
    page: Page,
    url: str,
) -> Tuple[str, List[Dict[str, Any]], str]:
    """
    Fetch and parse a single page.

    Returns the HTML, parsed items, and the URL (for pagination resolution).
    """
    html = await fetch_page_html(page, url)
    items = parse_items(html, config.SELECTORS)
    return html, items, url


async def scrape_directory(
    base_url: Optional[str] = None,
    max_pages: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Scrape a directory-style website into a list of records.

    Parameters
    ----------
    base_url:
        Starting URL for scraping. If omitted, uses `config.BASE_URL`.
    max_pages:
        Maximum number of pages to visit. If omitted, uses `config.MAX_PAGES`.

    Returns
    -------
    list of dict
        Aggregated records from all pages.
    """
    start_url = base_url or config.BASE_URL
    pages_limit = max_pages if max_pages is not None else config.MAX_PAGES

    LOGGER.info(
        "Starting scrape | url=%s max_pages=%s headless=%s",
        start_url,
        pages_limit,
        config.HEADLESS,
    )

    all_records: List[Dict[str, Any]] = []
    current_url: Optional[str] = start_url
    page_index = 0

    async with create_page(headless=config.HEADLESS) as page:
        while current_url and page_index < pages_limit:
            page_index += 1
            LOGGER.info("Scraping page %d: %s", page_index, current_url)

            try:
                html, items, visited_url = await async_retry(
                    _scrape_single_page,
                    page,
                    current_url,
                    retries=3,
                    delay=config.DELAY,
                    logger=LOGGER,
                )
            except Exception as exc:  # noqa: BLE001
                LOGGER.error(
                    "Failed to scrape page %d (%s): %s",
                    page_index,
                    current_url,
                    exc,
                    exc_info=True,
                )
                break

            LOGGER.info("Found %d items on page %d", len(items), page_index)
            all_records.extend(items)

            next_url = get_next_page_url(
                html,
                visited_url,
                config.PAGINATION_SELECTOR,
            )
            if not next_url:
                LOGGER.info("No further pages detected; stopping pagination.")
                break

            current_url = next_url

    LOGGER.info("Scraping finished; collected %d records.", len(all_records))
    return all_records


async def scrape_and_export(
    base_url: Optional[str] = None,
    max_pages: Optional[int] = None,
    filename_prefix: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Scrape the directory and export results to CSV and Excel.

    Parameters
    ----------
    base_url:
        Optional starting URL.
    max_pages:
        Optional maximum number of pages.
    filename_prefix:
        Optional prefix for the output filenames.

    Returns
    -------
    tuple[str, str]
        Paths (as strings) to the CSV and Excel files.
    """
    records = await scrape_directory(base_url=base_url, max_pages=max_pages)
    csv_path, xlsx_path = export_records(records, base_filename=filename_prefix)
    LOGGER.info("Exported CSV to %s", csv_path)
    LOGGER.info("Exported Excel to %s", xlsx_path)
    return str(csv_path), str(xlsx_path)

