"""CSV ingestion helpers for the Graph RAG module."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.schemas import LoadedTable


def load_csv_tables(data_path: Path) -> dict[str, LoadedTable]:
    """Load every CSV file in the raw data directory into memory."""
    csv_paths = sorted(data_path.glob("*.csv"))
    if not csv_paths:
        raise FileNotFoundError(f"No CSV files were found in {data_path}.")

    tables: dict[str, LoadedTable] = {}
    for csv_path in csv_paths:
        table_name = csv_path.stem
        tables[table_name] = LoadedTable(
            name=table_name,
            path=csv_path,
            dataframe=pd.read_csv(csv_path),
        )
    return tables
