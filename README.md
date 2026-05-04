Claro. Te dejo un **README final unificado**, pensado para reemplazar tu `README.md` actual. Incluye el proyecto sencillo, la extensión Big Data, Docker, Prefect, MongoDB, PostgreSQL/PostGIS, GeoPandas, ejecución, estructura y solución de errores comunes.

GitHub recomienda que cada repositorio tenga un README para explicar qué hace el proyecto, por qué es útil y cómo usarlo. Docker Compose permite levantar servicios en segundo plano con `docker compose up -d`; Prefect organiza procesos en `flows` y `tasks`; GeoPandas extiende pandas para datos geoespaciales; y PostGIS permite trabajar con geometrías espaciales en PostgreSQL, incluyendo coordenadas EPSG:4326. ([GitHub Docs][1])

Copia esto completo en tu `README.md`:

````md
# Proyecto Final - Big Data Tools

## Análisis de casos de reclutamiento y utilización de niños, niñas y adolescentes en el conflicto armado colombiano

Este repositorio contiene el desarrollo técnico del proyecto final de la asignatura **Herramientas de Big Data**. El proyecto analiza información del **Sistema de Información de Eventos de Violencia del Conflicto Armado - SIEVCAC**, específicamente los casos RU asociados al **reclutamiento y utilización de niños, niñas y adolescentes** en Colombia.

El proyecto combina una versión analítica inicial en notebook con una extensión de herramientas Big Data que incorpora pipeline modular, orquestación, contenedores, persistencia relacional, persistencia NoSQL y análisis geoespacial.

---

## Pregunta de investigación

¿Cómo se distribuyen temporal, territorial y categóricamente los casos de reclutamiento y utilización de niños, niñas y adolescentes en Colombia, y qué variables permiten identificar casos de mayor impacto dentro del conjunto de datos?

---

## Objetivo general

Analizar patrones históricos, geográficos y descriptivos de los casos registrados de reclutamiento y utilización de niños, niñas y adolescentes en el marco del conflicto armado colombiano, mediante técnicas de limpieza, análisis exploratorio, visualización, modelado predictivo básico, procesamiento geoespacial y almacenamiento en bases de datos relacionales y NoSQL.

---

## Objetivos específicos

- Cargar y limpiar el dataset original del SIEVCAC.
- Estandarizar variables temporales, categóricas y geográficas.
- Analizar la distribución de los casos por año, departamento, región, modalidad y presunto responsable.
- Generar visualizaciones descriptivas para apoyar la interpretación del fenómeno.
- Construir una variable objetivo denominada `alto_impacto`.
- Entrenar un modelo de clasificación inicial para identificar casos de mayor impacto.
- Exportar datos procesados en formatos CSV, Parquet y GeoJSON.
- Orquestar el flujo de procesamiento mediante Prefect.
- Persistir los datos procesados en PostgreSQL/PostGIS y MongoDB.
- Contenerizar los servicios de base de datos mediante Docker Compose.

---

## Fuente de datos

- **Nombre del conjunto:** Sistema de Información de Eventos de Violencia del Conflicto Armado SIEVCAC - Casos RU Reclutamiento y Utilización de Niños, Niñas y Adolescentes.
- **Entidad:** Centro Nacional de Memoria Histórica.
- **Dependencia:** Observatorio de Memoria y Conflicto.
- **Sector:** Inclusión Social y Reconciliación.
- **Cobertura geográfica:** Nacional.
- **Idioma:** Español.
- **Frecuencia de actualización:** Semestral.
- **Última actualización reportada:** 19 de diciembre de 2025.
- **Última actualización de datos:** 27 de febrero de 2025.

---

## Alcance del proyecto

El proyecto tiene un enfoque académico, exploratorio y técnico. No busca realizar afirmaciones causales sobre el fenómeno, sino demostrar el uso de herramientas de análisis de datos y Big Data para procesar, estructurar, visualizar y almacenar información sensible relacionada con el conflicto armado colombiano.

---

## Tecnologías utilizadas

