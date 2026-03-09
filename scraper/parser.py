from __future__ import annotations

"""
HTML parsing utilities using BeautifulSoup.
"""

from typing import Dict, List, Any

from bs4 import BeautifulSoup


def extract_text(element) -> str:
    """
    Safely extract and normalize text content from a BeautifulSoup element.
    """
    if element is None:
        return ""
    return " ".join(element.get_text(strip=True).split())


def parse_items(html: str, selectors: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Parse directory items from a page of HTML.

    Parameters
    ----------
    html:
        Raw HTML string for the current page.
    selectors:
        Dictionary of CSS selectors:
        - item
        - name
        - email
        - location
        - website
        - company

    Returns
    -------
    list of dict
        Each dict contains the extracted fields.
    """
    soup = BeautifulSoup(html, "html.parser")
    item_selector = selectors.get("item") or ""
    if not item_selector:
        return []

    items = soup.select(item_selector)
    results: List[Dict[str, Any]] = []

    for block in items:
        name_sel = selectors.get("name") or ""
        email_sel = selectors.get("email") or ""
        location_sel = selectors.get("location") or ""
        website_sel = selectors.get("website") or ""
        company_sel = selectors.get("company") or ""

        name_el = block.select_one(name_sel) if name_sel else None
        email_el = block.select_one(email_sel) if email_sel else None
        location_el = block.select_one(location_sel) if location_sel else None
        website_el = block.select_one(website_sel) if website_sel else None
        company_el = block.select_one(company_sel) if company_sel else None

        website_url = ""
        if website_el is not None:
            # Prefer href attribute if present.
            website_url = website_el.get("href") or extract_text(website_el)

        result: Dict[str, Any] = {
            "name": extract_text(name_el),
            "email": extract_text(email_el),
            "location": extract_text(location_el),
            "website": website_url,
            "company": extract_text(company_el),
        }
        results.append(result)

    return results

