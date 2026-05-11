from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"

RAW_DATA_FILE = RAW_DIR / "Caso_Conflicto_Armado.xlsx"
CLEAN_CSV = PROCESSED_DIR / "sievcac_limpio.csv"
CLEAN_PARQUET = PROCESSED_DIR / "sievcac_limpio.parquet"
QUALITY_TABLE = TABLES_DIR / "calidad_datos.csv"
SUMMARY_TABLE = TABLES_DIR / "resumen_general.csv"
DESCRIPTIVE_TABLE = TABLES_DIR / "estadistica_descriptiva.csv"
CHI2_TABLE = TABLES_DIR / "pruebas_chi_cuadrado.csv"

FIG_CASOS_ANIO = FIGURES_DIR / "casos_por_anio.png"
FIG_TOP_DEPARTAMENTOS = FIGURES_DIR / "top_departamentos.png"
FIG_MODALIDAD = FIGURES_DIR / "modalidad_casos.png"
FIG_RESPONSABLE = FIGURES_DIR / "presunto_responsable.png"

RANDOM_STATE = 42
NULL_THRESHOLD = 0.90
TOP_N = 15

ID_COL = "id_caso"
TARGET_COL = "alto_impacto"
VICTIMS_COL = "total_victimas_caso"
GEO_SOURCE_COL = "latitud_longitud"

DATE_COLUMNS = {
    "year": "anio",
    "month": "mes",
    "day": "dia",
}

TEXT_COLUMNS = [
    "departamento",
    "municipio",
    "region",
    "modalidad",
    "presunto_responsable",
    "tipo_vinculacion",
    "forma_vinculacion",
]

HECHOS_COLUMNS = [
    "abandono_o_despojo_forzado_de_tierras",
    "amenaza_o_intimidacion",
    "ataque_contra_mision_medica",
    "confinamiento_o_restriccion_a_la_movilidad",
    "desplazamiento_forzado",
    "extorsion",
    "lesionados_civiles",
    "pillaje",
    "tortura",
]

EDA_COLUMNS = [
    "anio_valido",
    "departamento",
    "region",
    "modalidad",
    "presunto_responsable",
]

CHI2_VARIABLES = [
    "departamento",
    "region",
    "modalidad",
    "presunto_responsable",
    "tipo_vinculacion",
    "forma_vinculacion",
    "decada",
]

MODEL_FEATURES = [
    "anio_valido",
    "mes_valido",
    "departamento",
    "municipio",
    "region",
    "modalidad",
    "presunto_responsable",
    "tipo_vinculacion",
    "forma_vinculacion",
    "latitud",
    "longitud",
    "total_hechos",
]

DIRECTORIES = [
    RAW_DIR,
    PROCESSED_DIR,
    FIGURES_DIR,
    TABLES_DIR,
]
