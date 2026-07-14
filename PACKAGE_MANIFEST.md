# Operational Live Repository Package Manifest

## Purpose

This is the guideline-aligned AI4I Track 3 repository with a demonstrated simulated edge-to-AI path. It preserves the verified historical research evidence and connects newly received gateway values to feature engineering, next-half-hour inference, facility-limit risk classification, advisory recommendations and the Estates and Facilities workflow.

## Demonstrated operational path

```text
Accelerated simulated gateway values
    -> schema validation and duplicate protection
    -> append-only local meter store
    -> four-interval rolling history
    -> live-compatible feature engineering
    -> public demo model or private model
    -> next-half-hour kVA forecast
    -> facility-limit utilization and risk
    -> advisory recommendation
    -> live alert queue and operator decision log
```

## Model boundary

- The verified research benchmark remains separate from live deployment evidence.
- The public repository contains a synthetic fallback model only so judges can reproduce the complete path without private UZ data.
- The private training workflow was exercised against the authorised 22-workbook archive with an untouched April 2026 holdout.
- The raw archive, real facility mapping and trained private model are not included in the public package.
- The full delivery ZIP supplies a sibling private workspace where the authorised dataset ZIP can be placed and trained locally.

## Main live components

- `src/live/features.py`: rolling-history and feature generation.
- `src/live/training.py`: compact deployment-model training and chronological evaluation.
- `src/live/model_manager.py`: public/private model selection.
- `src/live/service.py`: live forecast, risk and recommendation pipeline.
- `src/live/forecast_store.py`: persistent, deduplicated live forecasts.
- `scripts/train_private_live_model.py`: private ZIP parsing, anonymisation, training and testing.
- `models/public_demo/live_forecaster.json`: reproducible synthetic fallback.
- `TRAIN_PRIVATE_LIVE_MODEL.bat`: local private training launcher.
- `START_EDGE_DEMO.bat`: accelerated simulated half-hour feed.
- `Live forecast` dashboard tab.
- `/api/model-status`, `/api/live-forecasts`, `/api/live-alerts` and `/api/live-inference/rebuild`.

## Final validation

- Automated tests: **35 passed**.
- API smoke test: **PASS**, including four-reading edge-to-AI inference.
- JavaScript syntax: **PASS**.
- Security scan: **PASS**, zero findings.
- Repository audit: **PASS**, zero findings.
- Public demo live forecast: **generated after four completed simulated intervals**.
- Private training pipeline: **tested on 22 anonymised facilities**, with private artefacts removed afterward.
- Files checked by final audit: **186**.
- Public dashboard screenshots included: **7**.

## Entry points

- `START_AI4I_EMS.bat`
- `START_EDGE_DEMO.bat`
- `TRAIN_PRIVATE_LIVE_MODEL.bat`
- `RUN_STAGE4_COST_MODEL.bat`
- `FINAL_DEMO_INSTRUCTIONS.txt`
- `TEAM_SETUP_AND_RUN_INSTRUCTIONS.txt`
- `docs/live_inference/PRIVATE_MODEL_HANDOFF_PLAN.md`

## Excluded by design

- raw UZ workbooks and source archive;
- real facility names, account details and meter mapping;
- private trained model and private training outputs;
- runtime readings, forecasts, decisions and gateway state;
- local virtual environments, caches and logs;
- credentials and completed `.env` files;
- claims of commissioned live campus operation, autonomous switching or realised financial savings.