### Lenguaje y análisis de datos

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn

### Big Data Tools

- Docker
- Docker Compose
- Prefect
- PostgreSQL
- PostGIS
- MongoDB
- GeoPandas
- SQLAlchemy
- PyMongo

### Entorno de desarrollo

- Visual Studio Code
- Anaconda / Conda
- Jupyter Notebook
- Git
- GitHub

---

## Estructura del repositorio

```text
.
├── data/
│   ├── raw/
│   │   └── dataset_original.csv
│   └── processed/
│       ├── sievcac_limpio.csv
│       ├── sievcac_limpio.parquet
│       └── sievcac_geo.geojson
│
├── flows/
│   ├── __init__.py
│   └── pipeline.py
│
├── notebooks/
│   ├── 01_proyecto_final_bdtools_CORREGIDO.ipynb
│   └── 02_pipeline_big_data_tools_CORREGIDO.ipynb
│
├── reports/
│   ├── figures/
│   │   ├── top_departamentos.png
│   │   ├── casos_por_anio.png
│   │   ├── modalidad_casos.png
│   │   ├── presunto_responsable.png
│   │   ├── distribucion_geografica.png
│   │   └── matriz_confusion.png
│   │
│   └── tables/
│       ├── calidad_datos_inicial.csv
│       ├── resumen_general.csv
│       ├── tabla_departamento.csv
│       ├── tabla_anio.csv
│       ├── classification_report.json
│       └── classification_report.txt
│
├── scripts/
│   └── run_pipeline.py
│
├── sql/
│   └── init.sql
│
├── src/
│   └── bdtools/
│       ├── __init__.py
│       ├── config.py
│       ├── cleaning.py
│       ├── io.py
│       ├── eda.py
│       ├── geo.py
│       ├── databases.py
│       └── modeling.py
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── requirements_extra.txt
└── README.md
````

---

## Descripción de componentes

### `notebooks/01_proyecto_final_bdtools_CORREGIDO.ipynb`

Notebook principal de análisis. Incluye:

* Carga del CSV.
* Limpieza inicial.
* Análisis exploratorio.
* Visualizaciones.
* Construcción de la variable objetivo.
* Modelo predictivo básico.
* Exportación de tablas y figuras.

### `notebooks/02_pipeline_big_data_tools_CORREGIDO.ipynb`

Notebook técnico de extensión Big Data. Incluye:

* Validación del pipeline modular.
* Ejecución de ETL.
* Ejecución de EDA.
* Generación de GeoJSON con GeoPandas.
* Entrenamiento del modelo.
* Ejecución del flujo Prefect.
* Verificación de PostgreSQL/PostGIS.
* Verificación de MongoDB.

### `src/bdtools/`

Paquete local del proyecto. Contiene la lógica modular del pipeline:

* `config.py`: rutas y configuración general.
* `cleaning.py`: funciones de limpieza y transformación.
* `io.py`: lectura y escritura de archivos.
* `eda.py`: generación de tablas y visualizaciones.
* `geo.py`: construcción de datos geográficos y GeoJSON.
* `databases.py`: carga a PostgreSQL/PostGIS y MongoDB.
* `modeling.py`: entrenamiento y evaluación del modelo.

### `flows/pipeline.py`

Flujo principal de Prefect. Orquesta las tareas de:

1. ETL.
2. EDA.
3. Procesamiento geoespacial.
4. Modelado.
5. Carga a PostgreSQL/PostGIS.
6. Carga a MongoDB.
7. Consulta resumen desde PostgreSQL.

### `docker-compose.yml`

Archivo que levanta los servicios de base de datos:

* PostgreSQL/PostGIS.
* MongoDB.

---

## Variable objetivo

Se construyó la variable `alto_impacto` a partir del número total de víctimas registradas por caso.

La lógica general es:

```text
alto_impacto = 1 si el caso registra más de una víctima
alto_impacto = 0 si el caso registra una víctima o no supera el umbral definido
```

Esta variable permite formular un problema de clasificación supervisada para identificar registros con mayor impacto dentro del conjunto de datos.

---

## Variables usadas en el modelo

El modelo utiliza variables categóricas, temporales y descriptivas como:

```text
departamento
region
modalidad
presunto_responsable
forma_de_vinculacion
tipo_de_vinculacion
cantidad_hechos_simultaneos
anio
```

El modelo implementado es una clasificación inicial con preprocesamiento de variables categóricas mediante codificación y entrenamiento con Scikit-learn.

---

## Requisitos previos

Antes de ejecutar el proyecto se debe contar con:

* Anaconda o Miniconda instalado.
* Visual Studio Code.
* Docker Desktop.
* Git.
* Repositorio clonado localmente.

---

## Instalación del entorno

Crear o activar el ambiente:

```bash
conda activate proyectofinalbdtools
```

Instalar dependencias mínimas:

```bash
pip install -r requirements.txt
```

Instalar dependencias extra para la extensión Big Data:

```bash
pip install -r requirements_extra.txt
```

Si se requiere instalar GeoPandas con Conda:

```bash
conda install -n proyectofinalbdtools -c conda-forge geopandas -y
```

Instalar el proyecto local en modo editable:

```bash
conda run -n proyectofinalbdtools python -m pip install -e .
```

Este paso permite importar correctamente módulos como:

```python
from bdtools.io import run_etl
from flows.pipeline import sievcac_flow
```

---

## Configuración de variables de entorno

Crear un archivo `.env` a partir de `.env.example`.

Contenido recomendado:

```env
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
POSTGRES_DB=sievcac
POSTGRES_USER=bdtools
POSTGRES_PASSWORD=bdtools

