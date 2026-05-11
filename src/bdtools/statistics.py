import math

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

from bdtools.config import CHI2_TABLE, CHI2_VARIABLES, DESCRIPTIVE_TABLE, TARGET_COL, TABLES_DIR, VICTIMS_COL


def numeric_summary(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    selected = columns or df.select_dtypes(include="number").columns.tolist()
    selected = [column for column in selected if column in df.columns]

    rows = []
    for column in selected:
        values = pd.to_numeric(df[column], errors="coerce").dropna()
        if values.empty:
            continue
        rows.append(
            {
                "variable": column,
                "tipo": "numerica",
                "n": int(values.size),
                "media": round(float(values.mean()), 3),
                "mediana": round(float(values.median()), 3),
                "desviacion": round(float(values.std()), 3),
                "minimo": round(float(values.min()), 3),
                "maximo": round(float(values.max()), 3),
            }
        )
    return pd.DataFrame(rows)


def categorical_summary(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for column in columns:
        if column not in df.columns:
            continue
        counts = df[column].fillna("SIN INFORMACION").value_counts(dropna=False)
        for category, count in counts.items():
            rows.append(
                {
                    "variable": column,
                    "categoria": category,
                    "casos": int(count),
                    "porcentaje": round(float(count / len(df) * 100), 2) if len(df) else 0,
                }
            )
    return pd.DataFrame(rows)


def wilson_interval(successes: int, total: int, confidence: float = 0.95) -> tuple[float, float]:
    if total == 0:
        return np.nan, np.nan

    z = 1.959963984540054 if confidence == 0.95 else 1.959963984540054
    p = successes / total
    denominator = 1 + z**2 / total
    center = (p + z**2 / (2 * total)) / denominator
    margin = z * math.sqrt((p * (1 - p) + z**2 / (4 * total)) / total) / denominator
    return round(center - margin, 4), round(center + margin, 4)


def proportion_summary(df: pd.DataFrame, target_col: str = TARGET_COL) -> pd.DataFrame:
    if target_col not in df.columns:
        return pd.DataFrame(columns=["variable", "casos", "total", "proporcion", "ic_95_inf", "ic_95_sup"])

    target = pd.to_numeric(df[target_col], errors="coerce").dropna().astype(int)
    total = int(target.size)
    successes = int(target.sum())
    lower, upper = wilson_interval(successes, total)

    return pd.DataFrame(
        [
            {
                "variable": target_col,
                "casos": successes,
                "total": total,
                "proporcion": round(successes / total, 4) if total else np.nan,
                "ic_95_inf": lower,
                "ic_95_sup": upper,
            }
        ]
    )


def build_descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = [
        column
        for column in ["anio_valido", "mes_valido", "dia_valido", VICTIMS_COL, "total_hechos", "latitud", "longitud"]
        if column in df.columns
    ]
    numeric = numeric_summary(df, numeric_cols)
    proportions = proportion_summary(df)

    if proportions.empty:
        return numeric

    proportions = proportions.rename(
        columns={
            "casos": "n",
            "proporcion": "media",
            "ic_95_inf": "minimo",
            "ic_95_sup": "maximo",
        }
    )
    proportions["tipo"] = "proporcion"
    proportions["mediana"] = np.nan
    proportions["desviacion"] = np.nan
    return pd.concat([numeric, proportions[numeric.columns]], ignore_index=True)


def save_descriptive_statistics(df: pd.DataFrame, output_path=DESCRIPTIVE_TABLE) -> pd.DataFrame:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    table = build_descriptive_statistics(df)
    table.to_csv(output_path, index=False)
    return table


def chi_square_tests(df: pd.DataFrame, variables: list[str] | None = None, target_col: str = TARGET_COL) -> pd.DataFrame:
    selected = variables or CHI2_VARIABLES
    if target_col not in df.columns:
        return pd.DataFrame(columns=["variable", "chi2", "p_valor", "grados_libertad", "n", "decision"])

    rows = []
    for variable in selected:
        if variable not in df.columns:
            continue

        subset = df[[variable, target_col]].dropna()
        if subset[variable].nunique() < 2 or subset[target_col].nunique() < 2:
            continue

        contingency = pd.crosstab(subset[variable], subset[target_col])
        if contingency.shape[0] < 2 or contingency.shape[1] < 2:
            continue

        chi2, p_value, dof, _ = chi2_contingency(contingency)
        rows.append(
            {
                "variable": variable,
                "chi2": round(float(chi2), 4),
                "p_valor": round(float(p_value), 6),
                "grados_libertad": int(dof),
                "n": int(contingency.to_numpy().sum()),
                "decision": "asociacion" if p_value < 0.05 else "sin_evidencia",
            }
        )

    return pd.DataFrame(rows).sort_values("p_valor").reset_index(drop=True) if rows else pd.DataFrame(rows)


def save_chi_square_tests(df: pd.DataFrame, output_path=CHI2_TABLE) -> pd.DataFrame:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    table = chi_square_tests(df)
    table.to_csv(output_path, index=False)
    return table


def build_statistics_reports(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        "estadistica_descriptiva": save_descriptive_statistics(df),
        "pruebas_chi_cuadrado": save_chi_square_tests(df),
    }
