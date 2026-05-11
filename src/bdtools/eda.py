import matplotlib.pyplot as plt
import pandas as pd

from bdtools.config import (
    EDA_COLUMNS,
    FIG_CASOS_ANIO,
    FIG_MODALIDAD,
    FIG_RESPONSABLE,
    FIG_TOP_DEPARTAMENTOS,
    SUMMARY_TABLE,
    TABLES_DIR,
    TOP_N,
    VICTIMS_COL,
)


def frequency_table(df: pd.DataFrame, column: str, top_n: int | None = None) -> pd.DataFrame:
    if column not in df.columns:
        return pd.DataFrame(columns=[column, "casos", "porcentaje"])

    counts = df[column].fillna("SIN INFORMACION").value_counts(dropna=False)
    if top_n:
        counts = counts.head(top_n)

    table = counts.rename_axis(column).reset_index(name="casos")
    table["porcentaje"] = (table["casos"] / len(df) * 100).round(2) if len(df) else 0
    return table


def build_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {"indicador": "registros", "valor": len(df)},
        {"indicador": "columnas", "valor": df.shape[1]},
        {"indicador": "duplicados", "valor": int(df.duplicated().sum())},
    ]

    if VICTIMS_COL in df.columns:
        victims = pd.to_numeric(df[VICTIMS_COL], errors="coerce")
        rows.extend(
            [
                {"indicador": "victimas_total", "valor": float(victims.sum())},
                {"indicador": "victimas_promedio", "valor": round(float(victims.mean()), 2)},
                {"indicador": "victimas_mediana", "valor": round(float(victims.median()), 2)},
            ]
        )

    for column in EDA_COLUMNS:
        if column in df.columns:
            rows.append({"indicador": f"{column}_categorias", "valor": int(df[column].nunique(dropna=True))})

    return pd.DataFrame(rows)


def save_summary_table(df: pd.DataFrame, output_path=SUMMARY_TABLE) -> pd.DataFrame:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    table = build_summary_table(df)
    table.to_csv(output_path, index=False)
    return table


def _bar_plot(table: pd.DataFrame, x_col: str, y_col: str, title: str, output_path, horizontal: bool = False) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plot_data = table.copy()

    fig, ax = plt.subplots(figsize=(10, 6))
    if horizontal:
        plot_data = plot_data.sort_values(y_col)
        ax.barh(plot_data[x_col].astype(str), plot_data[y_col])
        ax.set_xlabel("Casos")
        ax.set_ylabel("")
    else:
        ax.bar(plot_data[x_col].astype(str), plot_data[y_col])
        ax.set_xlabel("")
        ax.set_ylabel("Casos")
        ax.tick_params(axis="x", rotation=45)

    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_cases_by_year(df: pd.DataFrame, output_path=FIG_CASOS_ANIO) -> pd.DataFrame:
    if "anio_valido" not in df.columns:
        return pd.DataFrame(columns=["anio_valido", "casos"])

    table = (
        df.dropna(subset=["anio_valido"])
        .assign(anio_valido=lambda data: data["anio_valido"].astype(int))
        .groupby("anio_valido", as_index=False)
        .size()
        .rename(columns={"size": "casos"})
        .sort_values("anio_valido")
    )
    _bar_plot(table, "anio_valido", "casos", "Casos por año", output_path)
    return table


def plot_top_departments(df: pd.DataFrame, output_path=FIG_TOP_DEPARTAMENTOS, top_n: int = TOP_N) -> pd.DataFrame:
    table = frequency_table(df, "departamento", top_n=top_n)
    _bar_plot(table, "departamento", "casos", "Departamentos con más casos", output_path, horizontal=True)
    return table


def plot_modality_cases(df: pd.DataFrame, output_path=FIG_MODALIDAD, top_n: int = TOP_N) -> pd.DataFrame:
    table = frequency_table(df, "modalidad", top_n=top_n)
    _bar_plot(table, "modalidad", "casos", "Casos por modalidad", output_path, horizontal=True)
    return table


def plot_presumed_responsible(df: pd.DataFrame, output_path=FIG_RESPONSABLE, top_n: int = TOP_N) -> pd.DataFrame:
    table = frequency_table(df, "presunto_responsable", top_n=top_n)
    _bar_plot(table, "presunto_responsable", "casos", "Casos por presunto responsable", output_path, horizontal=True)
    return table


def build_eda_reports(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    outputs = {
        "resumen_general": save_summary_table(df),
        "casos_por_anio": plot_cases_by_year(df),
        "top_departamentos": plot_top_departments(df),
        "modalidad_casos": plot_modality_cases(df),
        "presunto_responsable": plot_presumed_responsible(df),
    }
    return outputs
