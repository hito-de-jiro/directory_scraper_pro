from __future__ import annotations

"""
Pagination helpers.
"""

from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def get_next_page_url(
    html: str,
    current_url: str,
    pagination_selector: str,
) -> Optional[str]:
    """
    Find the URL of the next page using a CSS selector.

    Parameters
    ----------
    html:
        HTML content of the current page.
    current_url:
        URL of the current page (used as base for relative links).
    pagination_selector:
        CSS selector that locates the "next" link or button.

    Returns
    -------
    str | None
        Absolute URL of the next page, or None if not found.
    """
    if not pagination_selector:
        return None

    soup = BeautifulSoup(html, "html.parser")
    next_el = soup.select_one(pagination_selector)
    if next_el is None:
        return None

    href = next_el.get("href")
    if not href:
        return None

    return urljoin(current_url, href)