MONGO_URI=mongodb://localhost:27017
MONGO_DB=sievcac
MONGO_COLLECTION=casos
```

Si no existe conflicto con otro PostgreSQL local, también puede usarse el puerto `5432`.

---

## Ejecución con notebook principal

Abrir en Visual Studio Code:

```text
notebooks/01_proyecto_final_bdtools_CORREGIDO.ipynb
```

Seleccionar kernel:

```text
Python (proyectofinalbdtools)
```

Ejecutar todas las celdas.

Este notebook genera:

```text
data/processed/sievcac_limpio.csv

reports/figures/top_departamentos.png
reports/figures/casos_por_anio.png
reports/figures/modalidad_casos.png
reports/figures/presunto_responsable.png
reports/figures/distribucion_geografica.png
reports/figures/matriz_confusion.png

reports/tables/calidad_datos_inicial.csv
reports/tables/resumen_general.csv
reports/tables/tabla_departamento.csv
reports/tables/tabla_anio.csv
```

---

## Ejecución del pipeline sin bases de datos

Desde la raíz del proyecto:

```bash
conda run -n proyectofinalbdtools python -m flows.pipeline
```

Esta ejecución realiza:

* ETL.
* EDA.
* Generación de GeoJSON.
* Entrenamiento del modelo.

No carga información a PostgreSQL ni MongoDB.

---

## Ejecución de Docker

Abrir Docker Desktop.

Luego, desde la raíz del proyecto:

```bash
docker compose up -d
```

Verificar servicios:

```bash
docker compose ps
```

Se deben ver los contenedores:

```text
sievcac_postgres
sievcac_mongo
```

Para detener servicios:

```bash
docker compose down
```

Para reiniciar eliminando volúmenes:

```bash
docker compose down -v
docker compose up -d
```

Nota: `docker compose down -v` elimina los datos persistidos en los volúmenes.

---

## Ejecución del pipeline con bases de datos

Con Docker corriendo:

```bash
conda run -n proyectofinalbdtools python -c "from flows.pipeline import sievcac_flow; sievcac_flow(load_databases=True)"
```

Esta ejecución realiza:

* ETL.
* EDA.
* Generación de GeoJSON.
* Entrenamiento del modelo.
* Carga a PostgreSQL/PostGIS.
* Carga a MongoDB.
* Consulta resumen desde PostgreSQL.

---

## Verificación de PostgreSQL/PostGIS

Entrar al contenedor:

```bash
docker exec -it sievcac_postgres psql -U bdtools -d sievcac
```

Listar tablas:

```sql
\dt
```

Contar registros:

```sql
SELECT COUNT(*) FROM sievcac_clean;
```

Consultar registros:

```sql
SELECT id, departamento, municipio, latitud, longitud
FROM sievcac_clean
LIMIT 5;
```

Consultar geometría espacial:

```sql
SELECT id, ST_AsText(geom)
FROM sievcac_clean
WHERE geom IS NOT NULL
LIMIT 5;
```

Salir:

```sql
\q
```

También se puede ejecutar directamente:

```bash
docker exec -it sievcac_postgres psql -U bdtools -d sievcac -c "SELECT COUNT(*) FROM sievcac_clean;"
```

---

## Verificación de MongoDB

Entrar al contenedor:

```bash
docker exec -it sievcac_mongo mongosh
```

Seleccionar base de datos:

```javascript
use sievcac
```

Listar colecciones:

```javascript
show collections
```

Contar documentos:

```javascript
db.casos.countDocuments()
```

Ver un documento de ejemplo:

```javascript
db.casos.findOne()
```

Salir:

```javascript
exit
```

También se puede ejecutar directamente:

```bash
docker exec -it sievcac_mongo mongosh --eval "use sievcac; db.casos.countDocuments();"
```

---

## Ejecución del notebook Big Data

Abrir en Visual Studio Code:

```text
notebooks/02_pipeline_big_data_tools_CORREGIDO.ipynb
```

Seleccionar kernel:

```text
Python (proyectofinalbdtools)
```

Ejecutar todas las celdas.

Si aparece un error como:

```text
ModuleNotFoundError: No module named 'flows'
```

asegurarse de que el notebook agregue al `sys.path` tanto la raíz del proyecto como la carpeta `src`:

```python
from pathlib import Path
import sys

