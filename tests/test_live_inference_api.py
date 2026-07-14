from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from src.api.server import create_app

ROOT = Path(__file__).resolve().parents[1]


def reading(index: int) -> dict[str, object]:
    hour = 9 + index // 2
    minute = 30 if index % 2 else 0
    return {
        "timestamp": f"2026-07-14T{hour:02d}:{minute:02d}:00+02:00",
        "facility_id": "F17",
        "kva": 470.0 + index * 20,
        "kwh": 220.0 + index * 8,
        "power_factor": 0.90,
        "source": "live-api-test",
    }


def test_four_edge_intervals_generate_live_forecast(tmp_path: Path) -> None:
    app = create_app(
        evidence_dir=ROOT / "evidence" / "public_dashboard",
        operator_log=tmp_path / "operator.jsonl",
        meter_store_path=tmp_path / "meter.jsonl",
        edge_status_path=tmp_path / "edge.json",
        cost_impact_dir=ROOT / "evidence" / "cost_impact",
        forecast_store_path=tmp_path / "forecasts.jsonl",
        private_model_path=tmp_path / "missing-private.json",
        public_model_path=ROOT / "models" / "public_demo" / "live_forecaster.json",
        api_key=None,
    )
    client = TestClient(app)
    response = client.post("/api/meter-readings", json={"readings": [reading(i) for i in range(4)]})
    assert response.status_code == 200
    assert response.json()["accepted"] == 4
    assert response.json()["live_inference"]["generated"] == 1

    forecasts = client.get("/api/live-forecasts").json()
    assert forecasts["model"]["ready"] is True
    assert len(forecasts["items"]) == 1
    assert forecasts["items"][0]["facility_id"] == "F17"
    assert forecasts["items"][0]["operating_mode"] == "advisory"


def test_model_status_reports_public_fallback(tmp_path: Path) -> None:
    app = create_app(
        evidence_dir=ROOT / "evidence" / "public_dashboard",
        operator_log=tmp_path / "operator.jsonl",
        meter_store_path=tmp_path / "meter.jsonl",
        forecast_store_path=tmp_path / "forecast.jsonl",
        private_model_path=tmp_path / "missing-private.json",
        public_model_path=ROOT / "models" / "public_demo" / "live_forecaster.json",
        api_key=None,
    )
    payload = TestClient(app).get("/api/model-status").json()
    assert payload["ready"] is True
    assert payload["source"] == "public_demo_model"
    assert payload["prediction_horizon_minutes"] == 30
