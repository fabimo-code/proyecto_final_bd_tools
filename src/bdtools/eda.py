from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from bdtools.config import PATHS, ProjectPaths, ensure_directories


def save_table(df: pd.DataFrame, filename: str, paths: ProjectPaths = PATHS) -> None:
    ensure_directories(paths)
    df.to_csv(paths.tables / filename, index=False, encoding="utf-8-sig")


def barplot_counts(series: pd.Series, title: str, xlabel: str, ylabel: str, output_path) -> None:
    plt.figure(figsize=(11, 6))
    series.plot(kind="bar")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def run_eda(df: pd.DataFrame, paths: ProjectPaths = PATHS) -> dict[str, pd.DataFrame]:
    ensure_directories(paths)

    quality = pd.DataFrame({
        "columna": df.columns,
        "tipo": [str(df[col].dtype) for col in df.columns],
        "nulos": [int(df[col].isna().sum()) for col in df.columns],
        "porcentaje_nulos": [round(df[col].isna().mean() * 100, 2) for col in df.columns],
        "valores_unicos": [int(df[col].nunique(dropna=True)) for col in df.columns],
    })
    save_table(quality, "calidad_datos.csv", paths)

    resumen = pd.DataFrame({
        "indicador": [
            "registros",
            "columnas",
            "casos_alto_impacto",
            "porcentaje_alto_impacto",
            "anio_minimo",
            "anio_maximo",
        ],
        "valor": [
            len(df),
            df.shape[1],
            int(df.get("alto_impacto", pd.Series(dtype=int)).sum()) if "alto_impacto" in df.columns else None,
            round(df["alto_impacto"].mean() * 100, 2) if "alto_impacto" in df.columns else None,
            int(df["anio"].min()) if "anio" in df.columns and df["anio"].notna().any() else None,
            int(df["anio"].max()) if "anio" in df.columns and df["anio"].notna().any() else None,
        ],
    })
    save_table(resumen, "resumen_general.csv", paths)

    outputs: dict[str, pd.DataFrame] = {
        "calidad": quality,
        "resumen": resumen,
    }

    if "departamento" in df.columns:
        tabla_departamento = (
            df.groupby("departamento", dropna=False)
            .agg(
                casos=("departamento", "size"),
                victimas=("total_de_victimas_del_caso", "sum") if "total_de_victimas_del_caso" in df.columns else ("departamento", "size"),
                casos_alto_impacto=("alto_impacto", "sum") if "alto_impacto" in df.columns else ("departamento", "size"),
            )
            .reset_index()
            .sort_values("casos", ascending=False)
        )
        save_table(tabla_departamento, "tabla_departamento.csv", paths)
        outputs["departamento"] = tabla_departamento

        top = df["departamento"].value_counts().head(15)
        barplot_counts(
            top,
            "Top 15 departamentos por número de casos",
            "Departamento",
            "Casos",
            paths.figures / "top_departamentos.png",
        )

    if "anio" in df.columns:
        tabla_anio = (
            df.dropna(subset=["anio"])
            .groupby("anio")
            .size()
            .reset_index(name="casos")
            .sort_values("anio")
        )
        save_table(tabla_anio, "tabla_anio.csv", paths)
        outputs["anio"] = tabla_anio

        plt.figure(figsize=(11, 5))
        sns.lineplot(data=tabla_anio, x="anio", y="casos", marker="o")
        plt.title("Casos registrados por año")
        plt.xlabel("Año")
        plt.ylabel("Casos")
        plt.tight_layout()
        plt.savefig(paths.figures / "casos_por_anio.png", dpi=150)
        plt.close()

    if "modalidad" in df.columns:
        top = df["modalidad"].value_counts().head(10)
        barplot_counts(
            top,
            "Principales modalidades registradas",
            "Modalidad",
            "Casos",
            paths.figures / "modalidad_casos.png",
        )

    if "presunto_responsable" in df.columns:
        top = df["presunto_responsable"].value_counts().head(10)
        barplot_counts(
            top,
            "Principales presuntos responsables registrados",
            "Presunto responsable",
            "Casos",
            paths.figures / "presunto_responsable.png",
        )

    if {"longitud", "latitud"}.issubset(df.columns):
        geo_df = df.dropna(subset=["longitud", "latitud"])
        if not geo_df.empty:
            plt.figure(figsize=(8, 8))
            sns.scatterplot(data=geo_df, x="longitud", y="latitud", alpha=0.4, s=12)
            plt.title("Distribución geográfica aproximada de los casos")
            plt.xlabel("Longitud")
            plt.ylabel("Latitud")
            plt.tight_layout()
            plt.savefig(paths.figures / "distribucion_geografica.png", dpi=150)
            plt.close()

    return outputs
