from __future__ import annotations

import hashlib
from collections import defaultdict
from datetime import datetime, timezone
from typing import Iterable, Mapping

from src.live.features import MIN_HISTORY, feature_row_from_history
from src.live.forecast_store import ForecastStore
from src.live.model_manager import LiveModelManager


def risk_from_utilization(utilization: float) -> str:
    if utilization >= 0.95:
        return "high"
    if utilization >= 0.85:
        return "medium"
    return "low"


def recommendation(risk: str, tariff_period: str) -> str:
    if risk == "high" and tariff_period == "peak":
        return "Defer approved non-critical loads and stagger equipment starts after operator review."
    if risk == "high":
        return "Prepare supervised load coordination and verify the facility operating schedule."
    if risk == "medium" and tariff_period == "peak":
        return "Prepare an operator-confirmed load coordination action if demand continues rising."
    if tariff_period == "offpeak":
        return "Continue monitoring and schedule approved deferrable loads where operationally safe."
    return "Continue monitoring. No immediate load action is recommended."


class LiveInferenceService:
    def __init__(self, model: LiveModelManager, store: ForecastStore) -> None:
        self.model = model
        self.store = store

    def refresh(self, meter_records: Iterable[Mapping[str, object]]) -> dict[str, object]:
        grouped: dict[str, list[Mapping[str, object]]] = defaultdict(list)
        for record in meter_records:
            grouped[str(record["facility_id"])].append(record)
        produced: list[dict[str, object]] = []
        failures: list[str] = []
        if not self.model.ready:
            return {"generated": 0, "failures": [str(self.model.status().get("error"))]}

        for facility_id, records in grouped.items():
            ordered = sorted(records, key=lambda item: str(item["timestamp"]))
            for index in range(MIN_HISTORY - 1, len(ordered)):
                window = ordered[max(0, index - MIN_HISTORY + 1): index + 1]
                if len(window) < MIN_HISTORY:
                    continue
                try:
                    features, context = feature_row_from_history(window)
                    reading_id = str(context.get("reading_id") or f"{facility_id}-{context['reading_timestamp']}")
                    forecast_id = hashlib.sha256(
                        f"{reading_id}|{self.model.status().get('trained_utc')}".encode("utf-8")
                    ).hexdigest()[:24]
                    raw_model_forecast = self.model.predict(features)
                    current_kva = float(context["current_kva"])
                    limit = self.model.facility_limit(facility_id, current_kva)
                    lag_1 = float(features.iloc[0]["kva_lag_1"])
                    out_of_distribution = current_kva > 1.6 * limit or current_kva < 0.15 * limit
                    if out_of_distribution:
                        forecast_kva = max(current_kva + 0.5 * (current_kva - lag_1), 0.0)
                        limit = max(limit, float(features.iloc[0]["kva_rolling_max_4"]) * 1.05)
                        inference_method = "guarded_persistence_trend"
                        limit_source = "adaptive_demo_guard"
                    else:
                        forecast_kva = raw_model_forecast
                        inference_method = "trained_model"
                        limit_source = "training_only_facility_limit"
                    risk_basis_kva = max(current_kva, forecast_kva)
                    utilization = risk_basis_kva / max(limit, 1e-9)
                    risk = risk_from_utilization(utilization)
                    produced.append(
                        {
                            "forecast_id": forecast_id,
                            "reading_id": reading_id,
                            "facility_id": facility_id,
                            "reading_timestamp": context["reading_timestamp"],
                            "forecast_timestamp": context["forecast_timestamp"],
                            "current_kva": round(current_kva, 3),
                            "raw_model_forecast_kva": round(raw_model_forecast, 3),
                            "forecast_kva": round(forecast_kva, 3),
                            "inference_method": inference_method,
                            "risk_basis_kva": round(risk_basis_kva, 3),
                            "facility_limit_kva": round(limit, 3),
                            "limit_source": limit_source,
                            "utilization_percent": round(utilization * 100, 2),
                            "peak_risk": risk,
                            "tariff_period": context["forecast_tariff_period"],
                            "recommended_action": recommendation(risk, str(context["forecast_tariff_period"])),
                            "model_mode": self.model.status().get("model_mode"),
                            "operating_mode": "advisory",
                            "generated_utc": datetime.now(timezone.utc).isoformat(),
                        }
                    )
                except Exception as exc:
                    failures.append(f"{facility_id}: {exc}")
        generated = self.store.append(produced)
        return {"generated": generated, "candidates": len(produced), "failures": failures[:20]}

    def latest_forecasts(self, limit: int = 50) -> list[dict[str, object]]:
        return self.store.latest(limit)

    def live_alerts(self, limit: int = 50) -> list[dict[str, object]]:
        latest_by_facility: dict[str, dict[str, object]] = {}
        for item in self.store.all():
            latest_by_facility[str(item["facility_id"])] = item
        alerts: list[dict[str, object]] = []
        for item in latest_by_facility.values():
            if item.get("peak_risk") not in {"medium", "high"}:
                continue
            alerts.append(
                {
                    "alert_id": str(item["forecast_id"]),
                    "facility_name": str(item["facility_id"]),
                    "timestamp": str(item["forecast_timestamp"]),
                    "tariff_period": str(item["tariff_period"]),
                    "risk": str(item["peak_risk"]),
                    "current_kva": float(item["current_kva"]),
                    "forecast_kva": float(item["forecast_kva"]),
                    "facility_limit_kva": float(item["facility_limit_kva"]),
                    "utilization_percent": float(item["utilization_percent"]),
                    "planning_reduction_kva": round(max(float(item.get("risk_basis_kva", item["forecast_kva"])) - 0.9 * float(item["facility_limit_kva"]), 0), 2),
                    "recommended_action": str(item["recommended_action"]),
                    "source": "live_edge_forecast",
                }
            )
        alerts.sort(key=lambda item: (item["risk"] != "high", -float(item["utilization_percent"])))
        return alerts[: max(1, min(limit, 200))]
