from __future__ import annotations

import pandas as pd

from bdtools.config import PATHS, ProjectPaths, ensure_directories


def make_geodataframe(df: pd.DataFrame):
    """Crea un GeoDataFrame con geometría POINT a partir de longitud y latitud."""
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "GeoPandas no está instalado. Instala con: "
            "conda install -c conda-forge geopandas"
        ) from exc

    if not {"longitud", "latitud"}.issubset(df.columns):
        raise ValueError("El DataFrame debe tener columnas longitud y latitud.")

    geo_df = df.dropna(subset=["longitud", "latitud"]).copy()
    geo_df = gpd.GeoDataFrame(
        geo_df,
        geometry=gpd.points_from_xy(geo_df["longitud"], geo_df["latitud"]),
        crs="EPSG:4326",
    )
    return geo_df


def export_geojson(df: pd.DataFrame, paths: ProjectPaths = PATHS):
    ensure_directories(paths)
    geo_df = make_geodataframe(df)
    geo_df.to_file(paths.geojson, driver="GeoJSON")
    return geo_df
