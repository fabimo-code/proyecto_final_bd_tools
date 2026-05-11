from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

from bdtools.config import PATHS


def proportion_ci(successes, n, z=1.96):
    if n == 0:
        return np.nan, np.nan

    p = successes / n
    se = np.sqrt((p * (1 - p)) / n)

    return max(0, p - z * se), min(1, p + z * se)


def categorical_chi_square(df, target, variables):
    rows = []

    for var in variables:
        if var not in df.columns or target not in df.columns:
            continue

        subset = df[[var, target]].dropna()

        if subset[var].nunique() < 2 or subset[target].nunique() < 2:
            continue

        table = pd.crosstab(subset[var], subset[target])
        chi2, p_value, dof, expected = chi2_contingency(table)

        rows.append({
            "variable": var,
            "chi2": chi2,
            "p_value": p_value,
            "dof": dof,
            "significativa_005": p_value < 0.05
        })

    return pd.DataFrame(rows).sort_values("p_value")


def descriptive_summary(df):
    rows = []

    rows.append({"indicador": "registros", "valor": len(df)})
    rows.append({"indicador": "columnas", "valor": df.shape[1]})

    if "alto_impacto" in df.columns:
        n = len(df)
        successes = int(df["alto_impacto"].sum())
        low, high = proportion_ci(successes, n)

        rows.extend([
            {"indicador": "casos_alto_impacto", "valor": successes},
            {"indicador": "proporcion_alto_impacto", "valor": successes / n},
            {"indicador": "ic95_alto_impacto_inf", "valor": low},
            {"indicador": "ic95_alto_impacto_sup", "valor": high},
        ])

    if "anio" in df.columns:
        valid_year = df.loc[df["anio"] > 0, "anio"]
        rows.extend([
            {"indicador": "anio_min", "valor": valid_year.min()},
            {"indicador": "anio_max", "valor": valid_year.max()},
            {"indicador": "anio_mediana", "valor": valid_year.median()},
        ])

    return pd.DataFrame(rows)


def run_statistics(df):
    PATHS.tables.mkdir(parents=True, exist_ok=True)

    descriptive = descriptive_summary(df)

    variables = [
        "departamento",
        "region",
        "modalidad",
        "presunto_responsable",
        "forma_de_vinculacion",
        "tipo_de_vinculacion",
    ]

    chi_square = categorical_chi_square(
        df=df,
        target="alto_impacto",
        variables=variables
    )

    descriptive_path = PATHS.tables / "estadistica_descriptiva.csv"
    chi_square_path = PATHS.tables / "pruebas_chi_cuadrado.csv"

    descriptive.to_csv(descriptive_path, index=False, encoding="utf-8")
    chi_square.to_csv(chi_square_path, index=False, encoding="utf-8")

    return {
        "descriptive": descriptive,
        "chi_square": chi_square,
        "descriptive_path": descriptive_path,
        "chi_square_path": chi_square_path,
    }