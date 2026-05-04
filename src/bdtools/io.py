from __future__ import annotations

from pathlib import Path

import pandas as pd

from bdtools.cleaning import clean_sievcac
from bdtools.config import PATHS, ProjectPaths, ensure_directories


def find_raw_csv(paths: ProjectPaths = PATHS) -> Path:
    files = sorted(paths.data_raw.glob("*.csv"))
    if not files:
        raise FileNotFoundError(
            f"No se encontró ningún CSV en {paths.data_raw}. "
            "Copia el archivo original en data/raw/."
        )
    return files[0]


def read_raw_csv(csv_path: Path | None = None) -> pd.DataFrame:
    csv_path = csv_path or find_raw_csv()
    return pd.read_csv(csv_path, encoding="utf-8", sep=None, engine="python")


def save_processed(df: pd.DataFrame, paths: ProjectPaths = PATHS) -> None:
    ensure_directories(paths)
    df.to_csv(paths.clean_csv, index=False, encoding="utf-8-sig")
    try:
        df.to_parquet(paths.clean_parquet, index=False)
    except Exception as exc:
        print(f"No se pudo guardar Parquet. Se continúa con CSV. Detalle: {exc}")


def run_etl(paths: ProjectPaths = PATHS) -> pd.DataFrame:
    ensure_directories(paths)
    raw = read_raw_csv()
    clean = clean_sievcac(raw)
    save_processed(clean, paths)
    return clean
