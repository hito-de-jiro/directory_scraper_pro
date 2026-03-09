from __future__ import annotations

"""
Utility helpers for logging, retries, and filesystem setup.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Awaitable, Callable, Coroutine, TypeVar

from .config import DATA_DIR, LOG_DIR


T = TypeVar("T")


def ensure_directories() -> None:
    """
    Ensure that the data and log directories exist.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging() -> None:
    """
    Configure application-wide logging to file and console.
    """
    ensure_directories()
    log_file: Path = LOG_DIR / "app.log"

    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=datefmt,
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


async def async_retry(
    func: Callable[..., Awaitable[T]],
    *args: Any,
    retries: int = 3,
    delay: float = 1.0,
    logger: logging.Logger | None = None,
    **kwargs: Any,
) -> T:
    """
    Execute an async function with simple retry logic.

    Parameters
    ----------
    func:
        Async callable to execute.
    retries:
        Maximum number of attempts (including the first).
    delay:
        Delay in seconds between attempts.
    logger:
        Optional logger for error messages.

    Returns
    -------
    T
        Result of the async function.

    Raises
    ------
    Exception
        The last exception raised if all retries fail.
    """
    attempt = 0
    last_exc: BaseException | None = None
    while attempt < retries:
        try:
            return await func(*args, **kwargs)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            attempt += 1
            if logger:
                logger.warning(
                    "Attempt %d/%d failed: %s", attempt, retries, exc, exc_info=False
                )
            if attempt < retries:
                await asyncio.sleep(delay)
    assert last_exc is not None
    raise last_exc

