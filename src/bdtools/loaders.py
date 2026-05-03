import os

import pandas as pd
from sqlalchemy import create_engine


def postgres_url_from_env() -> str:
    user = os.getenv("POSTGRES_USER", "bdtools")
    password = os.getenv("POSTGRES_PASSWORD", "bdtools")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "bdtools")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def load_to_postgres(df: pd.DataFrame, table_name: str = "sievcac_clean") -> None:
    """
    Carga tabular a PostgreSQL. Para PostGIS se puede extender creando geometría POINT
    desde longitud/latitud con ST_SetSRID(ST_MakePoint(longitud, latitud), 4326).
    """
    engine = create_engine(postgres_url_from_env())
    df.to_sql(table_name, engine, if_exists="replace", index=False, chunksize=2000)


def load_to_mongo(df: pd.DataFrame, collection_name: str = "casos_sievcac") -> None:
    """Carga documentos a MongoDB."""
    from pymongo import MongoClient

    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB", "bdtools")
    client = MongoClient(uri)
    collection = client[db_name][collection_name]

    records = df.where(pd.notna(df), None).to_dict(orient="records")
    collection.delete_many({})
    if records:
        collection.insert_many(records)
