from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock
from typing import Iterable


class ForecastStore:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self._lock = Lock()

    def _read_unlocked(self) -> list[dict[str, object]]:
        if not self.path.exists():
            return []
        output: list[dict[str, object]] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                output.append(json.loads(line))
        return output

    def append(self, forecasts: Iterable[dict[str, object]]) -> int:
        candidates = list(forecasts)
        if not candidates:
            return 0
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            existing = self._read_unlocked()
            known = {str(item["forecast_id"]) for item in existing}
            accepted = [item for item in candidates if str(item["forecast_id"]) not in known]
            if not accepted:
                return 0
            with self.path.open("a", encoding="utf-8") as handle:
                for item in accepted:
                    handle.write(json.dumps(item, separators=(",", ":")) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            return len(accepted)

    def latest(self, limit: int = 50) -> list[dict[str, object]]:
        safe_limit = max(1, min(limit, 500))
        with self._lock:
            records = self._read_unlocked()
        return list(reversed(records[-safe_limit:]))

    def all(self) -> list[dict[str, object]]:
        with self._lock:
            return self._read_unlocked()

    def summary(self) -> dict[str, object]:
        records = self.all()
        if not records:
            return {"forecast_count": 0, "latest_forecast_timestamp": None, "latest_facility_id": None}
        latest = records[-1]
        return {
            "forecast_count": len(records),
            "latest_forecast_timestamp": latest.get("forecast_timestamp"),
            "latest_facility_id": latest.get("facility_id"),
        }