current = Path.cwd().resolve()

PROJECT_ROOT = current
for parent in [current] + list(current.parents):
    if (parent / "docker-compose.yml").exists() and (parent / "src").exists():
        PROJECT_ROOT = parent
        break

SRC_PATH = PROJECT_ROOT / "src"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
```

También se recomienda crear un archivo vacío:

```text
flows/__init__.py
```

---

## Resultados esperados

Al ejecutar correctamente el proyecto se generan:

### Datos procesados

```text
data/processed/sievcac_limpio.csv
data/processed/sievcac_limpio.parquet
data/processed/sievcac_geo.geojson
```

### Figuras

```text
reports/figures/top_departamentos.png
reports/figures/casos_por_anio.png
reports/figures/modalidad_casos.png
reports/figures/presunto_responsable.png
reports/figures/distribucion_geografica.png
reports/figures/matriz_confusion.png
```

### Tablas

```text
reports/tables/calidad_datos_inicial.csv
reports/tables/resumen_general.csv
reports/tables/tabla_departamento.csv
reports/tables/tabla_anio.csv
reports/tables/classification_report.json
reports/tables/classification_report.txt
```

### Bases de datos

En PostgreSQL/PostGIS:

```text
tabla sievcac_clean
columna geom con geometría espacial
```

En MongoDB:

```text
base de datos sievcac
colección casos
```

---

## Solución de errores comunes

### Error: `No module named bdtools`

Ejecutar desde la raíz:

```bash
conda run -n proyectofinalbdtools python -m pip install -e .
```

O verificar que `src` esté en el `sys.path`.

---

### Error: `No module named flows`

Agregar la raíz del proyecto al `sys.path` en el notebook:

```python
sys.path.insert(0, str(PROJECT_ROOT))
```

También verificar que exista:

```text
flows/pipeline.py
```

---

### Error: `No module named geopandas`

Instalar GeoPandas en el ambiente correcto:

```bash
conda install -n proyectofinalbdtools -c conda-forge geopandas -y
```

Verificar instalación:

```bash
conda run -n proyectofinalbdtools python -c "import geopandas as gpd; print(gpd.__version__)"
```

---

### Error de autenticación en PostgreSQL

Si aparece un error de autenticación para el usuario `bdtools`, limpiar volúmenes y recrear servicios:

```bash
docker compose down -v
docker compose up -d
```

Si existe otro PostgreSQL usando el puerto `5432`, cambiar el puerto a `5433` en `.env`:

```env
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
POSTGRES_DB=sievcac
POSTGRES_USER=bdtools
POSTGRES_PASSWORD=bdtools
```

Y en `docker-compose.yml`:

```yaml
ports:
  - "5433:5432"
