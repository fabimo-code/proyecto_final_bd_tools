# Extensión Big Data Tools

Esta extensión agrega una versión más completa del proyecto con:

- Docker Compose
- PostgreSQL + PostGIS
- MongoDB
- Prefect
- GeoPandas
- Pipeline modular en `src/bdtools`

## Ejecución rápida

1. Instalar dependencias extra:

```bash
conda activate proyectofinalbdtools
conda install -c conda-forge geopandas shapely pyarrow sqlalchemy psycopg2 pymongo python-dotenv -y
pip install prefect
```

2. Copiar `.env.example` como `.env`.

3. Instalar el proyecto como paquete editable:

```bash
pip install -e .
```

4. Levantar bases de datos:

```bash
docker compose up -d
```

5. Ejecutar pipeline sin bases de datos:

```bash
python -m flows.pipeline
```

6. Ejecutar pipeline con carga en PostgreSQL/PostGIS y MongoDB:

```bash
python -c "from flows.pipeline import sievcac_flow; sievcac_flow(load_databases=True)"
```

## Salidas

- `data/processed/sievcac_limpio.csv`
- `data/processed/sievcac_limpio.parquet`
- `data/processed/sievcac_geo.geojson`
- `reports/figures/*.png`
- `reports/tables/*.csv`
- tabla PostgreSQL: `sievcac_clean`
- colección MongoDB: `sievcac.casos`

## Verificación PostgreSQL

```sql
SELECT COUNT(*) FROM sievcac_clean;
SELECT COUNT(*) FROM sievcac_clean WHERE geom IS NOT NULL;
SELECT departamento, COUNT(*) AS casos
FROM sievcac_clean
GROUP BY departamento
ORDER BY casos DESC
LIMIT 10;
```

## Verificación MongoDB

```javascript
use sievcac
db.casos.countDocuments()
db.casos.findOne()
```
