from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from software.ai_engine.dataset_generator import generate_synthetic_uz_dataset


NUMERIC_FEATURES = [
    "hour",
    "minute",
    "dayofweek",
    "month",
    "is_weekend",
    "occupancy_proxy",
    "weather_temp_c",
    "avg_kw",
    "kwh",
    "kva",
    "kvarh",
    "power_factor",
    "voltage_v",
    "current_a",
    "kva_lag_1",
    "kva_lag_2",
    "kva_rolling_mean_4",
    "kva_rolling_max_4",
]

CATEGORICAL_FEATURES = [
    "facility_id",
    "sector",
    "load_type",
    "academic_status",
    "tariff_period",
    "event_type",
]


def add_model_features(data: pd.DataFrame) -> pd.DataFrame:
    result = data.sort_values(["facility_id", "timestamp"]).copy()
    result["timestamp"] = pd.to_datetime(result["timestamp"])
    result["hour"] = result["timestamp"].dt.hour
    result["minute"] = result["timestamp"].dt.minute
    result["dayofweek"] = result["timestamp"].dt.dayofweek
    result["month"] = result["timestamp"].dt.month
    result["is_weekend"] = result["dayofweek"].isin([5, 6]).astype(int)

    group = result.groupby("facility_id", group_keys=False)["kva"]
    result["kva_lag_1"] = group.shift(1)
    result["kva_lag_2"] = group.shift(2)
    result["kva_rolling_mean_4"] = group.rolling(4, min_periods=2).mean().reset_index(level=0, drop=True)
    result["kva_rolling_max_4"] = group.rolling(4, min_periods=2).max().reset_index(level=0, drop=True)
    return result.dropna(subset=NUMERIC_FEATURES + ["next_interval_kva"])


def make_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
            ("numeric", "passthrough", NUMERIC_FEATURES),
        ],
        remainder="drop",
    )


def safe_mape(actual: pd.Series, predicted: np.ndarray) -> float:
    actual_array = np.asarray(actual, dtype=float)
    predicted_array = np.asarray(predicted, dtype=float)
    denominator = np.where(np.abs(actual_array) < 1e-6, 1e-6, actual_array)
    return float(np.mean(np.abs((actual_array - predicted_array) / denominator)) * 100)


def train_models(days: int = 244, seed: int = 42, max_rows: int = 120_000) -> dict[str, object]:
    raw = generate_synthetic_uz_dataset(days=days, seed=seed)
    data = add_model_features(raw)

    if len(data) > max_rows:
        data = data.sample(n=max_rows, random_state=seed).sort_values("timestamp")

    x = data[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y_reg = data["next_interval_kva"]
    y_peak = data["peak_risk"]
    y_anomaly = data["is_anomaly"].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(x, y_reg, test_size=0.25, shuffle=False)
    _, x_test_labels, peak_train, peak_test = train_test_split(x, y_peak, test_size=0.25, shuffle=False)
    _, _, anomaly_train, anomaly_test = train_test_split(x, y_anomaly, test_size=0.25, shuffle=False)

    previous_interval_prediction = x_test["kva"].to_numpy()
    baseline = {
        "mae_kva": float(mean_absolute_error(y_test, previous_interval_prediction)),
        "mape_percent": safe_mape(y_test, previous_interval_prediction),
    }

    random_forest_regressor = Pipeline(
        steps=[
            ("preprocess", make_preprocessor()),
            ("model", RandomForestRegressor(n_estimators=120, random_state=seed, min_samples_leaf=3, n_jobs=-1)),
        ]
    )
    random_forest_regressor.fit(x_train, y_train)
    rf_pred = random_forest_regressor.predict(x_test)

    gradient_boosting_regressor = Pipeline(
        steps=[
            ("preprocess", make_preprocessor()),
            ("model", HistGradientBoostingRegressor(max_iter=180, learning_rate=0.08, random_state=seed)),
        ]
    )
    gradient_boosting_regressor.fit(x_train, y_train)
    gb_pred = gradient_boosting_regressor.predict(x_test)

    peak_classifier = Pipeline(
        steps=[
            ("preprocess", make_preprocessor()),
            ("model", RandomForestClassifier(n_estimators=160, class_weight="balanced_subsample", random_state=seed, n_jobs=-1)),
        ]
    )
    peak_classifier.fit(x_train, peak_train)
    peak_pred = peak_classifier.predict(x_test_labels)

    anomaly_classifier = Pipeline(
        steps=[
            ("preprocess", make_preprocessor()),
            ("model", RandomForestClassifier(n_estimators=160, class_weight="balanced_subsample", random_state=seed, n_jobs=-1)),
        ]
    )
    anomaly_classifier.fit(x_train, anomaly_train)
    anomaly_pred = anomaly_classifier.predict(x_test_labels)

    results = {
        "dataset_rows_used": int(len(data)),
        "dataset_facilities": int(data["facility_id"].nunique()),
        "dataset_event_types": sorted(data["event_type"].unique().tolist()),
        "regression_target": "next_interval_kva",
        "baseline_previous_interval": baseline,
        "random_forest_regressor": {
            "mae_kva": float(mean_absolute_error(y_test, rf_pred)),
            "mape_percent": safe_mape(y_test, rf_pred),
        },
        "hist_gradient_boosting_regressor": {
            "mae_kva": float(mean_absolute_error(y_test, gb_pred)),
            "mape_percent": safe_mape(y_test, gb_pred),
        },
        "peak_risk_classifier": {
            "accuracy": float(accuracy_score(peak_test, peak_pred)),
            "classification_report": classification_report(peak_test, peak_pred, output_dict=True, zero_division=0),
        },
        "anomaly_classifier": {
            "accuracy": float(accuracy_score(anomaly_test, anomaly_pred)),
            "classification_report": classification_report(anomaly_test, anomaly_pred, output_dict=True, zero_division=0),
        },
    }

    return {
        "results": results,
        "models": {
            "random_forest_regressor": random_forest_regressor,
            "hist_gradient_boosting_regressor": gradient_boosting_regressor,
            "peak_classifier": peak_classifier,
            "anomaly_classifier": anomaly_classifier,
        },
    }


def run_training_demo(days: int, output_dir: str | Path, seed: int = 42) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    training = train_models(days=days, seed=seed)
    results_path = output_path / "synthetic_model_results.json"
    results_path.write_text(json.dumps(training["results"], indent=2), encoding="utf-8")

    for model_name, model in training["models"].items():
        joblib.dump(model, output_path / f"{model_name}.joblib")

    return results_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train EMS AI models on physically consistent synthetic UZ-style data.")
    parser.add_argument("--days", type=int, default=244)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", default="evidence/synthetic_model_evidence")
    args = parser.parse_args()

    path = run_training_demo(days=args.days, output_dir=args.output_dir, seed=args.seed)
    print(f"Saved model evidence to {path}")
