# AI4I Track 3 Submission Evidence Index

This index gives judges a direct path from each product-readiness requirement to the relevant evidence.

## Core submission evidence

| Requirement | Primary evidence |
|---|---|
| Problem and target users | `README.md`, `docs/user_persona_and_journey.md` |
| Working MVP | `START_AI4I_EMS.bat`, `src/api/server.py`, `dashboard/` |
| Demo and walkthrough | `FINAL_DEMO_INSTRUCTIONS.txt`, `docs/demo_walkthrough.md`, `docs/screenshots/` |
| Architecture | `docs/architecture.md`, `docs/diagrams/` |
| Data source, rights, and quality | `docs/dataset_statement.md`, `evidence/public_dashboard/dashboard_evidence.json` |
| AI method and justification | `docs/ai_justification.md`, `docs/model_card.md` |
| AI versus simple rule | dashboard AI vs rule tab, aggregate controller comparison |
| User workflow | `docs/operator_workflow.md`, Estates and Facilities dashboard tab |
| Edge integration | `src/edge/`, `docs/edge_gateway_demo.md`, Edge gateway tab |
| Operational edge-to-AI inference | `src/live/`, `docs/live_inference/`, Live forecast tab, `/api/live-forecasts` |
| Cost impact | `docs/cost_impact_methodology.md`, `evidence/cost_impact/` |
| Business model | `docs/business_model.md` |
| Deployment model | `docs/deployment_plan.md`, `docs/pilot_deployment_plan.md` |
| Security and responsible AI | `docs/security_and_compliance.md`, `scripts/security_scan.py` |
| Testing | `tests/`, `.github/workflows/quality.yml`, `evidence/validation/` |
| API and integration | `docs/api_reference.md`, FastAPI `/docs` |
| Accessibility | `docs/accessibility_check.md` |
| Known limitations and claim discipline | `docs/known_limitations.md`, `docs/claim_register.md` |
| Team and ownership | `docs/team_and_ownership.md` |
| Product-readiness alignment | `docs/guideline_alignment.md` |
| Change history | `CHANGELOG.md` |
| Usage conditions | `LICENSE` |

## Demonstration sequence

```text
START_AI4I_EMS.bat
START_EDGE_DEMO.bat
RUN_STAGE4_COST_MODEL.bat
```

The cost model only needs to be rebuilt when its public inputs change.

## Evidence boundary

Public repository:

- safe sample meter data;
- aggregate data-quality metrics;
- anonymous facility aliases;
- normalized profiles and heatmaps;
- aggregate forecast and controller results;
- public-source cost planning evidence;
- simulated edge readings and forecasts generated from those incoming values;
- screenshots and test reports.

Excluded:

- raw UZ workbooks;
- source data ZIP;
- exact private interval records;
- real facility and meter mappings;
- private trained model files;
- credentials;
- completed environment files;
- local runtime state.

## Operating boundary

The current system is advisory and operator-confirmed. It performs operational inference on simulated gateway values, but no autonomous electrical switching, commissioned live UZ installation, realised savings, or billing-grade tariff reconstruction is claimed.

## Dashboard screenshot set

The seven public-safe screenshots are catalogued in [`screenshots/README.md`](screenshots/README.md).
