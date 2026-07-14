from __future__ import annotations

from pathlib import Path

from src.live.features import feature_row_from_history
from src.live.model_manager import LiveModelManager

ROOT = Path(__file__).resolve().parents[1]


def test_public_demo_model_loads_and_predicts() -> None:
    manager = LiveModelManager(
        ROOT / "private_models" / "missing.json",
        ROOT / "models" / "public_demo" / "live_forecaster.json",
    )
    assert manager.ready is True
    records = [
        {
            "reading_id": f"r{index}",
            "timestamp": f"2026-07-14T{9 + index // 2:02d}:{'30' if index % 2 else '00'}:00+02:00",
            "facility_id": "F17",
            "kva": 460 + 12 * index,
            "kwh": 220 + 5 * index,
            "power_factor": 0.91,
        }
        for index in range(4)
    ]
    features, _ = feature_row_from_history(records)
    assert manager.predict(features) >= 0
    assert manager.status()["source"] == "public_demo_model"
