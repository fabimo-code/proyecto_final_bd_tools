from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .config import PATHS


def save_top_tables(df: pd.DataFrame) -> None:
    PATHS.tables_dir.mkdir(parents=True, exist_ok=True)

    for col in ["departamento", "region", "municipio", "modalidad", "presunto_responsable", "tipo_de_vinculacion"]:
        if col in df.columns:
            table = df[col].value_counts(dropna=False).rename_axis(col).reset_index(name="casos")
            table.to_csv(PATHS.tables_dir / f"top_{col}.csv", index=False, encoding="utf-8")


def plot_cases_by_year(df: pd.DataFrame) -> Path:
    PATHS.figures_dir.mkdir(parents=True, exist_ok=True)
    yearly = (
        df.dropna(subset=["anio"])
        .groupby("anio", as_index=False)
        .agg(casos=("id_caso", "count"), victimas=("total_de_victimas_del_caso", "sum"))
        .sort_values("anio")
    )

    fig_path = PATHS.figures_dir / "casos_victimas_por_anio.png"
    plt.figure(figsize=(11, 5))
    plt.plot(yearly["anio"], yearly["casos"], marker="o", label="Casos")
    plt.plot(yearly["anio"], yearly["victimas"], marker="o", label="Víctimas")
    plt.xlabel("Año")
    plt.ylabel("Conteo")
    plt.title("Casos y víctimas por año")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_path, dpi=180)
    plt.close()
    return fig_path


def plot_top_departments(df: pd.DataFrame, n: int = 15) -> Path:
    PATHS.figures_dir.mkdir(parents=True, exist_ok=True)

    top = (
        df.groupby("departamento", as_index=False)
        .agg(casos=("id_caso", "count"), victimas=("total_de_victimas_del_caso", "sum"))
        .sort_values("casos", ascending=False)
        .head(n)
        .sort_values("casos")
    )

    fig_path = PATHS.figures_dir / "top_departamentos_casos.png"
    plt.figure(figsize=(10, 7))
    plt.barh(top["departamento"], top["casos"])
    plt.xlabel("Casos")
    plt.ylabel("Departamento")
    plt.title(f"Top {n} departamentos por número de casos")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=180)
    plt.close()
    return fig_path


def make_folium_map(df: pd.DataFrame, sample: int = 3000) -> Path:
    """
    Crea mapa HTML exploratorio. Usa muestra para evitar mapas pesados.
    """
    import folium

    geo = df.dropna(subset=["latitud", "longitud"]).copy()
    if len(geo) > sample:
        geo = geo.sample(sample, random_state=42)

    m = folium.Map(location=[4.6, -74.1], zoom_start=5, tiles="CartoDB positron")
    for _, row in geo.iterrows():
        folium.CircleMarker(
            location=[row["latitud"], row["longitud"]],
            radius=2 + min(float(row.get("total_de_victimas_del_caso", 1)), 10) * 0.2,
            fill=True,
            fill_opacity=0.65,
            popup=(
                f"Departamento: {row.get('departamento')}<br>"
                f"Municipio: {row.get('municipio')}<br>"
                f"Año: {row.get('anio')}<br>"
                f"Responsable: {row.get('presunto_responsable')}<br>"
                f"Víctimas: {row.get('total_de_victimas_del_caso')}"
            ),
        ).add_to(m)

    out = PATHS.figures_dir / "mapa_casos_sievcac.html"
    m.save(out)
    return out


def run_eda(df: pd.DataFrame) -> list[Path]:
    save_top_tables(df)
    outputs = [plot_cases_by_year(df), plot_top_departments(df), make_folium_map(df)]
    return outputs
