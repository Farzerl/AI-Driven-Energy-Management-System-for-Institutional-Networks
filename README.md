# AI-Driven Energy Management System in Institutional Networks

Track 3 Development repository for the 2026 AI for Impact Challenge.

AI4I-EMS is an integrated hardware-and-software energy-management system for institutional electrical networks. Its purpose is to help Estates and Facilities teams anticipate demand, identify emerging peak-risk conditions, coordinate non-critical loads, and preserve an auditable record of operational decisions.

The current repository contains the working software MVP and public-safe technical evidence. It proves the data pipeline, AI models, FastAPI backend, browser dashboard, operator workflow, testing, and security controls. The wider project also includes meter interfaces, edge data acquisition and buffering, optional additional submetering, and future supervised control of approved non-critical loads. The current MVP does not switch electrical loads autonomously.

## Primary user and decision

**Primary user:** University of Zimbabwe Estates and Facilities personnel responsible for campus electrical operations.

**Decision supported:** whether to prepare, defer, stagger, or reject a non-critical load action before the next half-hour demand interval.

Finance and institutional management are secondary users of aggregate reports. They are not expected to operate the live alert workflow.

## Start the demonstration on Windows

After downloading and extracting the repository, double-click:

```text
START_AI4I_EMS.bat
```

This is now the one-click operational launcher. It creates or validates `.venv`, installs the pinned dashboard dependencies when required, starts FastAPI on port 8000, starts the simulated edge gateway, waits for the first live next-half-hour forecast, and opens the dashboard. Keep the API and Edge Gateway service windows open while demonstrating the system.

The public demonstration does not require the confidential UZ dataset. It uses public-safe aggregate evidence, a synthetic fallback model, and accelerated simulated edge values to exercise the complete edge-to-AI forecasting path. `START_EDGE_DEMO.bat` remains available only as a manual recovery launcher.

## What the current MVP demonstrates

- ingestion and conservative cleaning logic for 22 institutional facility workbooks;
- half-hour demand forecasting and facility-specific peak-risk classification;
- direct comparison between forecast-assisted control and a simple current-demand rule;
- public-safe data-quality charts, heatmaps, profiles, and anonymous facility concentration;
- a FastAPI backend and responsive browser dashboard;
- operational ingestion of simulated gateway values into live next-half-hour forecasts;
- automatic replacement of sample fallback alerts with live forecast alerts after sufficient edge history arrives;
- an Estates and Facilities workflow to confirm, defer, dismiss, or mute an advisory action;
- append-only operator decision logging;
- architecture and private-to-public data-flow diagrams;
- pinned runtime dependencies, automated tests, CI checks, and a private-data security gate.

## Verified real-data evidence

The private dataset covers 22 facilities from 1 September 2025 to 30 April 2026 at 30-minute resolution.

| Evidence | Result |
|---|---:|
| Completed interval grid | 255,552 rows |
| Forecast-usable data | 99.898% |
| AI forecast MAE | 2.331 kVA |
| Persistence MAE | 2.731 kVA |
| MAE reduction | 14.65% |
| RMSE reduction | 25.95% |
| Actual high-risk events warned medium or high | 98.73% |
| Actual high-risk events missed as low | 1.27% |
| Critical misses avoided versus the simple rule | 161 |

The forecast-assisted controller reduces critical missed peaks but produces more advisory alerts than the simple rule. This supports human-confirmed operation rather than automatic switching.


## Operational live inference

Run the complete operational demonstration with:

```text
START_AI4I_EMS.bat
```

The launcher starts both the API and the simulated gateway. After four accelerated half-hour values arrive for a facility, the API constructs lag and rolling features, loads the active model, predicts the next half-hour kVA, classifies facility-limit risk, and generates an advisory recommendation. The launcher waits for the first forecast before reporting that the operational demonstration is ready.

The **Live forecast** tab shows current demand, forecast demand, facility limit, model source, risk and recent forecasts. The Estates queue uses live forecast alerts when available and retains a public sample fallback before sufficient gateway history exists. `START_EDGE_DEMO.bat` is retained for manual recovery and should not be run when the one-click gateway process is already active.

