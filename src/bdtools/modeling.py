from __future__ import annotations

import json

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from bdtools.config import PATHS, ProjectPaths, ensure_directories


def train_high_impact_classifier(df: pd.DataFrame, paths: ProjectPaths = PATHS) -> dict:
    ensure_directories(paths)

    if "alto_impacto" not in df.columns:
        raise ValueError("No existe la columna alto_impacto.")

    candidate_features = [
        "departamento",
        "region",
        "modalidad",
        "presunto_responsable",
        "forma_de_vinculacion",
        "tipo_de_vinculacion",
        "cantidad_hechos_simultaneos",
        "anio",
    ]
    features = [col for col in candidate_features if col in df.columns]
    model_df = df[features + ["alto_impacto"]].dropna(subset=["alto_impacto"]).copy()

    numeric_features = [
        col for col in ["anio", "cantidad_hechos_simultaneos"]
        if col in features
    ]
    
    categorical_features = [
        col for col in features
        if col not in numeric_features
    ]
    
    for col in numeric_features:
        model_df[col] = pd.to_numeric(model_df[col], errors="coerce").fillna(0)

    for col in categorical_features:
        model_df[col] = (
            model_df[col]
            .fillna("SIN INFORMACION")
            .astype(str)
            .str.strip()
        )

    X = model_df[features]
    y = model_df["alto_impacto"].astype(int)


    if y.nunique() < 2:
        raise ValueError("La variable objetivo solo tiene una clase. No se puede entrenar el modelo.")

    stratify = y if y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=stratify,
    )

    categorical = categorical_features
    numeric = numeric_features

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", StandardScaler(), numeric),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=3000, class_weight="balanced", solver="liblinear")),
        ]
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    report_text = classification_report(y_test, y_pred, zero_division=0)
    matrix = confusion_matrix(y_test, y_pred)

    with open(paths.tables / "classification_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    with open(paths.tables / "classification_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)

    disp = ConfusionMatrixDisplay(confusion_matrix=matrix)
    disp.plot()
    plt.title("Matriz de confusión - Clasificador alto impacto")
    plt.tight_layout()
    plt.savefig(paths.figures / "matriz_confusion.png", dpi=150)
    plt.close()

    return {
    "features": features,
    "report": report,
    "classification_report_text": report_text,
    "confusion_matrix": matrix.tolist(),
    }
