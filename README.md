# Proyecto Final Big Data Tools

Dataset: SIEVCAC - Casos RU Reclutamiento y Utilización de Niños, Niñas y Adolescentes.

## Pregunta investigativa propuesta

¿Cómo se distribuyen espacial y temporalmente los casos de reclutamiento y utilización de NNA en Colombia, y qué patrones de modalidad, presunto responsable, territorio y hechos simultáneos permiten priorizar zonas con mayor probabilidad de casos de alto impacto?

## Objetivo técnico inicial

Construir un pipeline reproducible de Big Data Tools que:

1. Ingiere el CSV original.
2. Limpia variables críticas, especialmente año, fecha aproximada y coordenadas.
3. Exporta una capa procesada en Parquet/CSV.
4. Genera EDA, tablas y visualizaciones georreferenciadas.
5. Entrena un modelo inicial de clasificación de casos de alto impacto.
6. Ejecuta clustering espacial con DBSCAN.
7. Permite cargar datos a PostgreSQL/PostGIS y MongoDB si se desea demostrar componentes vistos en clase.

## Crear ambiente y kernel

```bash
conda env create -f environment.yml
conda activate proyectofinalbdtools
python -m ipykernel install --user --name proyectofinalbdtools --display-name "Python (proyectofinalbdtools)"
jupyter lab
```

En Jupyter, selecciona el kernel: `Python (proyectofinalbdtools)`.

## Ejecutar pipeline básico sin Prefect

```bash
set PYTHONPATH=src   # Windows CMD
# o
export PYTHONPATH=src  # macOS/Linux

python -c "from bdtools.io import run_etl; df, quality = run_etl(); print(df.shape); print(quality.head())"
```

## Ejecutar Prefect

```bash
set PYTHONPATH=src
python flows/pipeline_prefect.py
```

## Docker opcional

```bash
docker compose up -d
```

Esto levanta PostgreSQL/PostGIS y MongoDB para extender el proyecto con persistencia relacional y NoSQL.