The public repository includes `models/public_demo/live_forecaster.json`, trained only on synthetic data. A locally trained private model at `private_models/uz_live_forecaster.json` takes precedence and remains excluded from GitHub. See [Operational flow](docs/live_inference/OPERATIONAL_FLOW.md) and [Private model handoff plan](docs/live_inference/PRIVATE_MODEL_HANDOFF_PLAN.md).

## Manual dashboard start

Windows PowerShell:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dashboard.lock.txt
python -m uvicorn src.api.server:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`.

## API endpoints

```text
GET  /api/health
GET  /api/summary
GET  /api/evidence
GET  /api/control-comparison
GET  /api/model-status
GET  /api/live-forecasts
GET  /api/live-alerts
POST /api/live-inference/rebuild
POST /api/meter-readings
GET  /api/meter-readings
GET  /api/edge-status
GET  /api/alerts
GET  /api/operator-decisions
POST /api/operator-decisions
```

Set `AI4I_API_KEY` to protect write operations during a networked demonstration. Optional environment variables are documented in `.env.example`.

## Run tests and security checks

```powershell
python -m pip install -r requirements.lock.txt
python -m pip install -r requirements-dev.lock.txt
python -m pytest -q
python -m scripts.security_scan --output-dir evidence\security
```

The GitHub Actions workflow runs the complete test suite, imports the API, and applies the security and private-data gate.

## Integrated architecture

```text
Existing smart meters and optional additional submeters
        ↓
Edge acquisition, validation, timestamping and local buffering
        ↓
Institutional data store and feature pipeline
        ↓
Demand forecast, peak-risk model and engineering rules
        ↓
Recommendation engine and FastAPI service
        ↓
Estates and Facilities dashboard
        ↓
Human-confirmed action and audit log
        ↓
Future supervised control interface for approved non-critical loads
```

Direct electrical actuation is outside the current MVP. Any future control interface requires site assessment, protection review, critical-load exclusion, interlocks, manual override, fail-safe testing, and institutional approval.

## Data and privacy boundary

Raw UZ workbooks are never committed. The public repository contains only aggregate quality counts, source hashes, anonymous facility aliases, normalized charts, model and controller metrics, and synthetic fallback evidence and forecasts generated from simulated edge values. Exact private timestamped readings, real facility mappings, private model files, and credentials remain outside the repository.

The source archive was supplied through the University of Zimbabwe Department of Electrical and Electronic Engineering under departmental oversight. Repository access does not grant permission to redistribute the source workbooks.

## Cost evidence status

The Cost Impact tab uses the study's aggregate energy and load-factor figures with the public ZERA average end-user tariff. It produces an indicative expenditure and planning scenarios without reproducing the confidential UZ invoice. These figures are not realised savings and must be verified during the pilot against authorised tariff and demand-register data.

## Repository structure

```text
dashboard/       Browser interface for evidence and operator workflow
docs/            Architecture, data, AI, deployment, business, security, and evidence notes
evidence/        Public-safe aggregate metrics, charts, hashes, and scan reports
hardware/        Meter interface, edge-gateway, BOM, and control-interface planning
sample_data/     Safe sample data used by the demonstration
scripts/         Audit, evidence, comparison, security, setup, and release commands
software/        Model training, controller backtesting, and aggregate analytics
src/             Ingestion, cleaning, features, models, API, tariff, and recommendation modules
tests/           Automated unit and integration tests
```

## Submission documentation

- [Submission evidence index](docs/submission_evidence_index.md)
- [AI justification](docs/ai_justification.md)
- [Dataset statement](docs/dataset_statement.md)
- [Architecture](docs/architecture.md)
- [Estates and Facilities workflow](docs/operator_workflow.md)
- [Deployment plan](docs/deployment_plan.md)
- [Business model](docs/business_model.md)
- [Security and compliance](docs/security_and_compliance.md)
- [Reproduction guide](docs/reproduction.md)
- [Known limitations](docs/known_limitations.md)

## Current limitations

- The public package runs live inference from accelerated simulated gateway values, not a commissioned campus meter connection.
- No controllable-load response dataset is available, so avoided kVA is not claimed.
- Billing-grade tariff rates and demand-charge rules have not yet been verified.
- Weather coverage begins late in the study period and is excluded from the principal benchmark.
- Signed reactive-power direction requires confirmation against the meter or export convention.
- The current build is advisory and does not implement automatic electrical switching.