```

Luego reiniciar:

```bash
docker compose down -v
docker compose up -d
```

---

### Error en OneHotEncoder por mezcla de tipos

Si aparece un error como:

```text
Encoders require their input argument must be uniformly strings or numbers
```

Verificar que en `src/bdtools/modeling.py` las columnas categóricas se conviertan a texto:

```python
for col in categorical_features:
    model_df[col] = (
        model_df[col]
        .fillna("SIN INFORMACION")
        .astype(str)
        .str.strip()
    )
```

Y que las columnas numéricas se conviertan explícitamente:

```python
for col in numeric_features:
    model_df[col] = pd.to_numeric(model_df[col], errors="coerce").fillna(0)
```

---

## Comandos principales

### Activar ambiente

```bash
conda activate proyectofinalbdtools
```

### Instalar proyecto local

```bash
conda run -n proyectofinalbdtools python -m pip install -e .
```

### Ejecutar pipeline sin bases de datos

```bash
conda run -n proyectofinalbdtools python -m flows.pipeline
```

### Levantar Docker

```bash
docker compose up -d
```

### Ejecutar pipeline con bases de datos

```bash
conda run -n proyectofinalbdtools python -c "from flows.pipeline import sievcac_flow; sievcac_flow(load_databases=True)"
```

### Verificar contenedores

```bash
docker compose ps
```

### Detener Docker

```bash
docker compose down
```

---

## Control de versiones

Revisar estado del repositorio:

```bash
git status
```

Agregar cambios:

```bash
git add .
```

Crear commit:

```bash
git commit -m "Agrega proyecto final Big Data Tools"
```

Subir cambios:

```bash
git push
```

---

## Notas metodológicas

Este proyecto trabaja con información sensible relacionada con violencia del conflicto armado. Por tanto:

* Los resultados deben interpretarse con cautela.
* El análisis no busca reemplazar investigaciones históricas, jurídicas o sociales.
* El modelo predictivo es exploratorio y académico.
* Las visualizaciones deben leerse como apoyo descriptivo, no como explicación causal.
* La calidad de los resultados depende de la calidad, cobertura y consistencia del registro administrativo original.

---

## Limitaciones

* Posibles valores faltantes en variables temporales, geográficas o categóricas.
* Posibles registros con año desconocido o codificado como `0`.
* Coordenadas no disponibles para todos los registros.
* Desbalance de clases en la variable `alto_impacto`.
* Modelo predictivo inicial, no optimizado para uso operativo.
* Dataset limitado a la fuente suministrada para el proyecto.

---

## Conclusión técnica

El proyecto implementa una solución integral de análisis de datos y herramientas Big Data sobre un dataset sensible y relevante para el contexto colombiano. La solución incluye limpieza, análisis exploratorio, visualización, modelado supervisado, procesamiento geoespacial, orquestación con Prefect, almacenamiento en PostgreSQL/PostGIS y MongoDB, y ejecución reproducible mediante Docker Compose.

---

## Autores

* Nombre del estudiante 1
* Nombre del estudiante 2
* Nombre del estudiante 3

---

## Asignatura

Herramientas de Big Data
Maestría en Analítica Aplicada
Universidad de La Sabana

---

## Profesor

Hugo Franco, Ph.D.

---

## Fecha

3 de Mayo del 2026

````

```text
Fabian Moya
Mariana Olivares
Nicolas Rodriguez 
````

