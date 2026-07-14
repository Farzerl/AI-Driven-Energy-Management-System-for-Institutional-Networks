from __future__ import annotations

import os
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.api.cost_store import load_cost_impact
from src.api.evidence_store import (
    DEFAULT_EVIDENCE_DIR,
    DEFAULT_OPERATOR_LOG,
    REPO_ROOT,
    append_operator_decision,
    build_demo_alerts,
    load_control_comparison,
    load_dashboard_evidence,
    read_operator_decisions,
)
from src.api.meter_store import MeterReadingStore, read_edge_status
from src.api.schemas import HealthResponse, OperatorDecision
from src.edge.schemas import MeterReading, MeterReadingBatch
from src.live.forecast_store import ForecastStore
from src.live.model_manager import LiveModelManager
from src.live.service import LiveInferenceService

DEFAULT_METER_STORE = REPO_ROOT / "runtime" / "meter_readings.jsonl"
DEFAULT_EDGE_STATUS = REPO_ROOT / "runtime" / "edge_status.json"
DEFAULT_COST_IMPACT_DIR = REPO_ROOT / "evidence" / "cost_impact"
DEFAULT_FORECAST_STORE = REPO_ROOT / "runtime" / "live_forecasts.jsonl"
DEFAULT_PRIVATE_MODEL = REPO_ROOT / "private_models" / "uz_live_forecaster.json"
DEFAULT_PUBLIC_MODEL = REPO_ROOT / "models" / "public_demo" / "live_forecaster.json"


