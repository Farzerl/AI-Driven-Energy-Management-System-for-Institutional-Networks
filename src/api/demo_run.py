from __future__ import annotations

import argparse
from pathlib import Path

from src.config.facility_limits import DEFAULT_FACILITY_LIMITS_PATH, load_facility_limits
from src.features.time_series import add_lag_features, add_time_features
from src.ingestion.load_data import load_meter_data
from src.models.anomaly_detection import add_simple_anomaly_flags
from src.models.peak_risk import add_peak_risk, infer_facility_peak_limits
from src.recommendations.engine import add_recommendations
from src.tariff.zetdc_tou import add_tariff_features


def run_demo(
    data_path: str = "sample_data/sample_meter_readings.csv",
    peak_kva_limit: float = 700,
    facility_peak_limits: dict[str, float] | None = None,
    auto_limits: bool = False,
) -> None:
    data = load_meter_data(Path(data_path))
    limits = dict(facility_peak_limits or {})
    if auto_limits:
        limits.update(infer_facility_peak_limits(data, quantile=0.95, safety_margin=1.0))
    data = add_tariff_features(data)
    data = add_time_features(data)
    data = add_lag_features(data, target="kva")
    data = add_simple_anomaly_flags(data)
    data = add_peak_risk(data, peak_kva_limit=peak_kva_limit, facility_peak_limits=limits)
    data = add_recommendations(data)
    columns = ["timestamp", "facility_name", "kva", "peak_kva_limit", "peak_utilization_ratio", "tariff_period", "peak_risk", "is_anomaly", "recommended_action"]
    print(data[columns].tail(10).to_string(index=False))


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the AI4I EMS demo pipeline on sample or real meter data.")
    parser.add_argument("--data-path", default="sample_data/sample_meter_readings.csv")
    parser.add_argument("--peak-kva-limit", type=float, default=700)
    parser.add_argument("--facility-limits", default=str(DEFAULT_FACILITY_LIMITS_PATH))
    parser.add_argument("--auto-limits", action="store_true")
    parser.add_argument("--no-facility-limits", action="store_true")
    return parser


if __name__ == "__main__":
    args = build_arg_parser().parse_args()
    facility_limits: dict[str, float] = {}
    if not args.no_facility_limits and args.facility_limits:
        limits_path = Path(args.facility_limits)
        if limits_path.exists():
            facility_limits.update(load_facility_limits(limits_path))
    run_demo(args.data_path, args.peak_kva_limit, facility_limits, args.auto_limits)
