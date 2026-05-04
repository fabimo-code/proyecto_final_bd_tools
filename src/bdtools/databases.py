from __future__ import annotations

import math

import pandas as pd
from sqlalchemy import create_engine, text

from bdtools.config import DB, DatabaseConfig


def get_postgres_engine(db: DatabaseConfig = DB):
    return create_engine(db.postgres_url)


def write_postgres(df: pd.DataFrame, table_name: str = "sievcac_clean", db: DatabaseConfig = DB) -> None:
    """Carga el dataset limpio en PostgreSQL y crea una columna geométrica PostGIS."""
    engine = get_postgres_engine(db)

    df_to_write = df.copy()
    if "geometry" in df_to_write.columns:
        df_to_write = df_to_write.drop(columns=["geometry"])

    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))

    df_to_write.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi",
    )

    if {"longitud", "latitud"}.issubset(df_to_write.columns):
        with engine.begin() as conn:
            conn.execute(text(f'ALTER TABLE "{table_name}" ADD COLUMN IF NOT EXISTS geom geometry(Point, 4326);'))
            conn.execute(text(
                f"""
                UPDATE "{table_name}"
                SET geom = ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)
                WHERE longitud IS NOT NULL AND latitud IS NOT NULL;
                """
            ))
            conn.execute(text(f'CREATE INDEX IF NOT EXISTS idx_{table_name}_geom ON "{table_name}" USING GIST (geom);'))


def write_mongo(df: pd.DataFrame, db: DatabaseConfig = DB) -> None:
    """Carga el dataset limpio en MongoDB. Si existen coordenadas, agrega campo GeoJSON."""
    try:
        from pymongo import MongoClient
    except ImportError as exc:
        raise ImportError("pymongo no está instalado. Instala con: pip install pymongo") from exc

    client = MongoClient(db.mongo_uri)
    database = client[db.mongo_db]
    collection = database[db.mongo_collection]

    records = df.where(pd.notnull(df), None).to_dict(orient="records")

    for record in records:
        lon = record.get("longitud")
        lat = record.get("latitud")
        if lon is not None and lat is not None:
            record["geometry"] = {
                "type": "Point",
                "coordinates": [lon, lat],
            }

    collection.delete_many({})
    if records:
        collection.insert_many(records)

    collection.create_index([("geometry", "2dsphere")])


def postgres_summary(db: DatabaseConfig = DB, table_name: str = "sievcac_clean") -> pd.DataFrame:
    engine = get_postgres_engine(db)
    query = f"""
    SELECT
        COUNT(*) AS registros,
        COUNT(geom) AS registros_con_geometria,
        MIN(anio) AS anio_minimo,
        MAX(anio) AS anio_maximo,
        SUM(alto_impacto) AS casos_alto_impacto
    FROM "{table_name}";
    """
    return pd.read_sql_query(query, engine)
