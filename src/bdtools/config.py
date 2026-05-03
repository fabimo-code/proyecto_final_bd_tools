from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectPaths:
    """Rutas estándar del proyecto."""

    root: Path = Path(__file__).resolve().parents[2]
    raw_csv: Path = root / "data" / "raw" / "sievcac_reclutamiento_nna.csv"
    interim_dir: Path = root / "data" / "interim"
    processed_dir: Path = root / "data" / "processed"
    figures_dir: Path = root / "reports" / "figures"
    tables_dir: Path = root / "reports" / "tables"
    models_dir: Path = root / "models"


PATHS = ProjectPaths()
