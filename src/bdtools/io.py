from pathlib import Path

import pandas as pd

from .cleaning import clean_sievcac, summarize_quality
from .config import PATHS


def read_raw_csv(path: str | Path = PATHS.raw_csv) -> pd.DataFrame:
    """
    Lee el CSV como texto para evitar que pandas convierta años como '2.004' en 2.004.
    """
    path = Path(path)
    return pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8")


def run_etl(raw_path: str | Path = PATHS.raw_csv) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Ejecuta lectura + limpieza + exportación a Parquet/CSV."""
    PATHS.interim_dir.mkdir(parents=True, exist_ok=True)
    PATHS.processed_dir.mkdir(parents=True, exist_ok=True)
    PATHS.tables_dir.mkdir(parents=True, exist_ok=True)

    raw = read_raw_csv(raw_path)
    clean = clean_sievcac(raw)
    quality = summarize_quality(clean)

    # Parquet es el formato recomendado para pipelines analíticos.
    # Si pyarrow/fastparquet no está instalado, el pipeline no se cae: deja CSV.
    try:
        clean.to_parquet(PATHS.processed_dir / "sievcac_clean.parquet", index=False)
    except ImportError:
        pass

    clean.to_csv(PATHS.processed_dir / "sievcac_clean.csv", index=False, encoding="utf-8")
    quality.to_csv(PATHS.tables_dir / "data_quality.csv", index=False, encoding="utf-8")

    return clean, quality