def create_app(
    evidence_dir: Path | None = None,
    operator_log: Path | None = None,
    api_key: str | None = None,
    meter_store_path: Path | None = None,
    edge_status_path: Path | None = None,
    cost_impact_dir: Path | None = None,
    forecast_store_path: Path | None = None,
    private_model_path: Path | None = None,
    public_model_path: Path | None = None,
) -> FastAPI:
    evidence_path = Path(evidence_dir or os.getenv("AI4I_EVIDENCE_DIR", DEFAULT_EVIDENCE_DIR))
    operator_log_path = Path(operator_log or os.getenv("AI4I_OPERATOR_LOG", DEFAULT_OPERATOR_LOG))
    meter_path = Path(meter_store_path or os.getenv("AI4I_METER_STORE", DEFAULT_METER_STORE))
    status_path = Path(edge_status_path or os.getenv("AI4I_EDGE_STATUS", DEFAULT_EDGE_STATUS))
    cost_path = Path(cost_impact_dir or os.getenv("AI4I_COST_IMPACT_DIR", DEFAULT_COST_IMPACT_DIR))
    forecast_path = Path(forecast_store_path or os.getenv("AI4I_FORECAST_STORE", DEFAULT_FORECAST_STORE))
    private_path = Path(private_model_path or DEFAULT_PRIVATE_MODEL)
    public_path = Path(public_model_path or DEFAULT_PUBLIC_MODEL)
    configured_api_key = api_key if api_key is not None else os.getenv("AI4I_API_KEY")

    meter_store = MeterReadingStore(meter_path)
    model_manager = LiveModelManager(private_path, public_path)
    forecast_store = ForecastStore(forecast_path)
    live_service = LiveInferenceService(model_manager, forecast_store)
    startup_refresh = live_service.refresh(meter_store.all())

    app = FastAPI(
        title="AI4I Institutional EMS API",
        version="1.3.0-live-inference",
        description=(
            "Public-safe evidence API, operational edge-to-AI inference, cost-impact planning model "
            "and advisory Estates workflow."
        ),
    )

    dashboard_dir = REPO_ROOT / "dashboard"
    static_dir = dashboard_dir / "static"
    diagrams_dir = REPO_ROOT / "docs" / "diagrams"
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    app.mount("/evidence-assets", StaticFiles(directory=evidence_path), name="evidence-assets")
    if diagrams_dir.exists():
        app.mount("/diagrams", StaticFiles(directory=diagrams_dir), name="diagrams")

    @app.middleware("http")
    async def add_security_headers(request, call_next):  # type: ignore[no-untyped-def]
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
            "connect-src 'self'; font-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
        )
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        return response

    def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
        if configured_api_key and x_api_key != configured_api_key:
            raise HTTPException(status_code=401, detail="Valid X-API-Key required.")

    @app.get("/", include_in_schema=False)
    def dashboard() -> FileResponse:
        return FileResponse(dashboard_dir / "index.html")

    @app.get("/api/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(
            status="online",
            evidence_ready=(evidence_path / "dashboard_evidence.json").exists(),
            operating_mode="advisory",
            api_key_required=bool(configured_api_key),
            model_ready=model_manager.ready,
        )

    @app.get("/api/summary")
    def summary() -> dict[str, object]:
        evidence = load_dashboard_evidence(evidence_path)
        quality = evidence["dataset_quality"]
        forecast = evidence["forecast"]
        peak = evidence["peak_risk"]
        comparison = evidence["controller_comparison"]["comparison"]
        return {
            "dataset": {
                "facilities": quality["facilities"],
                "intervals": quality["rows_after_grid_completion"],
                "usable_percent": quality["forecast_usable_percent"],
                "date_start": quality["date_start"],
                "date_end": quality["date_end"],
            },
            "forecast": {
                "baseline_mae_kva": forecast["baseline"]["mae_kva"],
                "model_mae_kva": forecast["model"]["mae_kva"],
                "mae_reduction_percent": forecast["improvement"]["model_vs_persistence"]["mae_reduction_percent"],
                "rmse_reduction_percent": forecast["improvement"]["model_vs_persistence"]["rmse_reduction_percent"],
            },
            "peak_risk": {
                "balanced_accuracy": peak["balanced_accuracy"],
                "macro_f1": peak["macro_f1"],
                "high_warning_recall": peak["actual_high_predicted_medium_or_high_recall"],
                "critical_miss_rate": peak["actual_high_predicted_low_miss_rate"],
            },
            "controller_comparison": comparison,
            "cost_status": "public_source_planning_estimate_not_actual_bill",
            "operating_mode": "advisory_or_operator_confirmed",
            "live_model": model_manager.status(),
        }

    @app.get("/api/evidence")
    def evidence() -> dict[str, object]:
        return load_dashboard_evidence(evidence_path)

    @app.get("/api/control-comparison")
    def control_comparison() -> dict[str, object]:
        return load_control_comparison(evidence_path)

    @app.get("/api/cost-impact")
    def cost_impact() -> dict[str, object]:
        return load_cost_impact(cost_path)

    @app.get("/api/model-status")
    def model_status() -> dict[str, object]:
        return {**model_manager.status(), "startup_refresh": startup_refresh}

    @app.get("/api/live-forecasts")
    def live_forecasts(limit: int = 50) -> dict[str, object]:
        safe_limit = max(1, min(limit, 500))
        return {
            "mode": "operational_live_inference",
            "model": model_manager.status(),
            "summary": forecast_store.summary(),
            "items": live_service.latest_forecasts(safe_limit),
        }

    @app.get("/api/live-alerts")
    def live_alerts(limit: int = 50) -> dict[str, object]:
        return {"mode": "live_edge_forecast", "alerts": live_service.live_alerts(limit)}

    @app.post("/api/live-inference/rebuild", dependencies=[Depends(require_api_key)])
    def rebuild_live_inference() -> dict[str, object]:
        return live_service.refresh(meter_store.all())

    @app.get("/api/alerts")
    def alerts() -> dict[str, object]:
        live = live_service.live_alerts()
        if live:
            return {"mode": "live_edge_forecast", "alerts": live}
        return {
            "mode": "public_sample_fallback",
            "alerts": build_demo_alerts(),
            "notice": "Start START_EDGE_DEMO.bat to replace sample alerts with forecasts from incoming edge values.",
        }

    @app.get("/api/operator-decisions")
    def decisions(limit: int = 50) -> dict[str, object]:
        safe_limit = max(1, min(limit, 200))
        return {"items": read_operator_decisions(operator_log_path, safe_limit)}

    @app.post("/api/operator-decisions", dependencies=[Depends(require_api_key)])
    def save_decision(decision: OperatorDecision) -> dict[str, object]:
        return append_operator_decision(operator_log_path, decision.model_dump())

    @app.post("/api/meter-readings", dependencies=[Depends(require_api_key)])
    def ingest_meter_readings(payload: MeterReading | MeterReadingBatch) -> dict[str, object]:
        readings = payload.readings if isinstance(payload, MeterReadingBatch) else [payload]
        result = meter_store.append(readings)
        inference = live_service.refresh(meter_store.all())
        return {"status": "accepted", **result, "live_inference": inference}

    @app.get("/api/meter-readings")
    def latest_meter_readings(limit: int = 50) -> dict[str, object]:
        safe_limit = max(1, min(limit, 500))
        return {"mode": "edge_demo", "items": meter_store.latest(safe_limit)}

    @app.get("/api/edge-status")
    def edge_status() -> dict[str, object]:
        return {
            "mode": "edge_demo",
            "store": meter_store.summary(),
            "gateway": read_edge_status(status_path),
            "live_forecasts": forecast_store.summary(),
            "model": model_manager.status(),
            "boundary": "Forecasting and advisory recommendations only; no electrical actuation.",
        }

    return app


app = create_app()
