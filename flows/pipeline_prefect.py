from pathlib import Path

from prefect import flow, task

from bdtools.config import PATHS
from bdtools.eda import run_eda
from bdtools.io import run_etl
from bdtools.modeling import run_spatial_clustering, train_high_impact_classifier


@task(name="ETL SIEVCAC")
def etl_task():
    df, quality = run_etl(PATHS.raw_csv)
    return df, quality


@task(name="EDA")
def eda_task(df):
    return run_eda(df)


@task(name="Modelamiento inicial")
def model_task(df):
    model, metrics = train_high_impact_classifier(df)
    clusters = run_spatial_clustering(df)
    return metrics, clusters


@flow(name="pipeline-proyecto-final-bdtools")
def main_flow():
    df, quality = etl_task()
    figures = eda_task(df)
    metrics, clusters = model_task(df)
    return {
        "registros_limpios": len(df),
        "figuras": [str(p) for p in figures],
        "metricas": metrics.to_dict(orient="records"),
        "clusters_principales": clusters.head(10).to_dict(orient="records"),
    }


if __name__ == "__main__":
    main_flow()
