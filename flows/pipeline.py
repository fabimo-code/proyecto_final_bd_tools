from __future__ import annotations

from prefect import flow, task

from bdtools.databases import postgres_summary, write_mongo, write_postgres
from bdtools.eda import run_eda
from bdtools.geo import export_geojson
from bdtools.io import run_etl
from bdtools.modeling import train_high_impact_classifier


@task(retries=1, retry_delay_seconds=5)
def task_etl():
    return run_etl()


@task
def task_eda(df):
    return run_eda(df)


@task
def task_geo(df):
    return export_geojson(df)


@task
def task_model(df):
    return train_high_impact_classifier(df)


@task(retries=2, retry_delay_seconds=5)
def task_load_postgres(df):
    write_postgres(df)
    return postgres_summary()

@task
def task_statistics(df):
    return run_statistics(df)

@task(retries=2, retry_delay_seconds=5)
def task_load_mongo(df):
    write_mongo(df)
    return "Carga MongoDB completada"


@flow
def sievcac_flow(load_databases=False):
    df = task_etl()

    eda_outputs = task_eda(df)
    stats_outputs = task_statistics(df)
    geo_output = task_geo(df)
    model_outputs = task_model(df)

    if load_databases:
        task_load_postgres(df)
        task_load_mongo(df)

    return {
        "eda": eda_outputs,
        "statistics": stats_outputs,
        "geo": geo_output,
        "modeling": model_outputs,
    }


if __name__ == "__main__":
    sievcac_flow(load_databases=False)
