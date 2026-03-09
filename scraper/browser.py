from __future__ import annotations

"""
Async Playwright browser helpers.
"""

from contextlib import asynccontextmanager
from typing import AsyncIterator
import logging
import asyncio

from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from .config import HEADLESS, PAGE_LOAD_TIMEOUT_MS, DELAY, WAIT_FOR_SELECTOR


LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def create_page(headless: bool = HEADLESS) -> AsyncIterator[Page]:
    """
    Create a Playwright page and clean up all resources when done.

    This context manager launches the browser, opens a single page,
    yields it, and ensures everything is closed afterwards.
    """
    async with async_playwright() as p:
        browser: Browser = await p.chromium.launch(headless=headless)
        context: BrowserContext = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page: Page = await context.new_page()
        try:
            yield page
        finally:
            await context.close()
            await browser.close()


async def fetch_page_html(
    page: Page,
    url: str,
    timeout_ms: int = PAGE_LOAD_TIMEOUT_MS,
) -> str:
    """
    Navigate the given page to `url` and return the HTML content.

    Parameters
    ----------
    page:
        Reusable Playwright page instance.
    url:
        Target URL.
    timeout_ms:
        Page load timeout in milliseconds.
    """
    LOGGER.info("Navigating to %s", url)
    await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
    if WAIT_FOR_SELECTOR:
        try:
            await page.wait_for_selector(WAIT_FOR_SELECTOR, timeout=timeout_ms)
        except Exception:  # noqa: BLE001
            LOGGER.warning("Timeout waiting for %s; proceeding with current HTML", WAIT_FOR_SELECTOR)
    await asyncio.sleep(0.5)
    html = await page.content()
    LOGGER.debug("Fetched %d characters of HTML", len(html))
    # Global delay between requests to be polite.
    await asyncio.sleep(DELAY)
    return html

