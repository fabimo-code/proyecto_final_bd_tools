import re
import unicodedata

import numpy as np
import pandas as pd

from bdtools.config import (
    DATE_COLUMNS,
    GEO_SOURCE_COL,
    HECHOS_COLUMNS,
    NULL_THRESHOLD,
    TARGET_COL,
    TEXT_COLUMNS,
    VICTIMS_COL,
)


def normalize_column_name(name: str) -> str:
    text = unicodedata.normalize("NFKD", str(name))
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    text = text.replace("ano", "anio") if text in {"ano", "ano_valido"} else text
    return text


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data.columns = [normalize_column_name(col) for col in data.columns]
    return data


def build_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    total = len(df)
    report = pd.DataFrame(
        {
            "columna": df.columns,
            "tipo": df.dtypes.astype(str).values,
            "nulos": df.isna().sum().values,
            "porcentaje_nulos": (df.isna().mean().values * 100).round(2),
            "valores_unicos": df.nunique(dropna=True).values,
        }
    )
    report["registros"] = total
    return report.sort_values("porcentaje_nulos", ascending=False).reset_index(drop=True)


def drop_sparse_columns(df: pd.DataFrame, threshold: float = NULL_THRESHOLD) -> pd.DataFrame:
    data = df.copy()
    null_rate = data.isna().mean()
    columns_to_drop = null_rate[null_rate > threshold].index.tolist()
    return data.drop(columns=columns_to_drop)


def normalize_text_values(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    data = df.copy()
    selected_columns = columns or TEXT_COLUMNS
    missing_values = {"", "NAN", "NONE", "NULL", "0", "SIN DATO", "NO REGISTRA"}

    for column in selected_columns:
        if column in data.columns:
            serie = data[column].astype("string").str.strip().str.upper()
            data[column] = serie.mask(serie.isin(missing_values), "SIN INFORMACION")

    return data


def impute_region_from_department(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    if {"departamento", "region"}.issubset(data.columns):
        valid = data.loc[data["region"].notna() & data["departamento"].notna()]
        region_by_department = valid.groupby("departamento")["region"].agg(
            lambda values: values.mode().iat[0] if not values.mode().empty else np.nan
        )
        missing_region = data["region"].isna() | data["region"].eq("SIN INFORMACION")
        data.loc[missing_region, "region"] = data.loc[missing_region, "departamento"].map(region_by_department)
        data["region"] = data["region"].fillna("SIN INFORMACION")
    return data


def fix_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    year_col = DATE_COLUMNS["year"]
    month_col = DATE_COLUMNS["month"]
    day_col = DATE_COLUMNS["day"]

    for original, new_column in [
        (year_col, "anio_valido"),
        (month_col, "mes_valido"),
        (day_col, "dia_valido"),
    ]:
        if original in data.columns:
            numeric = pd.to_numeric(data[original], errors="coerce")
            data[new_column] = numeric.where(numeric > 0, np.nan)

    return data


def extract_coordinates(value) -> tuple[float, float]:
    numbers = re.findall(r"-?\d+(?:\.\d+)?", str(value))
    if len(numbers) < 2:
        return np.nan, np.nan

    longitude, latitude = float(numbers[0]), float(numbers[1])
    if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
        return np.nan, np.nan

    return longitude, latitude


def add_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    if GEO_SOURCE_COL in data.columns:
        coordinates = data[GEO_SOURCE_COL].apply(extract_coordinates)
        data[["longitud", "latitud"]] = pd.DataFrame(coordinates.tolist(), index=data.index)
    return data


def add_decade(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    if "anio_valido" in data.columns:
        data["decada"] = data["anio_valido"].apply(
            lambda value: f"{int(value) // 10 * 10}s" if pd.notna(value) else "SIN FECHA"
        )
    return data


def add_total_hechos(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    available_columns = [column for column in HECHOS_COLUMNS if column in data.columns]
    if available_columns:
        hechos = data[available_columns].apply(pd.to_numeric, errors="coerce").fillna(0)
        data["total_hechos"] = hechos.gt(0).sum(axis=1)
    return data


def add_target(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    if VICTIMS_COL in data.columns:
        victims = pd.to_numeric(data[VICTIMS_COL], errors="coerce").fillna(0)
        data[VICTIMS_COL] = victims
        data[TARGET_COL] = (victims > 1).astype(int)
    return data


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    data = clean_column_names(df)
    data = drop_sparse_columns(data)
    data = normalize_text_values(data)
    data = impute_region_from_department(data)
    data = fix_date_columns(data)
    data = add_coordinates(data)
    data = add_decade(data)
    data = add_total_hechos(data)
    data = add_target(data)
    return data
