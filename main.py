from __future__ import annotations

"""
CLI entrypoint for the directory scraper.
"""

import argparse
import asyncio
import logging
from typing import Optional

from dotenv import load_dotenv

from scraper import config
from scraper.scraper import scrape_and_export
from scraper.utils import setup_logging


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Async directory scraper using Playwright and BeautifulSoup.",
    )
    parser.add_argument(
        "--url",
        type=str,
        default=None,
        help="Base URL of the directory to scrape. Defaults to BASE_URL from config/env.",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=None,
        help="Maximum number of pages to scrape. Defaults to MAX_PAGES from config/env.",
    )
    parser.add_argument(
        "--headless",
        type=str,
        default=None,
        choices=["true", "false"],
        help="Override headless mode (true/false). Defaults to HEADLESS from config/env.",
    )
    parser.add_argument(
        "--output-prefix",
        type=str,
        default=None,
        help="Optional prefix for output CSV/Excel filenames.",
    )
    return parser.parse_args()


def coerce_headless(value: Optional[str]) -> bool:
    """
    Convert a string CLI flag to a boolean headless value.
    """
    if value is None:
        return config.HEADLESS
    return value.lower() in {"1", "true", "yes", "on"}


async def async_main() -> None:
    """
    Async portion of the CLI.
    """
    args = parse_args()
    headless = coerce_headless(args.headless)

    # Reflect any CLI override into the config module for this run.
    config.HEADLESS = headless  # type: ignore[attr-defined]

    base_url: Optional[str] = args.url or None
    max_pages: Optional[int] = args.pages if args.pages is not None else None

    logging.getLogger(__name__).info(
        "Running scraper | url=%s pages=%s headless=%s",
        base_url or config.BASE_URL,
        max_pages or config.MAX_PAGES,
        headless,
    )

    await scrape_and_export(
        base_url=base_url,
        max_pages=max_pages,
        filename_prefix=args.output_prefix,
    )


def main() -> None:
    """
    Synchronous entrypoint.
    """
    load_dotenv()
    setup_logging()
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logging.getLogger(__name__).warning("Interrupted by user.")


if __name__ == "__main__":
    main()

