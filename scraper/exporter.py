from __future__ import annotations

"""
Data export helpers (CSV and Excel).
"""

from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Dict, Any, Tuple

import pandas as pd

from .config import DATA_DIR


def _default_filename_prefix() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"directory_scrape_{timestamp}"


def export_records(
    records: Iterable[Dict[str, Any]],
    base_filename: str | None = None,
    output_dir: Path | None = None,
) -> Tuple[Path, Path]:
    """
    Export records to CSV and Excel.

    Parameters
    ----------
    records:
        Iterable of dictionaries.
    base_filename:
        Optional filename prefix (without extension).
    output_dir:
        Directory for output files. Defaults to the configured data directory.

    Returns
    -------
    tuple[Path, Path]
        Paths to the CSV and Excel files.
    """
    output_dir = output_dir or DATA_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    filename_prefix = base_filename or _default_filename_prefix()
    csv_path = output_dir / f"{filename_prefix}.csv"
    xlsx_path = output_dir / f"{filename_prefix}.xlsx"

    rows: List[Dict[str, Any]] = list(records)
    df = pd.DataFrame(rows)

    df.to_csv(csv_path, index=False, encoding="utf-8")
    df.to_excel(xlsx_path, index=False, engine="openpyxl")

    return csv_path, xlsx_path

