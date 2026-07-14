from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.live.private_dataset import load_private_archive
from src.live.training import save_model_bundle, train_live_model_bundle

DEFAULT_WORKSPACE = ROOT.parent / "AI4I_PRIVATE_MODEL_WORKSPACE"
DEFAULT_INPUT = DEFAULT_WORKSPACE / "input"
DEFAULT_OUTPUT = DEFAULT_WORKSPACE / "output"
DEFAULT_MODEL = ROOT / "private_models" / "uz_live_forecaster.json"
DEFAULT_METRICS = ROOT / "evidence" / "private_model_validation" / "live_model_validation.json"


def find_archive(input_dir: Path) -> Path:
    archives = sorted(input_dir.glob("*.zip"))
    if len(archives) != 1:
        raise ValueError(
            f"Place exactly one dataset ZIP in {input_dir}. Found {len(archives)} ZIP files."
        )
    return archives[0]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Train and chronologically test the private live forecasting model."
    )
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--test-start", default="2026-04-01")
    parser.add_argument("--model-output", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--metrics-output", type=Path, default=DEFAULT_METRICS)
    args = parser.parse_args()

    archive = args.archive or find_archive(args.input_dir)
    DEFAULT_OUTPUT.mkdir(parents=True, exist_ok=True)
    data, alias_map = load_private_archive(archive, DEFAULT_OUTPUT)
    bundle = train_live_model_bundle(
        data,
        source_kind="private_uz_chronological",
        test_start=args.test_start,
        max_train_rows=220_000,
    )
    save_model_bundle(bundle, args.model_output, args.metrics_output)
    report = {
        "status": "pass",
        "dataset_archive_name": archive.name,
        "facility_alias_count": len(alias_map),
        "raw_rows_after_basic_validation": len(data),
        "model_output": str(args.model_output.relative_to(ROOT)),
        "metrics_output": str(args.metrics_output.relative_to(ROOT)),
        "metadata": bundle["metadata"],
        "privacy": "Raw meter files and the private facility alias map remain outside the public repository.",
    }
    (DEFAULT_OUTPUT / "training_receipt.private.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    print("Private live model training and chronological testing: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
