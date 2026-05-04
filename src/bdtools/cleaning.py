from __future__ import annotations

import re
import unicodedata
from typing import Optional

import numpy as np
import pandas as pd


def clean_column_name(value: str) -> str:
    """Convierte nombres de columnas a snake_case sin tildes."""
    value = str(value).strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def normalize_year(value) -> Optional[int]:
    """Normaliza años que vienen como 2.004, 1.988 o 0."""
    if pd.isna(value):
        return np.nan

    text = str(value).strip()

    if text in {"0", "0.0", ""}:
        return np.nan

    if re.fullmatch(r"\d\.\d{3}", text):
        return int(text.replace(".", ""))

    try:
        number = float(text)
        if 1800 <= number <= 2100:
            return int(number)
    except ValueError:
        pass

    digits = re.sub(r"\D", "", text)
    if len(digits) == 4:
        return int(digits)

    return np.nan


def extract_coordinates(point_text) -> tuple[float, float]:
    """Extrae longitud y latitud desde texto tipo POINT (-74.57 6.21)."""
    if pd.isna(point_text):
        return (np.nan, np.nan)

    match = re.search(r"POINT\s*\(\s*([\-0-9.]+)\s+([\-0-9.]+)\s*\)", str(point_text))
    if not match:
        return (np.nan, np.nan)

    lon = float(match.group(1))
    lat = float(match.group(2))
    return (lon, lat)


def clean_sievcac(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Limpia y enriquece el dataset SIEVCAC RU."""
    df = df_raw.copy()
    df.columns = [clean_column_name(col) for col in df.columns]

    if "ano" in df.columns:
        df["anio"] = df["ano"].apply(normalize_year)
        df = df.drop(columns=["ano"])
    elif "a_o" in df.columns:
        df["anio"] = df["a_o"].apply(normalize_year)
        df = df.drop(columns=["a_o"])
    elif "anio" in df.columns:
        df["anio"] = df["anio"].apply(normalize_year)

    numeric_candidates = [
        "id_caso",
        "id_caso_relacionado",
        "mes",
        "dia",
        "codigo_dane_de_municipio",
        "total_de_victimas_del_caso",
        "abandono_o_despojo_forzado_de_tierras",
        "amenaza_o_intimidacion",
        "ataque_contra_mision_medica",
        "confinamiento_o_restriccion_a_la_movilidad",
        "desplazamiento_forzado",
        "extorsion",
        "lesionados_civiles",
        "pillaje",
        "tortura",
        "violencia_basada_en_genero",
        "otro_hecho_simultaneo",
    ]

    for col in numeric_candidates:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    simultaneous_cols = [
        "abandono_o_despojo_forzado_de_tierras",
        "amenaza_o_intimidacion",
        "ataque_contra_mision_medica",
        "confinamiento_o_restriccion_a_la_movilidad",
        "desplazamiento_forzado",
        "extorsion",
        "lesionados_civiles",
        "pillaje",
        "tortura",
        "violencia_basada_en_genero",
        "otro_hecho_simultaneo",
    ]

    existing_simultaneous = [col for col in simultaneous_cols if col in df.columns]
    if existing_simultaneous:
        df[existing_simultaneous] = df[existing_simultaneous].fillna(0)
        df["cantidad_hechos_simultaneos"] = df[existing_simultaneous].sum(axis=1)

    if "latitud_longitud" in df.columns:
        coords = df["latitud_longitud"].apply(extract_coordinates)
        df["longitud"] = coords.apply(lambda x: x[0])
        df["latitud"] = coords.apply(lambda x: x[1])

    if "total_de_victimas_del_caso" in df.columns:
        df["total_de_victimas_del_caso"] = df["total_de_victimas_del_caso"].fillna(0)
        df["alto_impacto"] = (df["total_de_victimas_del_caso"] > 1).astype(int)

    text_cols = df.select_dtypes(include=["object"]).columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": np.nan, "None": np.nan, "": np.nan})

    if {"anio", "mes"}.issubset(df.columns):
        df["periodo"] = (
            df["anio"].astype("Int64").astype(str)
            + "-"
            + df["mes"].fillna(0).astype(int).astype(str).str.zfill(2)
        )
        df.loc[df["anio"].isna(), "periodo"] = np.nan

    return df
