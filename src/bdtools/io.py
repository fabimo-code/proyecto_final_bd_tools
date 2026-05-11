from pathlib import Path

import pandas as pd

from bdtools.cleaning import build_quality_report, clean_dataset
from bdtools.config import CLEAN_CSV, CLEAN_PARQUET, DIRECTORIES, QUALITY_TABLE, RAW_DATA_FILE, RAW_DIR


def ensure_directories() -> None:
    for directory in DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


def find_raw_file() -> Path:
    candidates = []
    for pattern in ("*.csv", "*.xlsx", "*.xls"):
        candidates.extend(sorted(RAW_DIR.glob(pattern)))

    if not candidates:
        raise FileNotFoundError(f"No se encontró archivo fuente en {RAW_DIR}")

    return candidates[0]


def read_raw_data(path: str | Path | None = None) -> pd.DataFrame:
    source = Path(path) if path else RAW_DATA_FILE
    if not source.exists():
        source = find_raw_file()

    suffix = source.suffix.lower()
    if suffix == ".csv":
        try:
            return pd.read_csv(source)
        except UnicodeDecodeError:
            return pd.read_csv(source, encoding="latin-1")

    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(source)

    raise ValueError(f"Formato no soportado: {source.suffix}")


def save_processed_data(df: pd.DataFrame) -> None:
    ensure_directories()
    df.to_csv(CLEAN_CSV, index=False)
    df.to_parquet(CLEAN_PARQUET, index=False)


def save_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    ensure_directories()
    report = build_quality_report(df)
    report.to_csv(QUALITY_TABLE, index=False)
    return report


def load_processed_data(path: str | Path = CLEAN_PARQUET) -> pd.DataFrame:
    source = Path(path)
    if source.suffix.lower() == ".csv":
        return pd.read_csv(source)
    return pd.read_parquet(source)


def run_etl(path: str | Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    ensure_directories()
    raw_data = read_raw_data(path)
    clean_data = clean_dataset(raw_data)
    save_processed_data(clean_data)
    quality_report = save_quality_report(clean_data)
    return clean_data, quality_report
