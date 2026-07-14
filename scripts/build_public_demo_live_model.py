from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from software.ai_engine.dataset_generator import FACILITIES, generate_synthetic_uz_dataset
from src.live.training import save_model_bundle, train_live_model_bundle


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the public-safe live inference demo model.")
    parser.add_argument("--days", type=int, default=80)
    parser.add_argument("--output", type=Path, default=ROOT / "models" / "public_demo" / "live_forecaster.json")
    parser.add_argument("--metrics", type=Path, default=ROOT / "evidence" / "live_model_validation" / "public_demo_model_metrics.json")
    args = parser.parse_args()

    data = generate_synthetic_uz_dataset(days=args.days, seed=42)
    alias_map = {profile.facility_id: f"F{index:02d}" for index, profile in enumerate(FACILITIES, start=1)}
    data["facility_id"] = data["facility_id"].map(alias_map)
    bundle = train_live_model_bundle(
        data[["timestamp", "facility_id", "kva", "kwh", "power_factor"]],
        source_kind="public_synthetic_demo",
        test_start=None,
        max_train_rows=90_000,
    )
    save_model_bundle(bundle, args.output, args.metrics)
    print(json.dumps(bundle["metadata"], indent=2))
    print(f"Saved public demo model to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
