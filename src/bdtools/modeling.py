from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .config import PATHS


FEATURES = [
    "anio",
    "mes_original",
    "departamento",
    "region",
    "modalidad",
    "presunto_responsable",
    "forma_de_vinculacion",
    "tipo_de_vinculacion",
    "num_hechos_simultaneos",
    "latitud",
    "longitud",
]

TARGET = "alto_impacto"


def train_high_impact_classifier(df: pd.DataFrame) -> tuple[Pipeline, pd.DataFrame]:
    """
    Modelo inicial: clasifica casos de alto impacto (>1 víctima).
    Nota metodológica: no se usa 'total_de_victimas_del_caso' como predictor
    porque define directamente la variable objetivo.
    """
    data = df.dropna(subset=[TARGET]).copy()
    X = data[[c for c in FEATURES if c in data.columns]]
    y = data[TARGET].astype(int)

    numeric_features = [c for c in X.columns if c in ["anio", "mes_original", "num_hechos_simultaneos", "latitud", "longitud"]]
    categorical_features = [c for c in X.columns if c not in numeric_features]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", SimpleImputer(strategy="median"), numeric_features),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=10)),
                    ]
                ),
                categorical_features,
            ),
        ],
        remainder="drop",
    )

    model = RandomForestClassifier(
        n_estimators=300,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    pipe = Pipeline(steps=[("preprocess", preprocessor), ("model", model)])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipe.fit(X_train, y_train)
    proba = pipe.predict_proba(X_test)[:, 1]
    pred = (proba >= 0.5).astype(int)

    metrics = {
        "roc_auc": roc_auc_score(y_test, proba),
        "average_precision": average_precision_score(y_test, proba),
        "target_rate": y.mean(),
        "n_train": len(X_train),
        "n_test": len(X_test),
    }

    report = classification_report(y_test, pred, output_dict=True, zero_division=0)
    metrics_df = pd.DataFrame([metrics])
    report_df = pd.DataFrame(report).T.reset_index(names="clase")

    PATHS.models_dir.mkdir(parents=True, exist_ok=True)
    PATHS.tables_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, PATHS.models_dir / "modelo_alto_impacto.joblib")
    metrics_df.to_csv(PATHS.tables_dir / "metricas_modelo_alto_impacto.csv", index=False)
    report_df.to_csv(PATHS.tables_dir / "classification_report_alto_impacto.csv", index=False)

    return pipe, metrics_df


def run_spatial_clustering(df: pd.DataFrame, eps_km: float = 25, min_samples: int = 20) -> pd.DataFrame:
    """
    Agrupamiento espacial con DBSCAN usando distancia haversine.
    eps_km controla el radio aproximado del clúster.
    """
    from sklearn.cluster import DBSCAN

    geo = df.dropna(subset=["latitud", "longitud"]).copy()
    coords_rad = np.radians(geo[["latitud", "longitud"]].to_numpy())
    kms_per_radian = 6371.0088
    db = DBSCAN(
        eps=eps_km / kms_per_radian,
        min_samples=min_samples,
        metric="haversine",
        algorithm="ball_tree",
    )
    geo["cluster_espacial"] = db.fit_predict(coords_rad)

    resumen = (
        geo.groupby("cluster_espacial", as_index=False)
        .agg(
            casos=("id_caso", "count"),
            victimas=("total_de_victimas_del_caso", "sum"),
            latitud_media=("latitud", "mean"),
            longitud_media=("longitud", "mean"),
            departamentos=("departamento", lambda x: ", ".join(sorted(set(x))[:5])),
        )
        .sort_values("casos", ascending=False)
    )
    resumen.to_csv(PATHS.tables_dir / "clusters_espaciales.csv", index=False, encoding="utf-8")
    return resumen
