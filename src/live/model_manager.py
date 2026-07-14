from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock
from typing import Any

import pandas as pd

from src.live.features import MODEL_FEATURES
from src.live.training import predict_with_bundle


class LiveModelManager:
    def __init__(self, private_path: Path, public_demo_path: Path) -> None:
        configured = os.getenv("AI4I_MODEL_PATH", "").strip()
        candidates = [Path(configured)] if configured else [Path(private_path), Path(public_demo_path)]
        self._selected_path = next((path for path in candidates if path.exists()), None)
        self._bundle: dict[str, Any] | None = None
        self._error = ""
        self._lock = Lock()
        self.reload()

    def reload(self) -> None:
        with self._lock:
            self._bundle = None
            self._error = ""
            if self._selected_path is None:
                self._error = "No live model bundle is available."
                return
            try:
                bundle = json.loads(self._selected_path.read_text(encoding="utf-8"))
                required = {"model", "metadata", "facility_limits_kva"}
                if not isinstance(bundle, dict) or not required.issubset(bundle):
                    raise ValueError("Model bundle is missing required fields.")
                self._bundle = bundle
            except Exception as exc:
                self._error = str(exc)

    @property
    def ready(self) -> bool:
        return self._bundle is not None

    def status(self) -> dict[str, object]:
        metadata = dict(self._bundle.get("metadata", {})) if self._bundle else {}
        return {
            "ready": self.ready,
            "model_mode": metadata.get("model_mode", "unavailable"),
            "model_family": metadata.get("model_family"),
            "trained_utc": metadata.get("trained_utc"),
            "prediction_horizon_minutes": metadata.get("prediction_horizon_minutes", 30),
            "minimum_history_intervals": metadata.get("minimum_history_intervals", 4),
            "facility_count": metadata.get("facility_count", 0),
            "metrics": metadata.get("metrics", {}),
            "source": "private_model" if self._selected_path and "private_models" in self._selected_path.parts else "public_demo_model",
            "error": self._error,
            "operating_mode": "advisory",
        }

    def predict(self, features: pd.DataFrame) -> float:
        if not self._bundle:
            raise RuntimeError(self._error or "Live model is not ready.")
        missing = set(MODEL_FEATURES).difference(features.columns)
        if missing:
            raise ValueError(f"Live features are missing: {sorted(missing)}")
        return float(predict_with_bundle(self._bundle, features)[0])

    def facility_limit(self, facility_id: str, current_kva: float) -> float:
        if not self._bundle:
            return max(current_kva * 1.1, 1.0)
        limits = self._bundle.get("facility_limits_kva", {})
        configured = limits.get(str(facility_id))
        return float(configured) if configured is not None else max(current_kva * 1.1, 1.0)
