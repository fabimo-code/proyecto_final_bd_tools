import re
import unicodedata
from typing import Iterable

import numpy as np
import pandas as pd


NO_INFO_VALUES = {
    "",
    "ND",
    "N/D",
    "NA",
    "NAN",
    "SIN INFORMACION",
    "SIN INFORMACIÓN",
    "DESCONOCIDO",
    "DESCONOCIDA",
    "NO DETERMINADO",
    "NO IDENTIFICADO",
}


def normalize_col_name(name: str) -> str:
    """Convierte nombres de columnas a snake_case sin tildes."""
    text = str(name).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [normalize_col_name(c) for c in out.columns]
    return out


def normalize_year(value) -> pd.Int64Dtype:
    """
    Normaliza años que vienen como texto con punto de miles:
    '2.004' -> 2004, '1.988' -> 1988, '0' -> <NA>.
    """
    if pd.isna(value):
        return pd.NA
    text = str(value).strip()
    if text in {"", "0", "0.0", "nan", "None"}:
        return pd.NA
    text = text.replace(".", "")
    try:
        year = int(float(text))
    except ValueError:
        return pd.NA
    if year < 1900 or year > 2100:
        return pd.NA
    return year


def clean_category(value: object) -> str:
    if pd.isna(value):
        return "NO IDENTIFICADO"
    text = str(value).strip().upper()
    text = unicodedata.normalize("NFKC", text)
    return "NO IDENTIFICADO" if text in NO_INFO_VALUES else text


def extract_point_lon_lat(value: object) -> tuple[float, float]:
    """Extrae longitud y latitud desde WKT tipo POINT (-74.57 6.21)."""
    if pd.isna(value):
        return (np.nan, np.nan)
    match = re.search(r"POINT\s*\(\s*([-0-9.]+)\s+([-0-9.]+)\s*\)", str(value))
    if not match:
        return (np.nan, np.nan)
    return (float(match.group(1)), float(match.group(2)))


def build_fecha_aproximada(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea fecha aproximada sin perder la calidad de la información:
    - año desconocido => fecha NaT
    - mes 0/desconocido => enero como aproximación, con bandera de precisión
    - día 0/desconocido => día 1 como aproximación, con bandera de precisión
    """
    out = df.copy()

    out["mes_original"] = pd.to_numeric(out.get("mes"), errors="coerce").astype("Int64")
    out["dia_original"] = pd.to_numeric(out.get("dia"), errors="coerce").astype("Int64")

    out["mes_aprox"] = out["mes_original"].where(out["mes_original"].between(1, 12), 1)
    out["dia_aprox"] = out["dia_original"].where(out["dia_original"].between(1, 31), 1)

    conditions = [
        out["anio"].isna(),
        out["mes_original"].isna() | (out["mes_original"] == 0),
        out["dia_original"].isna() | (out["dia_original"] == 0),
    ]
    choices = ["sin_fecha", "solo_anio", "anio_mes"]
    out["precision_fecha"] = np.select(conditions, choices, default="anio_mes_dia")

    out["fecha_aproximada"] = pd.NaT
    valid_year = out["anio"].notna()
    out.loc[valid_year, "fecha_aproximada"] = pd.to_datetime(
        {
            "year": out.loc[valid_year, "anio"].astype(int),
            "month": out.loc[valid_year, "mes_aprox"].astype(int),
            "day": out.loc[valid_year, "dia_aprox"].astype(int),
        },
        errors="coerce",
    )
    out["decada"] = (out["anio"] // 10 * 10).astype("Int64")
    return out


def clean_sievcac(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Limpieza principal para el dataset SIEVCAC de reclutamiento/utilización de NNA."""
    df = normalize_columns(raw_df)

    # Identificador y fecha
    if "id_caso" in df.columns:
        df = df.drop_duplicates(subset=["id_caso"]).copy()

    df["anio"] = df["ano"].apply(normalize_year).astype("Int64")
    df = build_fecha_aproximada(df)

    # Coordenadas
    if "latitud_longitud" in df.columns:
        coords = df["latitud_longitud"].apply(extract_point_lon_lat)
        df["longitud"] = coords.apply(lambda x: x[0])
        df["latitud"] = coords.apply(lambda x: x[1])

    # Categorías principales
    categorical_cols = [
        "municipio",
        "departamento",
        "region",
        "modalidad",
        "presunto_responsable",
        "descripcion_presunto_responsable",
        "forma_de_vinculacion",
        "tipo_de_vinculacion",
    ]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_category)

    # Variables numéricas de hechos victimizantes
    numeric_candidates = [
        "abandono_o_despojo_forzado_de_tierras",
        "amenaza_o_intimidacion",
        "ataque_contra_mision_medica",
        "confinamiento_o_restriccion_a_la_movilidad",
        "desplazamiento_forzado",
        "extorsion",
        "lesionados_civiles",
        "pillaje",
        "tortura",
        "total_de_victimas_del_caso",
    ]
    for col in numeric_candidates:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Variables de texto muy escasas: conservar como bandera + detalle
    for col in ["violencia_basada_en_genero", "otro_hecho_simultaneo"]:
        if col in df.columns:
            df[f"flag_{col}"] = (~df[col].fillna("").astype(str).str.strip().isin(["", "0", "ND"])).astype(int)
            df[col] = df[col].apply(clean_category)

    # Feature resumen: cuántos hechos simultáneos se reportan aparte del reclutamiento/utilización.
    hecho_cols = [c for c in numeric_candidates if c in df.columns and c != "total_de_victimas_del_caso"]
    if hecho_cols:
        df["num_hechos_simultaneos"] = (df[hecho_cols] > 0).sum(axis=1)

    if "total_de_victimas_del_caso" in df.columns:
        df["alto_impacto"] = (df["total_de_victimas_del_caso"] > 1).astype(int)

    return df


def summarize_quality(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla compacta de calidad: nulos, únicos y porcentaje de nulos por columna."""
    return (
        pd.DataFrame(
            {
                "columna": df.columns,
                "nulos": df.isna().sum().values,
                "porcentaje_nulos": (df.isna().mean().values * 100).round(2),
                "unicos": df.nunique(dropna=True).values,
                "tipo": [str(t) for t in df.dtypes.values],
            }
        )
        .sort_values(["porcentaje_nulos", "nulos"], ascending=False)
        .reset_index(drop=True)
    )
