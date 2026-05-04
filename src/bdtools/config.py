from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


ROOT_DIR = Path(__file__).resolve().parents[2]

if load_dotenv is not None:
    load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class ProjectPaths:
    root: Path = ROOT_DIR
    data_raw: Path = ROOT_DIR / "data" / "raw"
    data_processed: Path = ROOT_DIR / "data" / "processed"
    reports: Path = ROOT_DIR / "reports"
    figures: Path = ROOT_DIR / "reports" / "figures"
    tables: Path = ROOT_DIR / "reports" / "tables"
    models: Path = ROOT_DIR / "models"

    @property
    def clean_csv(self) -> Path:
        return self.data_processed / "sievcac_limpio.csv"

    @property
    def clean_parquet(self) -> Path:
        return self.data_processed / "sievcac_limpio.parquet"

    @property
    def geojson(self) -> Path:
        return self.data_processed / "sievcac_geo.geojson"


@dataclass(frozen=True)
class DatabaseConfig:
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")
    postgres_db: str = os.getenv("POSTGRES_DB", "sievcac")
    postgres_user: str = os.getenv("POSTGRES_USER", "bdtools")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "bdtools")

    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    mongo_db: str = os.getenv("MONGO_DB", "sievcac")
    mongo_collection: str = os.getenv("MONGO_COLLECTION", "casos")

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


PATHS = ProjectPaths()
DB = DatabaseConfig()


def ensure_directories(paths: ProjectPaths = PATHS) -> None:
    for path in [
        paths.data_raw,
        paths.data_processed,
        paths.figures,
        paths.tables,
        paths.models,
    ]:
        path.mkdir(parents=True, exist_ok=True)
